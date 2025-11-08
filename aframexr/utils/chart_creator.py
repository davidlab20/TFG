"""AframeXR chart creator"""

import json
import urllib.request


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

    def __init__(self):
        pass

    @staticmethod
    def _set_bar_width(data: list, max_width: float) -> float:
        return max_width / len(data)

    @staticmethod
    def _set_x_coordinates(data: list, base_x_pos: float, max_width: float) -> list:
        x_coordinates = []
        for i in range(len(data)):
            x_coordinates.append(base_x_pos + i * BarChartCreator._set_bar_width(data, max_width))  # Move each element in the axis
        return x_coordinates

    @staticmethod
    def _set_heights_of_bars(data: list, max_height: float) -> list:
        max_value = max(data)
        heights = [(h / max_value) * max_height for h in data]
        return heights

    @staticmethod
    def _set_bars_colors(data: list) -> list:
        colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
        bar_colors = [colors[c % len(colors)] for c in range(len(data))]
        return bar_colors

    @staticmethod
    def get_chart_specs(chart_specs: dict) -> list[dict]:
        """
        Returns a list of dictionaries with the specifications (position, color, ...) for each element of the bar chart.
        One dictionary per element.

        Parameters
        ----------
        chart_specs : dict
            Chart specifications.
        """

        # Important values (for easier management)
        base_position = chart_specs.get('position', '0 0 0')  # Base position of the chart
        encoding = chart_specs.get('encoding')  # Encoding and parameters of the chart
        raw_data = _get_raw_data(chart_specs.get('data'))  # Raw data
        max_width = chart_specs.get('width')  # Maximum width of the bar chart
        max_height = chart_specs.get('height')  # Maximum height of the bar chart
        max_depth = chart_specs.get('depth')  # Depth of the bar chart

        elements_specs = []  # Will store the specifications for each element of the chart

        # X-axis
        base_x_axis_pos = float(base_position.split()[0])
        field = encoding['x']['field']  # Field of the x-axis
        data = [d[field] for d in raw_data]
        x_coordinates = BarChartCreator._set_x_coordinates(data, base_x_axis_pos, max_width)

        # Y-axis
        base_y_pos = float(base_position.split()[1])
        y_coordinates = [base_y_pos for _ in range(len(raw_data))]

        # Z-axis
        base_z_pos = float(base_position.split()[2])
        z_coordinates = [base_z_pos for _ in range(len(raw_data))]

        # Width
        bar_width = BarChartCreator._set_bar_width(data, max_width)
        widths = [bar_width for _ in range(len(raw_data))]

        # Height
        field = encoding['y']['field']  # Field of the y-axis
        data = [d[field] for d in raw_data]
        heights = BarChartCreator._set_heights_of_bars(data, max_height)

        # Depth
        depths = [max_depth for _ in range(len(raw_data))]

        # Color
        colors = BarChartCreator._set_bars_colors(data)

        for elem in range(len(raw_data)):
            specs = {}  # Specifications of the single element
            specs.update({'pos': f'{x_coordinates[elem]} {y_coordinates[elem]} {z_coordinates[elem]}'})
            specs.update({'width': widths[elem]})  # Default width = 1
            specs.update({'height': heights[elem]})  # Default height = 1
            specs.update({'depth': depths[elem]})  # Default depth = 1
            specs.update({'color': colors[elem]})  # Default color = 'white'
            elements_specs.append(specs)
        return elements_specs


class PointChartCreator:
    """Point chart creator class."""

    def __init__(self):
        pass

    @staticmethod
    def get_chart_specs(raw_data: list[dict], encoding: dict, base_position: str) -> list[dict]:
        pass  # TODO


""" PARA POINT, BUBBLE CHART O SCATTER PLOT
pos = f'{element.get('px', 0)} {element.get('py', 0)} {element.get('pz', 0)}'  # Default pos = '0 0 0'
radius = element.get('radius', 1)  # Default radius = 1
color = element.get('color', 'white')  # Default color = 'white'
elem_specs = {'pos': pos, 'radius': radius, 'color': color}
"""
