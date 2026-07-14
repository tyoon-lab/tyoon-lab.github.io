#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

repo = Path.cwd()

# This repository uses index.html, not index.md.
path = repo / "index.html"
if not path.exists():
    fallback = repo / "index.md"
    if fallback.exists():
        path = fallback
    else:
        print(f"ERROR: Neither {repo / 'index.html'} nor {fallback} was found.")
        print("Run this file from the tyoon-lab.github.io repository root.")
        sys.exit(1)

text = path.read_text(encoding="utf-8")

replacements = [
    (
        'description: "Quantitative electrochemical diagnostics for interfaces, degradation, corrosion, and energy materials."',
        'description: "Mechanistic electrochemical diagnostics for interfaces, degradation, corrosion, and transport."'
    ),
    (
        '<h1>Decoding Electrochemical Interfaces, Degradation, and Corrosion</h1>',
        '<h1>Mechanistic Electrochemical Diagnostics</h1>'
    ),
    (
        '<p>Yoon Lab develops quantitative electrochemical diagnostics to reveal how interfacial degradation, transport limitations, side reactions, and corrosion govern the performance and lifetime of energy materials and devices.</p>',
        '<p>Decoding interfaces, degradation, corrosion, and transport from electrochemical signals.</p>'
    ),
    (
        '<h2 class="section-title">Quantitative diagnostics for electrochemical interfaces</h2>',
        '<h2 class="section-title">Quantitative Diagnostics for Electrochemical Systems</h2>'
    ),
    (
        '<p class="section-lead">We use electrochemical signals as quantitative probes of interfaces, transport, side reactions, corrosion, and degradation in energy materials and devices.</p>',
        '<p class="section-lead">We use electrochemical signals as quantitative probes of hidden interfacial states, transport processes, side reactions, corrosion, and degradation across energy materials and devices.</p>'
    ),
]

missing = [old for old, _ in replacements if old not in text]
if missing:
    print(f"ERROR: Some expected text was not found in {path.name}.")
    print("The file may already have been edited. Missing blocks:")
    for item in missing:
        print()
        print(item)
    sys.exit(2)

backup = path.with_suffix(path.suffix + ".before-identity-update")
shutil.copy2(path, backup)

for old, new in replacements:
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")

print(f"{path.name} updated successfully.")
print(f"Backup: {backup}")
print()
print("Changed:")
print("  Hero: Mechanistic Electrochemical Diagnostics")
print("  Tagline: Decoding interfaces, degradation, corrosion, and transport from electrochemical signals.")
print("  Research Themes: Quantitative Diagnostics for Electrochemical Systems")
print()
print("Next:")
print("  bundle exec jekyll serve --livereload")
print("  Open http://localhost:4000/")
