# AFrameXR <a href="https://davidlab20.github.io/TFG/"><img align="right" src="https://davidlab20.github.io/TFG/static/imgs/logo.png" height="50"></a>

![PyPI](https://img.shields.io/pypi/v/aframexr)
![License](https://img.shields.io/github/license/davidlab20/TFG)

**AFrameXR** is a declarative 3D visualization library for Python. With a syntax inspired by
[Vega-Altair](https://github.com/vega/altair) and [Vega-Lite](https://github.com/vega/vega-lite), it enables you to
easily create and display interactive 3D graphics, offering a simple and intuitive way to visualize your data in three
dimensions.

## Features

- **XR Visualization** - Explore charts in immersive XR environments
- **Notebooks** - Seamlessly integrates with Jupyter and Marimo Notebooks for interactive visualization.
- **3D Browser Visualization** - Visualize 3D charts directly in your web browser.
- **Chart interaction** - Interact with charts for deeper insights and dynamic exploration.

## Installation

```bash
pip install aframexr
```

## Documentation
You can find the full documentation [here](https://davidlab20.github.io/TFG/).

## Simple example

```python
import aframexr
from aframexr.datasets import data

# Load a simple dataset
cars = data.cars()

# Create the chart
aframexr.Chart(
    cars,
    position="0 2 -5"
).mark_bar().encode(
    x="model",
    y="sales",
    color="motor"
)
```
