#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import sys

repo = Path.cwd()
css_path = repo / "assets" / "css" / "style.css"

if not css_path.exists():
    print(f"ERROR: {css_path} not found.")
    print("Run this file from the tyoon-lab.github.io repository root.")
    sys.exit(1)

css = css_path.read_text(encoding="utf-8")

marker_start = "/* === Cache-reveal typography correction: START === */"
marker_end = "/* === Cache-reveal typography correction: END === */"

css_block = r'''
/* === Cache-reveal typography correction: START === */
.hero-tagline {
  color: rgba(255,255,255,.90) !important;
  font-size: clamp(1.02rem, 1.35vw, 1.16rem) !important;
  font-weight: 620 !important;
  line-height: 1.56 !important;
}

.hero-description {
  color: rgba(255,255,255,.66) !important;
  font-size: clamp(.92rem, 1.05vw, .99rem) !important;
  font-weight: 400 !important;
  line-height: 1.70 !important;
}

.about-panel {
  padding: 34px 48px !important;
}

.about-panel .about-lead {
  margin: 0 !important;
  color: var(--navy-900) !important;
  font-family: inherit !important;
  font-size: clamp(1.08rem, 1.55vw, 1.28rem) !important;
  font-weight: 700 !important;
  line-height: 1.48 !important;
}

.about-panel .about-detail {
  margin: 12px 0 0 !important;
  color: var(--slate-500) !important;
  font-size: clamp(.96rem, 1.15vw, 1.04rem) !important;
  line-height: 1.68 !important;
}

@media (max-width: 700px) {
  .about-panel {
    padding: 28px 24px !important;
  }
}
/* === Cache-reveal typography correction: END === */
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

backup = css_path.with_suffix(css_path.suffix + ".before-cache-reveal-fix")
if not backup.exists():
    shutil.copy2(css_path, backup)

css_path.write_text(css, encoding="utf-8")

print("Typography correction applied.")
print(f"Backup: {backup}")
print()
print("Adjusted:")
print("  - Decoding tagline: less bold and slightly smaller")
print("  - Yoon Lab description: readable but still secondary")
print("  - About lead: smaller sans-serif emphasis")
print("  - About box: reduced vertical padding")
print()
print("Next:")
print("  bundle exec jekyll serve --livereload")
print("  Open http://localhost:4000/")
print("  Press Ctrl+F5 once after the server reloads.")
