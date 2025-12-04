"""AframeXR entity creator"""

import copy
import json
import os
import urllib.request, urllib.error
import warnings

from aframexr.api.aggregate import *
from aframexr.api.filters import FilterTransform
from aframexr.utils.constants import *


AXIS_DICT_TEMPLATE = {'start': None, 'end': None, 'labels_pos': [], 'labels_values': [], 'labels_rotation': ''}
"""Axis dictionary template for chart creation."""

GROUP_DICT_TEMPLATE = {'pos': '', 'rotation': ''}
"""Group dictionary template for group base specifications creation."""


def _get_raw_data(data_field: dict, transform_field: dict | None) -> list[dict]:
    """Returns the raw data from the data field specifications, transformed if necessary."""

    # Get the raw data of the chart
    if data_field.get('url'):  # Data is stored in a file
        try:
            if data_field['url'].startswith('http'):  # Load data as URL
                with urllib.request.urlopen(data_field['url']) as response:
                    data = response.read().decode()
            else:
                absolute_path = os.path.normpath(data_field['url'])
                with open(absolute_path, 'r') as f:
                    data = f.read()
        except urllib.error.URLError:
            raise IOError(f'Could not load data from URL: {data_field['url']}.')
        except FileNotFoundError:
            raise IOError(f'Could not find local file: {data_field['url']}.')
        except IOError as e:
            raise IOError(f'Could not load data from local file: {data_field['url']}. Error: {e}.')
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
                filtered_data = filter_object.get_filtered_data(raw_data)
                if len(filtered_data) == 0:  # Data does not contain any value for the filter
                    warnings.warn(f'Data does not contain any value for the filter: {transformation["filter"]}.')
                raw_data = filtered_data
            else:
                raise ValueError(f'Invalid transformation filter: {transformation["filter"]}.')

    return raw_data


class ChartCreator:
    """Chart creator base class"""

    def __init__(self, chart_specs: dict):
        base_position = chart_specs.get('position', DEFAULT_CHART_POS)
        [self._base_x, self._base_y, self._base_z] = [float(pos) for pos in base_position.split()]  # Base position
        self._encoding = chart_specs.get('encoding')  # Encoding and parameters of the chart
        if chart_specs['mark']['type'] in CHART_TEMPLATES:
            self._raw_data = _get_raw_data(chart_specs['data'], chart_specs.get('transform'))  # Raw data
        if chart_specs['mark']['type'] in IMAGES_TEMPLATES:
            self._url = chart_specs['data']['url']  # URL of the image model
        rotation = chart_specs.get('rotation', DEFAULT_CHART_ROTATION)  # Rotation of the chart
        [self._x_rotation, self._y_rotation, self._z_rotation] = [float(rot) for rot in rotation.split()]

    @staticmethod
    def create_object(chart_type: str, chart_specs: dict):
        """Returns a ChartCreator instance of the specific chart type."""

        if chart_type == 'arc':
            return ArcChartCreator(chart_specs)
        elif chart_type == 'bar':
            return BarChartCreator(chart_specs)
        elif chart_type == 'point':
            return PointChartCreator(chart_specs)
        elif chart_type == 'image':
            return ImageCreator(chart_specs)
        elif chart_type == 'gltf':
            return GLTFModelCreator(chart_specs)
        else:
            raise ValueError(f'Invalid chart type: {chart_type}.')


