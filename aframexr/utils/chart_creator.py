"""AframeXR chart creator"""

import json
import urllib.request

from aframexr.utils.defaults import *


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
    def get_axis_specs(chart_type: str, chart_specs: dict) -> tuple[str, float, float]:
        """Return the axis specifications of the chart type."""

        if chart_type == 'bar':
            return BarChartCreator(chart_specs).get_axis_specs()
        elif chart_type == 'point':
            return PointChartCreator(chart_specs).get_axis_specs()
        else:
            raise NotImplementedError(f'{chart_type} is not supported.')


class BarChartCreator:
    """Bar chart creator class."""

    def __init__(self, chart_specs: dict):
        base_position = chart_specs.get('position', DEFAULT_CHART_POS)
        [self.base_x, self.base_y, self.base_z] = [float(pos) for pos in base_position.split()]  # Base position
        self.encoding = chart_specs.get('encoding')  # Encoding and parameters of the chart
        self.raw_data = _get_raw_data(chart_specs.get('data'))  # Raw data
        self.max_width = chart_specs.get('width', DEFAULT_BAR_CHART_WIDTH)  # Maximum width of the bar chart
        self.max_height = chart_specs.get('height', DEFAULT_MAX_HEIGHT)  # Maximum height of the bar chart

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

        # Color
        colors = BarChartCreator._set_bars_colors(x_data)

        for elem in range(len(self.raw_data)):
            specs = {}  # Specifications of the single element
            specs.update({'pos': f'{x_coordinates[elem]} {y_coordinates[elem]} {z_coordinates[elem]}'})
            specs.update({'width': bar_widths[elem]})
            specs.update({'height': bar_heights[elem]})
            specs.update({'color': colors[elem]})
            elements_specs.append(specs)
        return elements_specs

    def get_axis_specs(self) -> tuple[str, float, float]:
        start = f'{self.base_x} {self.base_y} {self.base_z}'
        end_x = self.base_x + self.max_width
        end_y = self.base_y + self.max_height
        return start, end_x, end_y


class PointChartCreator:
    """Point chart creator class."""

    def __init__(self, chart_specs: dict):
        base_position = chart_specs.get('position', DEFAULT_CHART_POS)
        [self.base_x, self.base_y, self.base_z] = [float(pos) for pos in base_position.split()]  # Base position
        self.encoding = chart_specs.get('encoding')  # Encoding and parameters of the chart
        self.raw_data = _get_raw_data(chart_specs.get('data'))  # Raw data
        self.max_radius = chart_specs.get('max_radius', DEFAULT_POINT_RADIUS)

    def _set_point_radius(self, data: list) -> list:
        """Returns a list of the radius for each point composing the bar chart."""

        points_radius = []
        if self.encoding.get('color'):  # Scatter plot (all points same size)
            points_radius = [DEFAULT_POINT_RADIUS for _ in range(len(data))]
        if self.encoding.get('size'):  # Bubbles plot (each point size is proportional to the data value)
            max_value = max(data)
            points_radius = [(r / max_value) * self.max_radius for r in data]
        return points_radius

    def _set_x_coordinates(self, data: list, points_radius: list) -> list:
        """Returns a list of the x coordinates for each point composing the bar chart."""

        x_coordinates = []
        base_x = self.base_x + points_radius[0]  # Correct the position so the chart starts in the base position
        for i in range(len(data)):
            x_coordinates.append(base_x + (i * DEFAULT_POINT_X_SEPARATION))
        return x_coordinates

    def _set_y_coordinates(self, data: list, points_radius: list) -> list:
        """Returns a list of the y coordinates for each point composing the bar chart."""

        y_coordinates = []
        base_y = self.base_y + max(points_radius)  # The lower point starts in the base position

        # Proportional heights of the data
        max_value = max(data)
        heights = [(h / max_value) * DEFAULT_MAX_HEIGHT for h in data]

        for i in range(len(data)):
            y_coordinates.append(base_y + (heights[i] / 2))
        return y_coordinates

    @staticmethod
    def _set_points_radius(data: list) -> list:
        """Returns a list of the radius for each point composing the bubble chart."""

        max_value = max(data)
        points_radius = [(r / max_value) * DEFAULT_MAX_POINT_RADIUS for r in data]
        return points_radius

    def _set_points_colors(self, data: list) -> list:
        """Returns a list of the color for each point composing the scatter plot."""

        colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
        points_colors = []
        if self.encoding.get('color'):  # Scatter plot (same color for each type of point)
            types = list(set(data))  # Remove the duplicated values and convert into a list
            for t in data:
                index = types.index(t)  # Get the index of the type in types
                points_colors.append(colors[index % len(colors)])  # Add the color of the type
        return points_colors


    def get_chart_specs(self) -> list[dict]:
        """
        Returns a list of dictionaries with the specifications for each element of the point chart.
        One dictionary per element.
        """

        elements_specs = []

        # X-axis
        field = self.encoding['x']['field']
        x_data = [d[field] for d in self.raw_data]

        if self.encoding.get('size'):  # Bubbles plot (the size of the point depends on the value of the field)
            field = self.encoding['size']['field']
            size_data = [s[field] for s in self.raw_data]
            radius = self._set_points_radius(size_data)
        else:  # Scatter plot (same radius for all points)
            radius = [DEFAULT_POINT_RADIUS for _ in range(len(self.raw_data))]

        x_coordinates = self._set_x_coordinates(x_data, radius)

        # Y-axis
        field = self.encoding['y']['field']  # Field of the y-axis
        y_data = [d[field] for d in self.raw_data]

        y_coordinates = self._set_y_coordinates(y_data, radius)

        # Z-axis
        z_coordinates = [self.base_z for _ in range(len(self.raw_data))]

        # Color
        if self.encoding.get('color'):  # Scatter plot (same color for each type of point)
            field = self.encoding['color']['field']
            color_data = [c[field] for c in self.raw_data]
            colors = self._set_points_colors(color_data)
        else:  # Bubbles plot (same color for all points)
            colors = [DEFAULT_POINT_COLOR for _ in range(len(self.raw_data))]

        for elem in range(len(self.raw_data)):
            specs = {}  # Specifications of the single element
            specs.update({'pos': f'{x_coordinates[elem]} {y_coordinates[elem]} {z_coordinates[elem]}'})
            specs.update({'radius': radius[elem]})
            specs.update({'color': colors[elem]})
            elements_specs.append(specs)
        return elements_specs

    def get_axis_specs(self) -> tuple[str, float, float]:
        start = f'{self.base_x} {self.base_y} {self.base_z}'
        end_x = self.base_x + (len(self.raw_data) * DEFAULT_POINT_X_SEPARATION)
        end_y = self.base_y + DEFAULT_MAX_HEIGHT
        return start, end_x, end_y
