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

old_about = (
    '<p>Our research connects electrochemical measurements with real interfacial phenomena in batteries, '
    'solid-state and polymer electrolytes, corrosion systems, supercapacitors, seawater electrolysis, and '
    'electrochemical sensors. We focus on translating signals such as impedance, transient current, and mass '
    'change into mechanistic understanding of degradation and failure.</p>'
)

new_about = '''<p class="about-lead">Our approach treats electrochemical measurements as inverse probes of hidden system states.</p>
      <p class="about-detail">By combining impedance, transient response, mass change, and complementary characterization with physics-based analysis, we quantify reaction kinetics, transport limitations, interfacial degradation, and corrosion.</p>'''

if old_about in home:
    home = home.replace(old_about, new_about, 1)
elif 'class="about-lead"' in home and 'class="about-detail"' in home:
    home = re.sub(
        r'<p class="about-lead">.*?</p>\s*<p class="about-detail">.*?</p>',
        new_about,
        home,
        count=1,
        flags=re.DOTALL,
    )
else:
    print("ERROR: The expected About-panel paragraph was not found in index.html.")
    sys.exit(2)

marker_start = "/* === Hero and about hierarchy refinement: START === */"
marker_end = "/* === Hero and about hierarchy refinement: END === */"

css_block = r'''
/* === Hero and about hierarchy refinement: START === */
.hero-tagline {
  margin: 28px 0 0 !important;
  max-width: 720px !important;
  color: rgba(255,255,255,.94) !important;
  font-size: clamp(1.12rem, 1.65vw, 1.28rem) !important;
  font-weight: 760 !important;
  line-height: 1.5 !important;
}

.hero-description {
  margin: 14px 0 0 !important;
  max-width: 690px !important;
  color: rgba(255,255,255,.62) !important;
  font-size: clamp(.92rem, 1.1vw, 1rem) !important;
  font-weight: 400 !important;
  line-height: 1.72 !important;
}

.about-panel .about-lead {
  margin: 0 !important;
  max-width: 900px;
  color: var(--navy-900) !important;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1.25rem, 2vw, 1.62rem) !important;
  font-weight: 700;
  line-height: 1.4 !important;
}

.about-panel .about-detail {
  margin: 16px 0 0 !important;
  max-width: 960px;
  color: var(--slate-500) !important;
  font-size: clamp(.98rem, 1.25vw, 1.08rem) !important;
  line-height: 1.72 !important;
}
/* === Hero and about hierarchy refinement: END === */
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

home_backup = home_path.with_suffix(home_path.suffix + ".before-hierarchy-refinement")
css_backup = css_path.with_suffix(css_path.suffix + ".before-hierarchy-refinement")

if not home_backup.exists():
    shutil.copy2(home_path, home_backup)
if not css_backup.exists():
    shutil.copy2(css_path, css_backup)

home_path.write_text(home, encoding="utf-8")
css_path.write_text(css, encoding="utf-8")

print("Hero and About-panel hierarchy refined.")
print()
print("Updated:")
print("  index.html")
print("  assets/css/style.css")
print()
print("Backups:")
print(f"  {home_backup}")
print(f"  {css_backup}")
print()
print("Next:")
print("  bundle exec jekyll serve --livereload")
print("  Open http://localhost:4000/")
print("  Press Ctrl+F5 if needed.")