class ArcChartCreator(ChartCreator):
    """Arc chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._radius = chart_specs['mark'].get('radius', DEFAULT_PIE_RADIUS)  # Radius
        self._set_rotation()

    def _set_rotation(self):
        """Sets the rotation of the pie chart."""

        pie_rotation = DEFAULT_PIE_ROTATION.split()
        final_pie_rotation_x = float(self._x_rotation) + float(pie_rotation[0])
        final_pie_rotation_y = float(self._y_rotation) + float(pie_rotation[1])
        final_pie_rotation_z = float(self._z_rotation) + float(pie_rotation[2])
        self._rotation = f'{final_pie_rotation_x} {final_pie_rotation_y} {final_pie_rotation_z}'

    def get_group_specs(self) -> dict:
        """Returns a dictionary with the base specifications for the group of elements."""

        group_specs = copy.deepcopy(GROUP_DICT_TEMPLATE)
        group_specs.update({'pos': f'{self._base_x} {self._base_y} {self._base_z}', 'rotation': self._rotation})
        return group_specs

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

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        if len(self._raw_data) == 0:  # There is no data to display
            return []

        elements_specs = []

        # Axis
        x_coordinates = [0 for _ in range(len(self._raw_data))]
        y_coordinates = [0 for _ in range(len(self._raw_data))]
        z_coordinates = [0 for _ in range(len(self._raw_data))]

        # Radius
        radius = [self._radius for _ in range(len(self._raw_data))]

        # Theta
        field = self._encoding['theta']['field']
        theta_data = [d[field] for d in self._raw_data]
        theta_starts, theta_lengths = self._set_elements_theta(theta_data)

        # Color
        field = self._encoding['color']['field']
        color_data = [d[field] for d in self._raw_data]
        colors = self._set_elements_colors(color_data)

        # Id
        ids = []
        for i in range(len(self._raw_data)):
            label = color_data[i]
            value = int(theta_data[i]) if str(theta_data[i]).endswith('.0') else theta_data[i]
            ids.append(f'{label}: {value}')

        for elem in range(len(self._raw_data)):
            specs = {}  # Specifications of the single element
            specs.update({'id': ids[elem]})
            specs.update({'pos': f'{x_coordinates[elem]} {y_coordinates[elem]} {z_coordinates[elem]}'})
            specs.update({'radius': radius[elem]})
            specs.update({'theta_start': theta_starts[elem]})
            specs.update({'theta_length': theta_lengths[elem]})
            specs.update({'color': colors[elem]})
            elements_specs.append(specs)
        return elements_specs

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = {'x': copy.deepcopy(AXIS_DICT_TEMPLATE), 'y': copy.deepcopy(AXIS_DICT_TEMPLATE),
                      'z': copy.deepcopy(AXIS_DICT_TEMPLATE)}
        return axis_specs  # Arc chart have no axis


class BarChartCreator(ChartCreator):
    """Bar chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self.bar_width = chart_specs['mark'].get('width', DEFAULT_BAR_WIDTH)  # Width of the bar
        self.max_height = chart_specs.get('height', DEFAULT_MAX_HEIGHT)  # Maximum height of the bar chart

    def get_group_specs(self) -> dict:
        """Returns a dictionary with the base specifications for the group of elements."""

        group_specs = copy.deepcopy(GROUP_DICT_TEMPLATE)
        group_specs.update({'pos': f'{self._base_x} {self._base_y} {self._base_z}',
                            'rotation': f'{self._x_rotation} {self._y_rotation} {self._z_rotation}'})
        return group_specs

    def _recalculate_x_coordinates(self, aggregate_function: str, x_field: str) -> list:
        """Recalculate the x coordinates for each bar composing the bar chart."""

        if not x_field:
            raise ValueError('Aggregate can only be used having data for the x-axis.')
        aggregate_object = AggregatedFieldDef.from_string()

    def _set_bars_colors(self) -> list:
        """Returns a list of the color for each bar composing the bar chart."""

        bar_colors = [AVAILABLE_COLORS[c % len(AVAILABLE_COLORS)] for c in range(len(self._raw_data))]
        return bar_colors

    def _set_bars_heights(self, data: list | None) -> list:
        """Returns a list of the height for each bar composing the bar chart."""

        if data is None:
            heights = [DEFAULT_BAR_HEIGHT_WHEN_NO_Y_AXIS for _ in range(len(self._raw_data))]
        else:
            max_value = max(data)
            heights = [(h / max_value) * self.max_height for h in data]
        return heights

    def _set_x_coordinates(self, data: list | None) -> list:
        """Returns a list of the x coordinates for each bar composing the bar chart."""

        x_coordinates = []
        relative_x_start = self.bar_width / 2

        if data is None:  # No field for x-axis
            x_coordinates = [relative_x_start for _ in range(len(self._raw_data))]
        else:  # Field for x-axis
            for element in range(len(data)):
                x_coordinates.append(relative_x_start + element * self.bar_width)
        return x_coordinates

    def _set_y_coordinates(self, bar_heights: list) -> list:
        """Returns a list of the y coordinates for each bar composing the bar chart."""

        y_coordinates = []
        for i in range(len(self._raw_data)):
            y_coordinates.append(bar_heights[i] / 2)
        return y_coordinates

    def _set_z_coordinates(self, data: list | None) -> list:
        """Returns a list of the z coordinates for each bar composing the bar chart."""

        z_coordinates = []
        relative_z_start = - DEFAULT_BAR_DEPTH / 2

        if data is None:
            z_coordinates = [relative_z_start for _ in range(len(self._raw_data))]
        else:
            types = list(set(data))  # Remove the duplicated values and convert into a list
            for t in data:
                index = types.index(t)  # Get the index of the type in types
                elem_z = relative_z_start - (index * DEFAULT_MAX_DEPTH / len(types))
                z_coordinates.append(elem_z)  # Add the z_coordinate
        return z_coordinates

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        if len(self._raw_data) == 0:  # There is no data to display
            return []

        elements_specs = []

        # X-axis
        x_data = None
        x_field = None

        if self._encoding.get('x'):
            x_field = self._encoding['x']['field']  # Field of the x-axis
            x_data = [d[x_field] for d in self._raw_data]

        bar_widths = [self.bar_width for _ in range(len(self._raw_data))]  # Widths for each bar
        x_coordinates = self._set_x_coordinates(x_data)  # X-axis value for each bar


        # Y-axis
        y_data = None

        if self._encoding.get('y'):
            y_field = self._encoding['y']['field']  # Field of the y-axis
            y_aggregate = self._encoding['y'].get('aggregate')
            if y_aggregate:
                x_coordinates = self._recalculate_x_coordinates(y_aggregate, x_field)
            y_data = [d[y_field] for d in self._raw_data]

        bar_heights = self._set_bars_heights(y_data)
        y_coordinates = self._set_y_coordinates(bar_heights)

        # Z-axis
        z_data = None

        if self._encoding.get('z'):
            z_field = self._encoding['z']['field']  # Field of the z-axis
            z_data = [d[z_field] for d in self._raw_data]

        z_coordinates = self._set_z_coordinates(z_data)

        # Color
        colors = self._set_bars_colors()

        # Id
        ids = []
        for i in range(len(self._raw_data)):
            values = []
            if x_data:
                values.append(str(x_data[i]))
            if y_data:
                values.append(str(y_data[i]))
            if z_data:
                values.append(str(z_data[i]))

            elem_id = ' : '.join(values)
            ids.append(elem_id)

        for elem in range(len(self._raw_data)):
            specs = {}  # Specifications of the single element
            specs.update({'id': ids[elem]})
            specs.update({'pos': f'{x_coordinates[elem]} {y_coordinates[elem]} {z_coordinates[elem]}'})
            specs.update({'width': bar_widths[elem]})
            specs.update({'height': bar_heights[elem]})
            specs.update({'color': colors[elem]})
            elements_specs.append(specs)
        return elements_specs

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = {'x': copy.deepcopy(AXIS_DICT_TEMPLATE), 'y': copy.deepcopy(AXIS_DICT_TEMPLATE),
                      'z': copy.deepcopy(AXIS_DICT_TEMPLATE)}
        if len(self._raw_data) == 0:  # There is no data to display
            return axis_specs

        # ---- X-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['x']['axis'] if self._encoding.get('x') else False
        except KeyError or display_axis is True:  # Display axis if key 'axis' not found (default display axis) or True
            start = '0 0 0'
            end = f'{self.bar_width * len(self._raw_data)} 0 0'

            axis_specs['x']['start'] = start
            axis_specs['x']['end'] = end

        # Axis labels
            x_field = self._encoding['x']['field']  # Field of the x-axis
            x_data = [d[x_field] for d in self._raw_data]
            x_coordinates = self._set_x_coordinates(x_data)  # X-axis value for each bar

            for label in range(len(self._raw_data)):
                label_pos = f'{x_coordinates[label]} {LABELS_Y_DELTA} {LABELS_Z_DELTA}'
                label_value = x_data[label]
                axis_specs['x']['labels_pos'].append(label_pos)
                axis_specs['x']['labels_values'].append(label_value)
            axis_specs['x']['labels_rotation'] = '-90 0 -90'  # Rotation of the labels

        # ---- Y-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['y']['axis'] if self._encoding.get('y') else False
        except KeyError or display_axis is True:  # Display axis if key 'axis' not found (default display axis) or True
            start = '0 0 0'
            end = f'0 {self.max_height} 0'

            axis_specs['y']['start'] = start
            axis_specs['y']['end'] = end

        # Axis labels
            y_field = self._encoding['y']['field']  # Field of the y-axis
            y_data = [d[y_field] for d in self._raw_data]

            for label in range(1, Y_NUM_OF_TICKS + 1):
                label_pos = f'{Y_LABELS_X_DELTA} {self.max_height * label / Y_NUM_OF_TICKS} 0'
                label_value = max(y_data) * label / Y_NUM_OF_TICKS
                axis_specs['y']['labels_pos'].append(label_pos)
                axis_specs['y']['labels_values'].append(label_value)
            axis_specs['y']['labels_rotation'] = '0 0 0'  # Rotation of the labels

        # ---- Z-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['z']['axis'] if self._encoding.get('z') else False
        except KeyError or display_axis is True:  # Display axis if key 'axis' not found (default display axis) or True
            start = f'0 0 0'
            end = f'0 0 {-DEFAULT_MAX_DEPTH}'

            axis_specs['z']['start'] = start
            axis_specs['z']['end'] = end

        # Axis labels
            z_field = self._encoding['z']['field']  # Field of the z-axis
            z_data = [d[z_field] for d in self._raw_data]
            types = list(set(z_data))  # Remove the duplicated values and convert into a list

            for label in types:
                label_z_pos = - (DEFAULT_BAR_DEPTH / 2) - (types.index(label) * DEFAULT_MAX_DEPTH / len(types))
                label_pos = f'{Z_LABELS_X_DELTA} {LABELS_Y_DELTA} {label_z_pos}'
                label_value = label
                axis_specs['z']['labels_pos'].append(label_pos)
                axis_specs['z']['labels_values'].append(label_value)
            axis_specs['z']['labels_rotation'] = '-90 0 0'

        return axis_specs


