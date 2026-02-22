import argparse
import os
from jinja2 import Environment, FileSystemLoader

# ===== COMMAND LINE ARGUMENTS =====
parser = argparse.ArgumentParser(description='Build pages with Jinja2')
parser.add_argument(
    '--prod',
    action='store_true',
    help='Production mode (for GitHub Pages). If not generating for local'
)
args = parser.parse_args()

# ===== CONFIG =====
DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

# ===== ENVIRONMENT =====
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# ===== PAGES =====
PAGES = [
    {
        'template': 'base.html',
        'output': 'index.html',
        'title': '3D Visualization in Python',
    },
]

# ===== BASE URL =====
if args.prod:
    BASE_URL = '/TFG/'  # GitHub Pages
else:
    BASE_URL = ''  # Local

# ===== Generate pages =====
for page in PAGES:
    full_output_path = os.path.join(DOCS_DIR, page['output'])
    output_dir = os.path.dirname(full_output_path)

    os.makedirs(output_dir, exist_ok=True)

    template = env.get_template(page['template'])

    context = {
        'title': page['title'],
        'base_url': BASE_URL,
    }

    # Render
    html = template.render(**context)
    with open(full_output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Wrote {full_output_path}')
