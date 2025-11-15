"""AframeXR chart creator"""

import json
import urllib.request, urllib.error

from aframexr.api.filters import FilterTransform
from aframexr.utils.constants import *


def _get_raw_data(data_field: dict, transform_field: dict | None) -> list[dict]:
    """Returns the raw data from the data field specifications, transformed if necessary."""

    # Get the raw data of the chart
    if data_field.get('url'):  # Data is stored in a file
        try:
            with urllib.request.urlopen(data_field['url']) as response:  # Load the data
                data = response.read().decode()
        except urllib.error.URLError:
            raise IOError(f'Could not load data from URL: {data_field['url']}')
    elif data_field.get('values'):  # Data is stored as the raw data
        data = data_field['values']
    else:  # Should never enter here
        raise RuntimeError('Something went wrong. Should never happen.')

    # Convert the raw data into a JSON object
    try:
        raw_data = json.loads(str(data).replace('\'', '\"'))  # Replace ' with " for syntaxis
    except json.decoder.JSONDecodeError:
        raise TypeError('Data is not a valid JSON string.')

    # Transform data (if necessary)
    if transform_field:
        for transformation in transform_field:
            if transformation.get('filter'):
                filter_object = FilterTransform.from_string(transformation['filter'])
                filtered_data = filter_object.filter_data(raw_data)
                raw_data = filtered_data
            else:
                raise NotImplementedError(f'The transformation {transformation} has not been implemented yet.')

    return raw_data


class ChartCreator:
    """Chart creator base class"""

    def __init__(self, chart_specs: dict):
        base_position = chart_specs.get('position', DEFAULT_CHART_POS)
        [self.base_x, self.base_y, self.base_z] = [float(pos) for pos in base_position.split()]  # Base position
        self.encoding = chart_specs.get('encoding')  # Encoding and parameters of the chart
        self.raw_data = _get_raw_data(chart_specs.get('data'), chart_specs.get('transform'))  # Raw data

    @staticmethod
    def get_elements_specs(chart_type: str, chart_specs: dict) -> list[dict]:
        """Return the chart specifications of the chart type."""

        if chart_type == 'arc':
            return ArcChartCreator(chart_specs).get_chart_specs()
        elif chart_type == 'bar':
            return BarChartCreator(chart_specs).get_chart_specs()
        elif chart_type == 'point':
            return PointChartCreator(chart_specs).get_chart_specs()
        else:
            raise NotImplementedError(f'{chart_type} is not supported.')

    @staticmethod
    def get_x_axis_specs(chart_type: str, chart_specs: dict) -> tuple[None, None] | tuple[str, str]:
        """Return the x-axis specifications of the chart type."""

        if chart_type == 'arc':
            return None, None  # Pie chart and doughnut chart have no axis
        elif chart_type == 'bar':
            return BarChartCreator(chart_specs).x_axis_specs()
        elif chart_type == 'point':
            return PointChartCreator(chart_specs).x_axis_specs()
        else:
            raise NotImplementedError(f'{chart_type} is not supported.')

    @staticmethod
    def get_y_axis_specs(chart_type: str, chart_specs: dict) -> tuple[None, None] | tuple[str, str]:
        """Return the y-axis specifications of the chart type."""

        if chart_type == 'arc':
            return None, None  # Pie chart and doughnut chart have no axis
        elif chart_type == 'bar':
            return BarChartCreator(chart_specs).y_axis_specs()
        elif chart_type == 'point':
            return PointChartCreator(chart_specs).y_axis_specs()
        else:
            raise NotImplementedError(f'{chart_type} is not supported.')


