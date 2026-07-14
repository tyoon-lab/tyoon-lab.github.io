#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import sys

repo = Path.cwd()
research_path = repo / "research.md"
data_path = repo / "_data" / "research.yml"
css_path = repo / "assets" / "css" / "style.css"

for path in (research_path, data_path, css_path):
    if not path.exists():
        print(f"ERROR: {path} not found.")
        print("Run this file from the tyoon-lab.github.io repository root.")
        sys.exit(1)

research = research_path.read_text(encoding="utf-8")
data = data_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

# 1. Broaden the Research hero without redefining all work as diagnostics.
hero_replacements = [
    (
        "<h1>Electrochemical signals as windows into hidden interfacial processes</h1>",
        "<h1>Electrochemical signals as windows into hidden states and mechanisms</h1>",
    ),
    (
        "<p>Yoon Lab develops quantitative approaches to understand how interfaces, transport limitations, side reactions, and corrosion determine the performance and lifetime of electrochemical energy systems.</p>",
        "<p>Yoon Lab develops quantitative approaches to understand how interfaces, transport limitations, side reactions, degradation, and corrosion determine the performance and lifetime of electrochemical energy systems.</p>",
    ),
]

for old, new in hero_replacements:
    if old in research:
        research = research.replace(old, new, 1)
    elif new not in research:
        print("ERROR: Expected Research hero text was not found:")
        print(old)
        sys.exit(2)

# 2. Convert the Approach section from two stages to three.
old_approach = '''    <p class="section-lead">Our work emphasizes the translation of electrochemical measurements into physically meaningful descriptors such as interfacial resistance, transport limitation, reaction rate, corrosion susceptibility, and degradation mode.</p>
    <div class="grid-2" style="margin-top: 34px;">
      <article class="paper-card">
        <h3>Signal acquisition</h3>
        <p>EIS, DRT, PITT/GITT, chronoamperometry, QCM, RRDE, and operando or post-mortem materials characterization.</p>
      </article>
      <article class="paper-card">
        <h3>Mechanistic interpretation</h3>
        <p>Physics-informed modeling, transport analysis, kinetic decoupling, and degradation/corrosion mapping.</p>
      </article>
    </div>'''

new_approach = '''    <p class="section-lead">Our work translates electrochemical measurements into physically meaningful descriptors of reaction kinetics, interfacial resistance, transport limitation, corrosion susceptibility, and degradation mode.</p>
    <div class="approach-grid">
      <article class="paper-card">
        <h3>Signal acquisition</h3>
        <p>EIS, DRT, PITT/GITT, chronoamperometry, QCM, RRDE, and operando or post-mortem materials characterization.</p>
      </article>
      <article class="paper-card">
        <h3>Parameter extraction</h3>
        <p>Time constants, interfacial resistance, reaction rates, diffusion and transport descriptors, mass response, and corrosion susceptibility.</p>
      </article>
      <article class="paper-card">
        <h3>Mechanistic interpretation</h3>
        <p>Physics-informed modeling, kinetic decoupling, degradation mapping, and inverse identification of hidden system states.</p>
      </article>
    </div>'''

if old_approach in research:
    research = research.replace(old_approach, new_approach, 1)
elif '<div class="approach-grid">' not in research:
    print("ERROR: Expected Approach section was not found.")
    sys.exit(3)

# 3. Broaden only the Advanced Electrochemical Diagnostics card.
old_description = (
    '  description: "We develop signal-based diagnostic methods using EIS/DRT, '
    'PITT/GITT, QCM, RRDE, transient analysis, and electrochemical modeling to '
    'quantify hidden interfacial processes."'
)
new_description = (
    '  description: "We develop signal-based diagnostic methods using EIS/DRT, '
    'PITT/GITT, QCM, RRDE, transient analysis, and electrochemical modeling to '
    'identify and quantify hidden kinetic, transport, interfacial, and degradation phenomena."'
)

if old_description in data:
    data = data.replace(old_description, new_description, 1)
elif new_description not in data:
    print("ERROR: Expected Advanced Electrochemical Diagnostics description was not found.")
    sys.exit(4)

# 4. Add responsive three-stage Approach layout.
marker_start = "/* === Research approach three-stage layout: START === */"
marker_end = "/* === Research approach three-stage layout: END === */"

css_block = r'''
/* === Research approach three-stage layout: START === */
.approach-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
  margin-top: 34px;
}

.approach-grid .paper-card {
  height: 100%;
}

@media (max-width: 980px) {
  .approach-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 680px) {
  .approach-grid {
    grid-template-columns: 1fr;
  }
}
/* === Research approach three-stage layout: END === */
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

# Backups
for path in (research_path, data_path, css_path):
    backup = path.with_suffix(path.suffix + ".before-research-refinement")
    if not backup.exists():
        shutil.copy2(path, backup)

research_path.write_text(research, encoding="utf-8")
data_path.write_text(data, encoding="utf-8")
css_path.write_text(css, encoding="utf-8")

print("Research page refinement completed.")
print()
print("Updated:")
print("  - Hero broadened beyond interfacial processes")
print("  - Existing quantitative-approaches description retained and expanded")
print("  - Advanced Diagnostics card broadened")
print("  - Approach changed to acquisition → extraction → interpretation")
print()
print("Next:")
print("  bundle exec jekyll serve --livereload")
print("  Open http://localhost:4000/research/")
print("  Press Ctrl+F5 after the server reloads.")