class GLTFModelCreator(ChartCreator):
    """GLTF model creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._scale = chart_specs['mark'].get('scale', DEFAULT_GLTF_SCALE)

    def get_group_specs(self) -> dict:
        """Returns a dictionary with the base specifications for the group of elements."""

        group_specs = copy.deepcopy(GROUP_DICT_TEMPLATE)
        group_specs.update({'pos': f'{self._base_x} {self._base_y} {self._base_z}',
                            'rotation': f'{self._x_rotation} {self._y_rotation} {self._z_rotation}'})
        return group_specs

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        return [{'src': self._url, 'scale': self._scale}]

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = {'x': copy.deepcopy(AXIS_DICT_TEMPLATE), 'y': copy.deepcopy(AXIS_DICT_TEMPLATE),
                      'z': copy.deepcopy(AXIS_DICT_TEMPLATE)}
        return axis_specs  # GLTF models have no axis


class ImageCreator(ChartCreator):
    """Image creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._height = chart_specs['mark'].get('height', DEFAULT_IMAGE_HEIGHT)
        self._width = chart_specs['mark'].get('width', DEFAULT_IMAGE_WIDTH)

    def get_group_specs(self) -> dict:
        """Returns a dictionary with the base specifications for the group of elements."""

        group_specs = copy.deepcopy(GROUP_DICT_TEMPLATE)
        group_specs.update({'pos': f'{self._base_x} {self._base_y} {self._base_z}',
                            'rotation': f'{self._x_rotation} {self._y_rotation} {self._z_rotation}'})
        return group_specs

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        return [{'src': self._url, 'width': self._width, 'height': self._height}]

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = {'x': copy.deepcopy(AXIS_DICT_TEMPLATE), 'y': copy.deepcopy(AXIS_DICT_TEMPLATE),
                      'z': copy.deepcopy(AXIS_DICT_TEMPLATE)}
        return axis_specs  # Images have no axis



