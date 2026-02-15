"""Program to convert the .py notebooks into .ipynb for MyBinder."""

import glob
import os
import subprocess

NOTEBOOKS_DIR = ''

try:
    # Change into docs/examples/notebooks/ directory
    os.chdir(NOTEBOOKS_DIR)

    # Convert all .py notebooks into .ipynb notebooks for MyBinder
    py_files = glob.glob('*.py')
    if py_files:
        subprocess.run(['jupytext', '--to', 'notebook'] + py_files, check=True)
        print('Converted notebooks into .ipynb')
    else:
        print('No .py notebooks found')

except FileNotFoundError:
    print(f'The directory {NOTEBOOKS_DIR} does not exist')
except subprocess.CalledProcessError:
        print('Error while running jupytext command. Make sure jupytext is installed and available')
except Exception as e:
        print(f"An unexpected error occurred: {e}")
