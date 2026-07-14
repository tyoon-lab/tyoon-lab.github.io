#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import sys

repo = Path.cwd()
home_path = repo / "index.html"
css_path = repo / "assets" / "css" / "style.css"

if not home_path.exists():
    print(f"ERROR: {home_path} not found.")
    print("Run this file from the tyoon-lab.github.io repository root.")
    sys.exit(1)

if not css_path.exists():
    print(f"ERROR: {css_path} not found.")
    sys.exit(1)

home = home_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

# Refine the About-panel lead sentence.
old_lead = (
    '<p class="about-lead">Our approach treats electrochemical measurements '
    'as inverse probes of hidden system states.</p>'
)
new_lead = (
    '<p class="about-lead">Electrochemical signals serve as inverse probes '
    'of hidden system states.</p>'
)

if old_lead in home:
    home = home.replace(old_lead, new_lead, 1)
elif new_lead not in home:
    print("ERROR: The expected About-panel lead sentence was not found.")
    sys.exit(2)

marker_start = "/* === Final homepage hierarchy tweak: START === */"
marker_end = "/* === Final homepage hierarchy tweak: END === */"

css_block = r'''
/* === Final homepage hierarchy tweak: START === */
.hero-description {
  color: rgba(255,255,255,.55) !important;
  font-size: clamp(.90rem, 1.05vw, .98rem) !important;
  line-height: 1.72 !important;
}

.about-panel .about-lead {
  color: var(--navy-900) !important;
  font-weight: 750 !important;
}
/* === Final homepage hierarchy tweak: END === */
'''

if marker_start in css and marker_end in css:
    css = re.sub(
        re.escape(marker_start) + r".*?" + re.escape(marker_end),
        css_block.strip(),
        css,
        count=1,
        flags=re.DOTALL,
    )
else:
    css = css.rstrip() + "\n\n" + css_block.strip() + "\n"

home_backup = home_path.with_suffix(home_path.suffix + ".before-final-hierarchy-tweak")
css_backup = css_path.with_suffix(css_path.suffix + ".before-final-hierarchy-tweak")

if not home_backup.exists():
    shutil.copy2(home_path, home_backup)
if not css_backup.exists():
    shutil.copy2(css_path, css_backup)

home_path.write_text(home, encoding="utf-8")
css_path.write_text(css, encoding="utf-8")

print("Final homepage hierarchy tweak completed.")
print()
print("Updated:")
print("  - Hero supporting description: slightly smaller and lighter")
print("  - About-panel lead: shorter and stronger")
print()
print("Next:")
print("  bundle exec jekyll serve --livereload")
print("  Open http://localhost:4000/")
print("  Press Ctrl+F5 if needed.")
