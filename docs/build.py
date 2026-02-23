import argparse
import shutil

from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# ===== COMMAND LINE ARGUMENTS =====
parser = argparse.ArgumentParser(description='Build pages with Jinja2')
parser.add_argument(
    '--production',
    action='store_true',
    help='Production mode (for GitHub Pages). If not generating for local.'
)
args = parser.parse_args()

# ===== CONFIG =====
BASE_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = BASE_DIR / 'templates'
OUTPUT_DIR = BASE_DIR / 'github_pages'
STATIC_DIR = BASE_DIR / 'static'
OUTPUT_STATIC_DIR = OUTPUT_DIR / 'static'

# ===== ENVIRONMENT =====
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# ===== PAGES' TITLES =====
TITLES = {
    'index.html': '3D Visualization in Python',
    'get_started/index.html': 'Getting Started',
    'examples/index.html': 'Examples',
    'user_guide/user-guide.html': 'User Guide',
    'user_guide/api.html': 'API Reference',
}

# ===== Generate pages =====
BASE_URL = '/TFG/' if args.production else ''
for html_file in TEMPLATES_DIR.rglob('*.html'):  # Recursive
    if '_layouts' in html_file.parts:
        continue  # Exclude _layouts/

    rel_path = html_file.relative_to(TEMPLATES_DIR).as_posix()
    output_path = OUTPUT_DIR / rel_path

    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = env.get_template(rel_path)
    context = {
        'base_url': BASE_URL,
        'title': TITLES.get(rel_path, html_file.stem.replace('-', ' ').title())
    }

    html = template.render(**context)
    output_path.write_text(html, encoding='utf-8')
    print(f"Wrote {output_path}")

# ===== COPY STATIC FILES =====
if STATIC_DIR.exists():
    if OUTPUT_STATIC_DIR.exists():
        shutil.rmtree(OUTPUT_STATIC_DIR)
    shutil.copytree(STATIC_DIR, OUTPUT_STATIC_DIR)
    print(f"Copied static files to {OUTPUT_STATIC_DIR}")

