import ast
import os
import shutil
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# ===== CONFIG =====
BASE_DIR = Path(__file__).parent.resolve()
API_DIR = BASE_DIR / '..' / 'aframexr' / 'api'
NOTEBOOKS_DIR = BASE_DIR / 'notebooks'
OUTPUT_DIR = BASE_DIR / os.getenv('OUTPUT_DIR', 'github_pages')
OUTPUT_STATIC_DIR = OUTPUT_DIR / 'static'
STATIC_DIR = BASE_DIR / 'static'
TEMPLATES_DIR = BASE_DIR / 'templates'

# ===== ENVIRONMENT =====
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# ===== API ITEMS =====
api_items = []

for py_file in API_DIR.rglob('*.py'):
    with open(py_file, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and not node.name.startswith('_'):
            api_items.append({
                'name': node.name,
                'docstring': ast.get_docstring(node),
            })

        elif isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
            api_items.append({
                'name': node.name,
                'docstring': ast.get_docstring(node),
            })

# ===== NOTEBOOKS =====
NOTEBOOKS = [
    {
        'title': file_name.replace('_', ' ').title(),
        'marimo_name': file_name.replace('_', '-') + '.html',
        'mybinder_name': file_name + '.ipynb'
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
repo_name = os.environ.get('GITHUB_REPOSITORY', '').split('/')[-1]
BASE_URL = f'/{repo_name}/' if repo_name else './'

for html_file in TEMPLATES_DIR.rglob('*.html'):
    if '_layouts' in html_file.parts:
        continue

    rel_path = html_file.relative_to(TEMPLATES_DIR).as_posix()
    output_path = OUTPUT_DIR / rel_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Profundidad relativa para los assets
    depth = len(html_file.relative_to(TEMPLATES_DIR).parents) - 1
    current_base_url = '../' * depth if depth > 0 else './'

    template = env.get_template(rel_path)
    context = {
        'base_url': current_base_url,
        'title': TITLES.get(rel_path, html_file.stem.replace('-', ' ').title()),
        'notebooks': NOTEBOOKS,
        'api_items': api_items,
    }

    html = template.render(**context)
    output_path.write_text(html, encoding='utf-8')
    print(f'Wrote {output_path}')

# ===== COPY STATIC FILES =====
if STATIC_DIR.exists():
    shutil.copytree(STATIC_DIR, OUTPUT_STATIC_DIR, dirs_exist_ok=True)
    print(f'Copied static files to {OUTPUT_STATIC_DIR}')
