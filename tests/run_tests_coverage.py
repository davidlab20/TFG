"""Program to run the tests and get the coverage."""

import os
import sys

# Execute --> python3 -m pytest . --cov=aframexr --cov-report=term-missing
os.system(f"{sys.executable} -m pytest . --cov=aframexr --cov-report=term-missing")

# Remove .coverage file
if os.path.exists(".coverage"):
    os.remove(".coverage")