class PointChartCreator(ChartCreator):
    """Point chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._max_radius = chart_specs['mark'].get('max_radius', DEFAULT_POINT_RADIUS)

    def get_group_specs(self) -> dict:
        """Returns a dictionary with the base specifications for the group of elements."""

        group_specs = copy.deepcopy(GROUP_DICT_TEMPLATE)
        group_specs.update({'pos': f'{self._base_x} {self._base_y} {self._base_z}',
                            'rotation': f'{self._x_rotation} {self._y_rotation} {self._z_rotation}'})
        return group_specs

    def _set_points_colors(self, data: list) -> list:
        """Returns a list of the color for each point composing the scatter plot."""

        points_colors = []
        if self._encoding.get('color'):  # Scatter plot (same color for each type of point)
            types = list(set(data))  # Remove the duplicated values and convert into a list
            for t in data:
                index = types.index(t)  # Get the index of the type in types
                points_colors.append(AVAILABLE_COLORS[index % len(AVAILABLE_COLORS)])  # Add the color of the type
        return points_colors

    def _set_points_radius(self, data: list) -> list:
        """Returns a list of the radius for each point composing the bubble chart."""

        max_value = max(data)
        points_radius = [(r / max_value) * self._max_radius for r in data]
        return points_radius

    def _set_x_coordinates(self, data: list | None, points_radius: list) -> list:
        """Returns a list of the x coordinates for each point composing the bar chart."""

        x_coordinates = []
        base_x = points_radius[0]  # Correct the position so the chart starts in the base position
        if data is None:
            x_coordinates = [base_x for _ in range(len(self._raw_data))]
        for i in range(len(self._raw_data)):
            x_coordinates.append(base_x + (i * DEFAULT_POINT_X_SEPARATION))
        return x_coordinates

    def _set_y_coordinates(self, data: list | None, points_radius: list) -> list:
        """Returns a list of the y coordinates for each point composing the bar chart."""

        y_coordinates = []
        base_y = max(points_radius)  # The lower point starts in the base position

        if data is None:
            y_coordinates = [base_y for _ in range(len(self._raw_data))]
        else:
            max_value = max(data)  # Proportional heights of the data
            heights = [(h / max_value) * DEFAULT_MAX_HEIGHT for h in data]

            for i in range(len(data)):
                y_coordinates.append(base_y + heights[i] - points_radius[i])
        return y_coordinates

    def _set_z_coordinates(self, data: list | None) -> list:
        """Returns a list of the z coordinates for each bar composing the bar chart."""

        z_coordinates = []

        if data is None:
            z_coordinates = [0 for _ in range(len(self._raw_data))]
        else:
            types = list(set(data))  # Remove the duplicated values and convert into a list
            base_z = DEFAULT_POINT_RADIUS
            for t in data:
                index = types.index(t)  # Get the index of the type in types
                elem_z = -base_z - (index * DEFAULT_MAX_DEPTH / len(types))
                z_coordinates.append(elem_z)  # Add the z_coordinate
        return z_coordinates

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        if len(self._raw_data) == 0:  # There is no data to display
            return []

        elements_specs = []

        # X-axis
        x_data = None
        radius = [self._max_radius for _ in range(len(self._raw_data))]

        if self._encoding.get('x'):
            x_field = self._encoding['x']['field']
            x_data = [d[x_field] for d in self._raw_data]

            if self._encoding.get('size'):  # Bubbles plot (the size of the point depends on the value of the field)
                size_field = self._encoding['size']['field']
                size_data = [s[size_field] for s in self._raw_data]
                radius = self._set_points_radius(size_data)
            else:  # Scatter plot (same radius for all points)
                pass

        x_coordinates = self._set_x_coordinates(x_data, radius)

        # Y-axis
        y_data = None

        if self._encoding.get('y'):
            y_field = self._encoding['y']['field']  # Field of the y-axis
            y_data = [d[y_field] for d in self._raw_data]

        y_coordinates = self._set_y_coordinates(y_data, radius)

        # Z-axis
        z_data = None

        if self._encoding.get('z'):
            z_field = self._encoding['z']['field']  # Field of the z-axis
            z_data = [d[z_field] for d in self._raw_data]

        z_coordinates = self._set_z_coordinates(z_data)

        # Color
        if self._encoding.get('color'):  # Scatter plot (same color for each type of point)
            color_field = self._encoding['color']['field']
            color_data = [c[color_field] for c in self._raw_data]
            colors = self._set_points_colors(color_data)
        else:  # Bubbles plot (same color for all points)
            colors = [DEFAULT_POINT_COLOR for _ in range(len(self._raw_data))]

        # Id
        ids = []
        for i in range(len(self._raw_data)):
            values = []
            if x_data:
                values.append(str(x_data[i]))
            if y_data:
                values.append(str(y_data[i]))
            if z_data:
                values.append(str(z_data[i]))

            elem_id = ' : '.join(values)
            ids.append(elem_id)

        for elem in range(len(self._raw_data)):
            specs = {}  # Specifications of the single element
            specs.update({'id': ids[elem]})
            specs.update({'pos': f'{x_coordinates[elem]} {y_coordinates[elem]} {z_coordinates[elem]}'})
            specs.update({'radius': radius[elem]})
            specs.update({'color': colors[elem]})
            elements_specs.append(specs)
        return elements_specs

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = {'x': copy.deepcopy(AXIS_DICT_TEMPLATE), 'y': copy.deepcopy(AXIS_DICT_TEMPLATE),
                      'z': copy.deepcopy(AXIS_DICT_TEMPLATE)}
        if len(self._raw_data) == 0:  # There is no data to display
            return axis_specs

        # ---- X-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['x']['axis'] if self._encoding.get('x') else False
        except KeyError or display_axis is True:  # Display axis if key not found (default display axis) or True
            start = '0 0 0'
            end = f'{DEFAULT_POINT_X_SEPARATION * len(self._raw_data) + self._max_radius} 0 0'

            axis_specs['x']['start'] = start
            axis_specs['x']['end'] = end

        # Axis labels
            x_field = self._encoding['x']['field']
            x_data = [d[x_field] for d in self._raw_data]

            if self._encoding.get('size'):  # Bubbles plot (the size of the point depends on the value of the field)
                size_field = self._encoding['size']['field']
                size_data = [s[size_field] for s in self._raw_data]
                radius = self._set_points_radius(size_data)
            else:  # Scatter plot (same radius for all points)
                radius = [DEFAULT_POINT_RADIUS for _ in range(len(self._raw_data))]
            x_coordinates = self._set_x_coordinates(x_data, radius)

            for label in range(len(self._raw_data)):
                label_pos = f'{x_coordinates[label]} {LABELS_Y_DELTA} {LABELS_Z_DELTA}'
                label_value = self._raw_data[label][self._encoding['x']['field']]
                axis_specs['x']['labels_pos'].append(label_pos)
                axis_specs['x']['labels_values'].append(label_value)
            axis_specs['x']['labels_rotation'] = '-90 0 -90'  # Rotation of the labels

        # ---- Y-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['y']['axis'] if self._encoding.get('y') else False
        except KeyError or display_axis is True:  # Display axis if key not found (default display axis) or True
            start = '0 0 0'
            end = f'0 {DEFAULT_MAX_HEIGHT} 0'

            axis_specs['y']['start'] = start
            axis_specs['y']['end'] = end

        # Axis labels
            y_field = self._encoding['y']['field']  # Field of the y-axis
            y_data = [d[y_field] for d in self._raw_data]

            for label in range(1, Y_NUM_OF_TICKS + 1):
                label_pos = f'{Y_LABELS_X_DELTA} {DEFAULT_MAX_HEIGHT * label / Y_NUM_OF_TICKS} 0'
                label_value = max(y_data) * label / Y_NUM_OF_TICKS
                axis_specs['y']['labels_pos'].append(label_pos)
                axis_specs['y']['labels_values'].append(label_value)
            axis_specs['y']['labels_rotation'] = '0 0 0'

        # ---- Z-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['z']['axis'] if self._encoding.get('z') else False
        except KeyError or display_axis is True:  # Display axis if key 'axis' not found (default display axis) or True
            start = '0 0 0'
            end = f'0 0 {-DEFAULT_MAX_DEPTH}'

            axis_specs['z']['start'] = start
            axis_specs['z']['end'] = end

        # Axis labels
            z_field = self._encoding['z']['field']  # Field of the z-axis
            z_data = [d[z_field] for d in self._raw_data]
            types = list(set(z_data))  # Remove the duplicated values and convert into a list

            for label in types:
                label_z_pos = - (DEFAULT_POINT_RADIUS / 2) - (types.index(label) * DEFAULT_MAX_DEPTH / len(types))
                label_pos = f'{Z_LABELS_X_DELTA} {LABELS_Y_DELTA} {label_z_pos}'
                label_value = label
                axis_specs['z']['labels_pos'].append(label_pos)
                axis_specs['z']['labels_values'].append(label_value)
            axis_specs['z']['labels_rotation'] = '-90 0 0'

        return axis_specs
