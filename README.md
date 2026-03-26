# AFrameXR <a href="https://davidlab20.github.io/TFG/"><img align="right" src="docs/static/imgs/logo.png" height="50"></a>

![PyPI](https://img.shields.io/pypi/v/aframexr)
![License](https://img.shields.io/github/license/davidlab20/TFG)

**AFrameXR** is a declarative 3D visualization library for Python. With a syntax inspired by
[Vega-Altair](https://github.com/vega/altair) and [Vega-Lite](https://github.com/vega/vega-lite), it enables you to
easily create and display interactive 3D graphics, offering a simple and intuitive way to visualize your data in three
dimensions.

## Documentation
You can find the full documentation [here](https://davidlab20.github.io/TFG/).

## Installation

```bash
pip install aframexr
```

## Simple example

```python
import aframexr

# Load a simple dataset
from aframexr.datasets import data
chart_data = data.cars()

# Create the chart
chart = aframexr.Chart(
    chart_data,
    position="0 2 -5"
).mark_bar().encode(
    x="model",
    y="sales",
    color="motor"
)
```
