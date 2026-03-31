# AFrameXR <a href="https://davidlab20.github.io/TFG/"><img align="right" src="https://davidlab20.github.io/TFG/static/imgs/logo.png" height="50"></a>

![PyPI](https://img.shields.io/pypi/v/aframexr)
![License](https://img.shields.io/github/license/davidlab20/TFG)

**AFrameXR** is a declarative Python library for building immersive 3D and XR data visualizations — directly in your
browser, with no 3D experience required.

Inspired by [Vega-Altair](https://github.com/vega/altair) and [Vega-Lite](https://github.com/vega/vega-lite), AFrameXR
lets you define interactive 3D charts using a simple grammar, and render them directly in the browsers and XR devices — 
without low-level 3D programming.

## Live Demo

> https://davidlab20.github.io/TFG/examples/index.html

## Features

- **Declarative API** — Define charts using a high-level grammar
- **XR Visualization** — Explore charts in immersive environments
- **Notebook Integration** — Works with Jupyter and Marimo
- **Browser Rendering** — Visualize charts directly in the browser
- **Interactive Exploration** — Navigate and interact with your data

## Why AFrameXR?

AFrameXR brings the declarative visualization paradigm to 3D and XR environments.

- No need to learn complex 3D engines
- Inspired by proven visualization tools like Vega-Lite
- Built for the web and XR from the ground up
- Clean and concise API for rapid prototyping

## Installation

```bash
pip install aframexr
```

## Simple example

```python
import aframexr
from aframexr.datasets import data

# Load dataset
cars = data.cars()

# Create a 3D chart
aframexr.Chart(
    cars,
    position="0 2 -5"
).mark_bar().encode(
    x="model",
    y="sales",
    z="doors:N",  # :N indicates a categorical (nominal) field
    color="motor"
)
```

## Supported Environments

- Jupyter Notebook
- Marimo Notebooks
- Modern web browsers (Chrome, Firefox)
- XR devices

## Documentation
Full documentation: https://davidlab20.github.io/TFG/
