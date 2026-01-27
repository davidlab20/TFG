#!/bin/bash

python3 -m pytest ../tests/ --cov=aframexr --cov-report=term-missing && rm .coverage
