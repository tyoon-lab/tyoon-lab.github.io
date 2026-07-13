#!/usr/bin/env python3
"""
Fill blank DOI fields in _data/publications.yml using Crossref metadata,
then make publication titles link to DOI URLs on Publications and Research pages.

Run from the repository root:
    python tools/update_publication_dois.py

No third-party Python packages are required.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
import time
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


CROSSREF_API = "https://api.crossref.org/works"
USER_AGENT = (
    "YoonLabWebsiteDOIUpdater/1.0 "
    "(https://yoonlab.khu.ac.kr; mailto:tyoon@khu.ac.kr)"
)
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
ENTRY_START = re.compile(r"^- number:\s*(\d+)\s*$")
KEY_LINE = re.compile(r"^  ([A-Za-z_][A-Za-z0-9_]*):(?:\s*(.*))?$")


@dataclass
class Publication:
    number: int
    year: int | None
    title: str
    journal: str
    authors: str
    doi: str
    start: int
    end: int
    doi_line: int | None


@dataclass
class Candidate:
    doi: str
    title: str
    journal: str
    year: int | None
    first_author: str
    score: float
    title_score: float
    journal_score: float
    year_score: float
    author_score: float


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = text.replace("–", "-").replace("—", "-").replace("−", "-")
    text = text.replace("‐", "-").replace("‑", "-")
    text = re.sub(r"([A-Za-z])\s+(\d)", r"\1\2", text)
    text = re.sub(r"(\d)\s+([A-Za-z])", r"\1\2", text)
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text).lower()
    return " ".join(text.split())


def unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    return value


def extract_field(lines: list[str], start: int, end: int, key: str) -> tuple[str, int | None]:
    target = f"  {key}:"
    for i in range(start, end):
        if lines[i].startswith(target):
            first = lines[i].split(":", 1)[1].strip()
            parts = [first]
            j = i + 1
            while j < end and not KEY_LINE.match(lines[j]):
                if lines[j].strip():
                    parts.append(lines[j].strip())
                j += 1
            return unquote_yaml_scalar(" ".join(parts).strip()), i
    return "", None


def parse_publications(lines: list[str]) -> list[Publication]:
    starts: list[tuple[int, int]] = []
    for i, line in enumerate(lines):
        match = ENTRY_START.match(line)
        if match:
            starts.append((i, int(match.group(1))))

    publications: list[Publication] = []
    for idx, (start, number) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
        title, _ = extract_field(lines, start, end, "title")
        journal, _ = extract_field(lines, start, end, "journal")
        authors, _ = extract_field(lines, start, end, "authors")
        year_text, _ = extract_field(lines, start, end, "year")
        doi, doi_line = extract_field(lines, start, end, "doi")
        try:
            year = int(float(year_text))
        except (TypeError, ValueError):
            year = None

        publications.append(
            Publication(
                number=number,
                year=year,
                title=title,
                journal=journal,
                authors=authors,
                doi=doi.strip(),
                start=start,
                end=end,
                doi_line=doi_line,
            )
        )
    return publications


def first_author_family(authors: str) -> str:
    if not authors:
        return ""
    first = authors.split(";", 1)[0].split(",", 1)[0].strip()
    if "," not in authors:
        first = authors.split(",", 1)[0].strip()
        words = first.split()
        if len(words) > 1:
            first = words[-1]
    return normalize(first)


def crossref_year(item: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "published", "issued", "created"):
        parts = item.get(key, {}).get("date-parts")
        if parts and parts[0]:
            try:
                return int(parts[0][0])
            except (TypeError, ValueError, IndexError):
                pass
    return None


def first_text(value: Any) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    if isinstance(value, str):
        return value
    return ""


def candidate_from_item(pub: Publication, item: dict[str, Any]) -> Candidate | None:
    doi = str(item.get("DOI", "")).strip()
    if not DOI_PATTERN.match(doi):
        return None

    title = first_text(item.get("title"))
    journal = first_text(item.get("container-title"))
    year = crossref_year(item)

    authors = item.get("author") or []
    first_author = ""
    if authors and isinstance(authors[0], dict):
        first_author = str(authors[0].get("family", ""))

    title_score = SequenceMatcher(None, normalize(pub.title), normalize(title)).ratio()
    journal_score = SequenceMatcher(None, normalize(pub.journal), normalize(journal)).ratio()

    if pub.year is None or year is None:
        year_score = 0.5
    elif pub.year == year:
        year_score = 1.0
    elif abs(pub.year - year) == 1:
        year_score = 0.65
    else:
        year_score = 0.0

    expected_author = first_author_family(pub.authors)
    actual_author = normalize(first_author)
    if expected_author and actual_author:
        author_score = SequenceMatcher(None, expected_author, actual_author).ratio()
    else:
        author_score = 0.5

    score = (
        0.76 * title_score
        + 0.12 * journal_score
        + 0.07 * year_score
        + 0.05 * author_score
    )

    return Candidate(
        doi=doi,
        title=title,
        journal=journal,
        year=year,
        first_author=first_author,
        score=score,
        title_score=title_score,
        journal_score=journal_score,
        year_score=year_score,
        author_score=author_score,
    )


def fetch_crossref_candidates(pub: Publication, rows: int = 8) -> list[Candidate]:
    bibliographic = " ".join(
        part for part in (pub.title, pub.journal, str(pub.year or ""), pub.authors.split(",", 1)[0])
        if part
    )
    params = {
        "query.bibliographic": bibliographic,
        "rows": str(rows),
        "select": "DOI,title,container-title,published-print,published-online,published,issued,created,author",
    }
    url = CROSSREF_API + "?" + urlencode(params)
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )

    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    items = payload.get("message", {}).get("items", [])
    candidates = [
        candidate
        for item in items
        if (candidate := candidate_from_item(pub, item)) is not None
    ]
    candidates.sort(key=lambda x: x.score, reverse=True)
    return candidates


def choose_candidate(
    candidates: list[Candidate],
    min_score: float,
    min_title_score: float,
    ambiguity_margin: float,
) -> tuple[Candidate | None, str]:
    if not candidates:
        return None, "no Crossref candidates"

    top = candidates[0]
    if top.title_score < min_title_score:
        return None, f"title similarity too low ({top.title_score:.3f})"
    if top.score < min_score:
        return None, f"combined score too low ({top.score:.3f})"

    if len(candidates) > 1:
        second = candidates[1]
        if top.score - second.score < ambiguity_margin and top.doi.lower() != second.doi.lower():
            return None, (
                f"ambiguous top matches ({top.score:.3f} vs {second.score:.3f})"
            )

    return top, "accepted"


def backup_file(path: Path) -> Path:
    backup = path.with_suffix(path.suffix + ".before-doi-update")
    shutil.copy2(path, backup)
    return backup


def patch_publications_page(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    old = """              <h4>
                {% if paper.link and paper.link != "" %}
                <a href="{{ paper.link }}">{{ paper.title }}</a>
                {% else %}
                {{ paper.title }}
                {% endif %}
              </h4>"""
    new = """              <h4>
                {% if paper.doi and paper.doi != "" %}
                <a href="https://doi.org/{{ paper.doi }}" target="_blank" rel="noopener">{{ paper.title }}</a>
                {% elsif paper.link and paper.link != "" %}
                <a href="{{ paper.link }}" target="_blank" rel="noopener">{{ paper.title }}</a>
                {% else %}
                {{ paper.title }}
                {% endif %}
              </h4>"""
    if new in text:
        return False
    if old not in text:
        raise RuntimeError(
            f"Could not find the expected title-link block in {path}. "
            "The page may have changed; update it manually using the README snippet."
        )
    backup_file(path)
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def patch_research_page(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    old = "              <h4>{{ paper.title }}</h4>"
    new = """              <h4>
                {% if paper.doi and paper.doi != "" %}
                <a href="https://doi.org/{{ paper.doi }}" target="_blank" rel="noopener">{{ paper.title }}</a>
                {% elsif paper.link and paper.link != "" %}
                <a href="{{ paper.link }}" target="_blank" rel="noopener">{{ paper.title }}</a>
                {% else %}
                {{ paper.title }}
                {% endif %}
              </h4>"""
    if new in text:
        return False
    if old not in text:
        raise RuntimeError(
            f"Could not find the expected representative-publication title in {path}."
        )
    backup_file(path)
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add verified DOI metadata to the Yoon Lab publication list."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Default: current directory.",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.88,
        help="Minimum combined Crossref match score (default: 0.88).",
    )
    parser.add_argument(
        "--min-title-score",
        type=float,
        default=0.90,
        help="Minimum normalized title similarity (default: 0.90).",
    )
    parser.add_argument(
        "--ambiguity-margin",
        type=float,
        default=0.025,
        help="Minimum separation from the second-best candidate (default: 0.025).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.12,
        help="Delay between Crossref calls in seconds (default: 0.12).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Search and report without changing files.",
    )
    parser.add_argument(
        "--skip-pages",
        action="store_true",
        help="Do not patch publications.md and research.md.",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    data_path = repo / "_data" / "publications.yml"
    publications_page = repo / "publications.md"
    research_page = repo / "research.md"

    if not data_path.exists():
        print(f"ERROR: {data_path} was not found.", file=sys.stderr)
        print("Run this command from the tyoon-lab.github.io repository root.", file=sys.stderr)
        return 2

    original_text = data_path.read_text(encoding="utf-8")
    had_trailing_newline = original_text.endswith("\n")
    lines = original_text.splitlines()
    publications = parse_publications(lines)

    if not publications:
        print("ERROR: No publication entries were parsed.", file=sys.stderr)
        return 2

    report_rows: list[dict[str, Any]] = []
    accepted_updates: dict[int, Candidate] = {}

    print(f"Found {len(publications)} publication entries.")
    for index, pub in enumerate(publications, start=1):
        if pub.doi:
            print(f"[{index:02d}/{len(publications)}] #{pub.number}: existing DOI retained")
            report_rows.append(
                {
                    "number": pub.number,
                    "year": pub.year or "",
                    "title": pub.title,
                    "status": "existing",
                    "doi": pub.doi,
                    "match_score": "",
                    "title_score": "",
                    "matched_title": "",
                    "matched_journal": "",
                    "matched_year": "",
                    "note": "existing DOI retained",
                }
            )
            continue

        print(f"[{index:02d}/{len(publications)}] #{pub.number}: searching …", end="", flush=True)
        try:
            candidates = fetch_crossref_candidates(pub)
            chosen, note = choose_candidate(
                candidates,
                min_score=args.min_score,
                min_title_score=args.min_title_score,
                ambiguity_margin=args.ambiguity_margin,
            )
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            chosen = None
            candidates = []
            note = f"Crossref request failed: {exc}"

        if chosen:
            accepted_updates[pub.number] = chosen
            print(f" matched {chosen.doi} ({chosen.score:.3f})")
            report_rows.append(
                {
                    "number": pub.number,
                    "year": pub.year or "",
                    "title": pub.title,
                    "status": "accepted",
                    "doi": chosen.doi,
                    "match_score": f"{chosen.score:.4f}",
                    "title_score": f"{chosen.title_score:.4f}",
                    "matched_title": chosen.title,
                    "matched_journal": chosen.journal,
                    "matched_year": chosen.year or "",
                    "note": note,
                }
            )
        else:
            best = candidates[0] if candidates else None
            print(f" review needed — {note}")
            report_rows.append(
                {
                    "number": pub.number,
                    "year": pub.year or "",
                    "title": pub.title,
                    "status": "review",
                    "doi": best.doi if best else "",
                    "match_score": f"{best.score:.4f}" if best else "",
                    "title_score": f"{best.title_score:.4f}" if best else "",
                    "matched_title": best.title if best else "",
                    "matched_journal": best.journal if best else "",
                    "matched_year": best.year if best and best.year else "",
                    "note": note,
                }
            )

        time.sleep(max(args.delay, 0.0))

    report_path = repo / "doi_update_report.csv"
    with report_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "number",
                "year",
                "title",
                "status",
                "doi",
                "match_score",
                "title_score",
                "matched_title",
                "matched_journal",
                "matched_year",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(report_rows)

    if args.dry_run:
        print("\nDry run completed; no site files were changed.")
        print(f"Report: {report_path}")
        return 0

    if accepted_updates:
        backup = backup_file(data_path)
        for pub in publications:
            chosen = accepted_updates.get(pub.number)
            if not chosen:
                continue
            if pub.doi_line is None:
                raise RuntimeError(f"Publication #{pub.number} has no doi field.")
            lines[pub.doi_line] = f"  doi: '{chosen.doi}'"

        updated_text = "\n".join(lines)
        if had_trailing_newline:
            updated_text += "\n"
        data_path.write_text(updated_text, encoding="utf-8")
        print(f"\nUpdated {len(accepted_updates)} DOI fields.")
        print(f"Backup: {backup}")
    else:
        print("\nNo new DOI fields met the confidence thresholds.")

    if not args.skip_pages:
        if publications_page.exists():
            changed = patch_publications_page(publications_page)
            print(f"publications.md: {'updated' if changed else 'already updated'}")
        else:
            print(f"WARNING: {publications_page} was not found.")

        if research_page.exists():
            changed = patch_research_page(research_page)
            print(f"research.md: {'updated' if changed else 'already updated'}")
        else:
            print(f"WARNING: {research_page} was not found.")

    review_count = sum(1 for row in report_rows if row["status"] == "review")
    print(f"Report: {report_path}")
    print(f"Manual review entries: {review_count}")
    print("\nNext:")
    print("  bundle exec jekyll serve --livereload")
    print("  Check http://localhost:4000/publications/ and /research/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
