import os
import shutil

from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# ===== CONFIG =====
BASE_DIR = Path(__file__).parent.resolve()
NOTEBOOKS_DIR = BASE_DIR / 'notebooks'
OUTPUT_DIR = BASE_DIR / os.getenv('OUTPUT_DIR', 'github_pages')  # Use environment variable
OUTPUT_STATIC_DIR = OUTPUT_DIR / 'static'
STATIC_DIR = BASE_DIR / 'static'
TEMPLATES_DIR = BASE_DIR / 'templates'

# ===== ENVIRONMENT =====
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# ===== NOTEBOOKS =====
NOTEBOOKS = [
    {
        'title': file_name.replace('_', ' ').title(),
        'marimo_name': file_name.replace('_', '-').replace('.py', '.html'),
        'mybinder_name': file_name.replace('.py', '.ipynb')
    }
    for nb in NOTEBOOKS_DIR.rglob('*_notebook.py')
    for file_name in [nb.stem]
]

# ===== PAGES' TITLES =====
TITLES = {
    'index.html': '3D Visualization in Python',
    'get_started/index.html': 'Getting Started',
    'examples/index.html': 'Examples',
    'user_guide/user-guide.html': 'User Guide',
    'user_guide/api.html': 'API Reference',
}

# ===== GENERATE PAGES =====
repo_name = os.environ.get('GITHUB_REPOSITORY', '').split('/')[-1]  # GitHub Actions define GITHUB_REPOSITORY
BASE_URL = f'/{repo_name}/' if repo_name else './'
for html_file in TEMPLATES_DIR.rglob('*.html'):  # Recursive
    if '_layouts' in html_file.parts:
        continue  # Exclude _layouts/

    rel_path = html_file.relative_to(TEMPLATES_DIR).as_posix()
    output_path = OUTPUT_DIR / rel_path

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Calculate relative depth depending on file's depth
    rel_depth = len(html_file.relative_to(TEMPLATES_DIR).parents) - 1
    BASE_URL = '../' * rel_depth

    template = env.get_template(rel_path)
    context = {
        'base_url': BASE_URL,
        'title': TITLES.get(rel_path, html_file.stem.replace('-', ' ').title()),
        'notebooks': NOTEBOOKS,
    }

    html = template.render(**context)
    output_path.write_text(html, encoding='utf-8')
    print(f'Wrote {output_path}')

# ===== COPY STATIC FILES =====
if STATIC_DIR.exists():
    if OUTPUT_STATIC_DIR.exists():
        shutil.rmtree(OUTPUT_STATIC_DIR)
    shutil.copytree(STATIC_DIR, OUTPUT_STATIC_DIR)
    print(f'Copied static files to {OUTPUT_STATIC_DIR}')