class ArcChartCreator(ChartCreator):
    """Arc chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self.radius = chart_specs['mark'].get('outerRadius', DEFAULT_PIE_RADIUS)  # Outer radius of the chart
        self.inner_radius = chart_specs['mark'].get('innerRadius', DEFAULT_PIE_INNER_RADIUS)  # Inner radius of the chart

    @staticmethod
    def _set_elements_theta(data: list) -> tuple[list, list]:
        """Returns a tuple with a list storing the theta start of each element, and another storing the theta length."""

        theta_start = []
        theta_length = []
        for i in range(len(data)):
            if i == 0:
                theta_start.append(0)  # The first element starts in theta = 0
            else:
                theta_start.append(theta_start[i - 1] + theta_length[i - 1])  # Start where the previous ended
            theta_length.append((data[i] / sum(data)) * 360)  # Theta length in degrees
        return theta_start, theta_length

    @staticmethod
    def _set_elements_colors(data: list) -> list:
        """Returns a list of the color for each element composing the chart."""

        element_colors = [AVAILABLE_COLORS[c % len(AVAILABLE_COLORS)] for c in range(len(data))]
        return element_colors

    def get_chart_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        elements_specs = []

        # Axis
        x_coordinates = [self.base_x for _ in range(len(self.raw_data))]
        y_coordinates = [self.base_y for _ in range(len(self.raw_data))]
        z_coordinates = [self.base_z for _ in range(len(self.raw_data))]

        # Radius
        inners_radius = [self.inner_radius for _ in range(len(self.raw_data))]
        outers_radius = [self.radius for _ in range(len(self.raw_data))]

        # Theta
        field = self.encoding['theta']['field']
        theta_data = [d[field] for d in self.raw_data]
        theta_starts, theta_lengths = self._set_elements_theta(theta_data)

        # Color
        field = self.encoding['color']['field']
        color_data = [d[field] for d in self.raw_data]
        colors = self._set_elements_colors(color_data)

        for elem in range(len(self.raw_data)):
            specs = {}  # Specifications of the single element
            specs.update({'pos': f'{x_coordinates[elem]} {y_coordinates[elem]} {z_coordinates[elem]}'})
            specs.update({'inner_radius': inners_radius[elem]})
            specs.update({'outer_radius': outers_radius[elem]})
            specs.update({'theta_start': theta_starts[elem]})
            specs.update({'theta_length': theta_lengths[elem]})
            specs.update({'color': colors[elem]})
            elements_specs.append(specs)
        return elements_specs


class BarChartCreator(ChartCreator):
    """Bar chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self.bar_width = chart_specs['mark'].get('width', DEFAULT_BAR_WIDTH)  # Width of the bar
        self.max_height = chart_specs.get('height', DEFAULT_MAX_HEIGHT)  # Maximum height of the bar chart

    def _set_x_coordinates(self, data: list) -> list:
        """Returns a list of the x coordinates for each bar composing the bar chart."""

        x_coordinates = []
        for i in range(len(data)):
            x_coordinates.append((self.base_x + (self.bar_width / 2)) + (i * self.bar_width))
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

        bar_colors = [AVAILABLE_COLORS[c % len(AVAILABLE_COLORS)] for c in range(len(data))]
        return bar_colors

    def get_chart_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the bar chart."""

        elements_specs = []

        # X-axis
        field = self.encoding['x']['field']  # Field of the x-axis
        x_data = [d[field] for d in self.raw_data]

        bar_widths = [self.bar_width for _ in range(len(self.raw_data))]  # Widths for each bar
        x_coordinates = self._set_x_coordinates(x_data)  # X-axis value for each bar

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

    def x_axis_specs(self) -> tuple[str, str]:
        start = None
        end = None
        display_axis = True
        try:
            display_axis = self.encoding['x']['axis']
        except KeyError or display_axis is True:  # Display axis if key not found (default display axis) or True
            start = f'{self.base_x} {self.base_y} {self.base_z}'
            end_x = self.base_x + (self.bar_width * len(self.raw_data))
            end = f'{end_x} {self.base_y} {self.base_z}'
        return start, end

    def y_axis_specs(self) -> tuple[str, str]:
        start = None
        end = None
        display_axis = True
        try:
            display_axis = self.encoding['y']['axis']
        except KeyError or display_axis is True:  # Display axis if key not found (default display axis) or True
            start = f'{self.base_x} {self.base_y} {self.base_z}'
            end_y = self.base_y + self.max_height
            end = f'{self.base_x} {end_y} {self.base_z}'
        return start, end


class PointChartCreator(ChartCreator):
    """Point chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self.max_radius = chart_specs['mark'].get('max_radius', DEFAULT_POINT_RADIUS)

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

    def _set_points_radius(self, data: list) -> list:
        """Returns a list of the radius for each point composing the bubble chart."""

        max_value = max(data)
        points_radius = [(r / max_value) * self.max_radius for r in data]
        return points_radius

    def _set_points_colors(self, data: list) -> list:
        """Returns a list of the color for each point composing the scatter plot."""

        points_colors = []
        if self.encoding.get('color'):  # Scatter plot (same color for each type of point)
            types = list(set(data))  # Remove the duplicated values and convert into a list
            for t in data:
                index = types.index(t)  # Get the index of the type in types
                points_colors.append(AVAILABLE_COLORS[index % len(AVAILABLE_COLORS)])  # Add the color of the type
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

    def x_axis_specs(self) -> tuple[str, str]:
        start = None
        end = None
        display_axis = True
        try:
            display_axis = self.encoding['x']['axis']
        except KeyError or display_axis is True:  # Display axis if key not found (default display axis) or True
            start = f'{self.base_x} {self.base_y} {self.base_z}'
            end_x = self.base_x + (len(self.raw_data) * DEFAULT_POINT_X_SEPARATION) + self.max_radius
            end = f'{end_x} {self.base_y} {self.base_z}'
        return start, end

    def y_axis_specs(self) -> tuple[str, str]:
        start = None
        end = None
        display_axis = True
        try:
            display_axis = self.encoding['y']['axis']
        except KeyError or display_axis is True:  # Display axis if key not found (default display axis) or True
            start = f'{self.base_x} {self.base_y} {self.base_z}'
            end_y = self.base_y + DEFAULT_MAX_HEIGHT
            end = f'{self.base_x} {end_y} {self.base_z}'
        return start, end
