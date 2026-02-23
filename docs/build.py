import argparse
import os
import shutil

from jinja2 import Environment, FileSystemLoader

# ===== COMMAND LINE ARGUMENTS =====
parser = argparse.ArgumentParser(description='Build pages with Jinja2')
parser.add_argument(
    '--production',
    action='store_true',
    help='Production mode (for GitHub Pages). If not generating for local.'
)
args = parser.parse_args()

# ===== CONFIG =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

if args.production:  # GitHub Pages
    BASE_URL = '/TFG/'
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'github_pages')
else:  # Local
    BASE_URL = ''
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'local_pages')

OUTPUT_STATIC_DIR = os.path.join(OUTPUT_DIR, 'static')

# ===== ENVIRONMENT =====
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== PAGES =====
PAGES = [
    {
        'template': 'index.html',
        'title': '3D Visualization in Python',
    },
]

# ===== Generate pages =====
for page in PAGES:
    full_output_path = os.path.join(OUTPUT_DIR, page['template'])
    output_dir = os.path.dirname(full_output_path)

    os.makedirs(output_dir, exist_ok=True)

    template = env.get_template(page['template'])

    context = {'title': page['title'], 'base_url': BASE_URL}

    # Render
    html = template.render(**context)
    with open(full_output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Wrote {full_output_path}')

# ===== COPY STATIC FILES =====
if os.path.exists(STATIC_DIR):
    if os.path.exists(OUTPUT_STATIC_DIR):
        shutil.rmtree(OUTPUT_STATIC_DIR)
    shutil.copytree(STATIC_DIR, OUTPUT_STATIC_DIR)
    print(f'Copied static files to {OUTPUT_STATIC_DIR}')

