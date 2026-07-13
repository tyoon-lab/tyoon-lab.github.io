#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import sys

DOIS = {
    23: "10.1149/1945-7111/acd1bf",
    36: "10.1002/er.7588",
    64: "10.1021/acsami.7b01481",
    72: "10.1149/2.0501606jes",
    82: "10.1149/2.019404jes",
    83: "10.1166/jnn.2013.8128",
}

repo = Path.cwd()
path = repo / "_data" / "publications.yml"

if not path.exists():
    print(f"ERROR: {path} not found.")
    print("Run this file from the tyoon-lab.github.io repository root.")
    sys.exit(1)

text = path.read_text(encoding="utf-8")
backup = path.with_suffix(path.suffix + ".before-remaining-dois")
shutil.copy2(path, backup)

updated = 0
for number, doi in DOIS.items():
    pattern = re.compile(
        rf"(^- number:\s*{number}\s*$)(.*?)(^  doi:\s*['\"]?[^'\"]*['\"]?\s*$)",
        re.MULTILINE | re.DOTALL,
    )

    def replace(match):
        nonlocal_marker = None
        return match.group(1) + match.group(2) + f"  doi: '{doi}'"

    new_text, count = pattern.subn(replace, text, count=1)
    if count == 1:
        text = new_text
        updated += 1
        print(f"#{number}: {doi}")
    else:
        print(f"WARNING: publication #{number} was not found or its DOI line could not be updated.")

path.write_text(text, encoding="utf-8")
print()
print(f"Completed: {updated}/{len(DOIS)} DOI entries updated.")
print(f"Backup: {backup}")
print("Next: bundle exec jekyll serve --livereload")
