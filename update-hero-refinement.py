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

old_hero_text = (
    '<p>Decoding interfaces, degradation, corrosion, and transport '
    'from electrochemical signals.</p>'
)

new_hero_text = '''<p class="hero-tagline">Decoding interfaces, degradation, corrosion, and transport from electrochemical signals.</p>
      <p class="hero-description">Yoon Lab develops quantitative electrochemical diagnostics that connect measurable signals with the hidden mechanisms governing performance, lifetime, and failure in energy materials and devices.</p>'''

# Update the hero copy. Also allow safe re-running.
if old_hero_text in home:
    home = home.replace(old_hero_text, new_hero_text, 1)
elif 'class="hero-tagline"' in home and 'class="hero-description"' in home:
    home = re.sub(
        r'<p class="hero-tagline">.*?</p>\s*'
        r'<p class="hero-description">.*?</p>',
        new_hero_text,
        home,
        count=1,
        flags=re.DOTALL,
    )
else:
    print("ERROR: The expected hero paragraph was not found in index.html.")
    print("The Home page may have changed. Please inspect the hero text manually.")
    sys.exit(2)

marker_start = "/* === Home hero hierarchy refinement: START === */"
marker_end = "/* === Home hero hierarchy refinement: END === */"

css_block = r'''
/* === Home hero hierarchy refinement: START === */
.hero-tagline {
  margin: 28px 0 0 !important;
  max-width: 720px !important;
  color: rgba(255,255,255,.92) !important;
  font-size: clamp(1.08rem, 1.55vw, 1.24rem) !important;
  font-weight: 650 !important;
  line-height: 1.55 !important;
}

.hero-description {
  margin: 12px 0 0 !important;
  max-width: 720px !important;
  color: rgba(255,255,255,.68) !important;
  font-size: clamp(.96rem, 1.25vw, 1.06rem) !important;
  line-height: 1.68 !important;
}

.hero-actions {
  margin-top: 30px !important;
}

@media (min-width: 901px) {
  .hero-inner {
    grid-template-columns: minmax(0, 1.12fr) minmax(300px, .62fr) !important;
    gap: clamp(56px, 7vw, 96px) !important;
  }

  .signal-card {
    width: min(100%, 370px) !important;
    min-height: 390px !important;
    justify-self: end !important;
    transform: translate(16px, 24px) !important;
    transform-origin: center !important;
  }

  .signal-card svg {
    min-height: 390px !important;
  }
}

@media (max-width: 900px) {
  .hero-tagline,
  .hero-description {
    max-width: 760px !important;
  }

  .signal-card {
    transform: none !important;
  }
}
/* === Home hero hierarchy refinement: END === */
'''

# Replace an earlier version of this patch if present; otherwise append.
if marker_start in css and marker_end in css:
    pattern = re.compile(
        re.escape(marker_start) + r".*?" + re.escape(marker_end),
        flags=re.DOTALL,
    )
    css = pattern.sub(css_block.strip(), css, count=1)
else:
    css = css.rstrip() + "\n\n" + css_block.strip() + "\n"

home_backup = home_path.with_suffix(home_path.suffix + ".before-hero-refinement")
css_backup = css_path.with_suffix(css_path.suffix + ".before-hero-refinement")

if not home_backup.exists():
    shutil.copy2(home_path, home_backup)
if not css_backup.exists():
    shutil.copy2(css_path, css_backup)

home_path.write_text(home, encoding="utf-8")
css_path.write_text(css, encoding="utf-8")

print("Home hero refinement completed.")
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
print("  Press Ctrl+F5 if the previous design remains cached.")
