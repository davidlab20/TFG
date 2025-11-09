"""AframeXR chart creator"""

import json
import urllib.request

from aframexr.utils.defaults import *


class ChartCreator:
    """Chart creator base class"""

    @staticmethod
    def get_elements_specs(chart_type: str, chart_specs: dict) -> list[dict]:
        """Return the chart specifications of the chart type."""

        if chart_type == 'bar':
            return BarChartCreator(chart_specs).get_chart_specs()
        elif chart_type == 'point':
            return PointChartCreator(chart_specs).get_chart_specs()
        else:
            raise NotImplementedError(f'{chart_type} is not supported.')

    @staticmethod
    def get_axis_specs(chart_type: str, chart_specs: dict) -> tuple[str, float, float, float] | list[dict]:
        """Return the axis specifications of the chart type."""

        if chart_type == 'bar':
            return BarChartCreator(chart_specs).get_axis_specs()
        elif chart_type == 'point':
            return PointChartCreator(chart_specs).get_chart_specs()
        else:
            raise NotImplementedError(f'{chart_type} is not supported.')


def _get_raw_data(data_field: dict):
    """Returns the raw data from the data field specifications."""

    # Get the raw data of the chart
    if data_field.get('url'):  # Data is stored in a file
        with urllib.request.urlopen(data_field['url']) as response:  # Load the data
            data = response.read().decode()
    elif data_field.get('values'):  # Data is stored as the raw data
        data = data_field['values']
    else:  # Should never enter here
        raise RuntimeError('Something went wrong. Should never happen.')

    # Convert the raw data into a JSON object
    try:
        raw_data = json.loads(str(data).replace('\'', '\"'))  # Replace ' with " for syntaxis
    except json.decoder.JSONDecodeError:
        raise TypeError('Data is not a valid JSON string.')
    return raw_data


class BarChartCreator:
    """Bar chart creator class."""

    def __init__(self, chart_specs: dict):
        base_position = chart_specs.get('position', DEFAULT_CHART_POS)
        [self.base_x, self.base_y, self.base_z] = [float(pos) for pos in base_position.split()]  # Base position
        self.encoding = chart_specs.get('encoding')  # Encoding and parameters of the chart
        self.raw_data = _get_raw_data(chart_specs.get('data'))  # Raw data
        self.max_width = chart_specs.get('width', DEFAULT_BAR_CHART_WIDTH)  # Maximum width of the bar chart
        self.max_height = chart_specs.get('height', DEFAULT_BAR_CHART_HEIGHT)  # Maximum height of the bar chart
        self.max_depth = chart_specs.get('depth', DEFAULT_BAR_CHART_DEPTH)  # Depth of the bar chart

    def _set_bar_widths(self, data: list) -> list:
        """Sets the width of the bar chart."""

        return [self.max_width / len(data) for _ in range(len(data))]

    def _set_x_coordinates(self, data: list, bar_widths: list) -> list:
        """Returns a list of the x coordinates for each bar composing the bar chart."""

        x_coordinates = []
        for i in range(len(data)):
            x_coordinates.append((self.base_x + (bar_widths[i] / 2)) + (i * bar_widths[i]))
        return x_coordinates

    def _set_heights_of_bars(self, data: list) -> list:
        """Returns a list of the height for each bar composing the bar chart."""

        max_value = max(data)
        heights = [(h / max_value) * self.max_height for h in data]
        return heights

    def _set_y_coordinates(self, data: list, bar_heights: list) -> list:
        """Returns a list of the y coordinates for each bar composing the bar chart."""

        y_coordinates = []
        for i in range(len(data)):
            y_coordinates.append(self.base_y + (bar_heights[i] / 2))
        return y_coordinates

    @staticmethod
    def _set_bars_colors(data: list) -> list:
        """Returns a list of the color for each bar composing the bar chart."""

        colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
        bar_colors = [colors[c % len(colors)] for c in range(len(data))]
        return bar_colors

    def get_chart_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the bar chart."""

        elements_specs = []  # Will store the specifications for each element of the chart

        # X-axis
        field = self.encoding['x']['field']  # Field of the x-axis
        x_data = [d[field] for d in self.raw_data]

        bar_widths = self._set_bar_widths(x_data)  # Widths for each bar
        x_coordinates = self._set_x_coordinates(x_data, bar_widths)  # X-axis value for each bar

        # Y-axis
        field = self.encoding['y']['field']  # Field of the y-axis
        y_data = [d[field] for d in self.raw_data]

        bar_heights = self._set_heights_of_bars(y_data)
        y_coordinates = self._set_y_coordinates(y_data, bar_heights)

        # Z-axis
        z_coordinates = [self.base_z for _ in range(len(self.raw_data))]

        depths = [self.max_depth for _ in range(len(self.raw_data))]

        # Color
        colors = BarChartCreator._set_bars_colors(x_data)

        for elem in range(len(self.raw_data)):
            specs = {}  # Specifications of the single element
            specs.update({'pos': f'{x_coordinates[elem]} {y_coordinates[elem]} {z_coordinates[elem]}'})
            specs.update({'width': bar_widths[elem]})
            specs.update({'height': bar_heights[elem]})
            specs.update({'depth': depths[elem]})
            specs.update({'color': colors[elem]})
            elements_specs.append(specs)
        return elements_specs

    def get_axis_specs(self) -> tuple[str, float, float, float]:
        start = f'{self.base_x} {self.base_y} {self.base_z}'
        end_x = self.base_x + self.max_width
        end_y = self.base_y + self.max_height
        end_z = self.base_z + self.max_depth
        return start, end_x, end_y, end_z


class PointChartCreator:
    """Point chart creator class."""

    def __init__(self, chart_specs: dict):
        self.errase_this_variable = chart_specs  # TODO, self store important parameters for easier management

    def get_chart_specs(self) -> list[dict]:
        """
        Returns a list of dictionaries with the specifications (position, color, ...) for each element of the bar chart.
        One dictionary per element.
        """

        pass  # TODO

    def get_axis_specs(self) -> tuple[str, float, float, float]:
        pass  # TODO


""" PARA POINT, BUBBLE CHART O SCATTER PLOT
pos = f'{element.get('px', 0)} {element.get('py', 0)} {element.get('pz', 0)}'  # Default pos = '0 0 0'
radius = element.get('radius', 1)  # Default radius = 1
color = element.get('color', 'white')  # Default color = 'white'
elem_specs = {'pos': pos, 'radius': radius, 'color': color}
"""
