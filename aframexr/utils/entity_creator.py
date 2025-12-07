"""AframeXR entity creator"""

import copy
import numpy as np
import os
import pandas as pd
import urllib.request, urllib.error
import warnings

from io import StringIO  # To delete FutureWarning pandas read_json() deprecation
from itertools import cycle, islice
from pandas import DataFrame, Series

from aframexr.api.filters import FilterTransform
from aframexr.utils.constants import *


AXIS_DICT_TEMPLATE = {
    'x': {'start': None, 'end': None, 'labels_pos': [], 'labels_values': [], 'labels_rotation': ''},
    'y': {'start': None, 'end': None, 'labels_pos': [], 'labels_values': [], 'labels_rotation': ''},
    'z': {'start': None, 'end': None, 'labels_pos': [], 'labels_values': [], 'labels_rotation': ''}
}
"""Axis dictionary template for chart creation."""

GROUP_DICT_TEMPLATE = {'pos': '', 'rotation': ''}
"""Group dictionary template for group base specifications creation."""


def _get_raw_data(data_field: dict, transform_field: dict | None) -> DataFrame:
    """Returns the raw data from the data field specifications, transformed if necessary."""

    # Get the raw data of the chart
    if data_field.get('url'):  # Data is stored in a file
        try:
            if data_field['url'].startswith(('http://', 'https://')):  # Load data as URL
                with urllib.request.urlopen(data_field['url']) as response:
                    json_data = response.read().decode()
            else:
                path = os.path.normpath(data_field['url'])
                with open(path, 'r') as f:
                    json_data = f.read()
            raw_data = pd.read_json(StringIO(json_data))  # Convert JSON data into DataFrame

        except urllib.error.URLError:
            raise IOError(f'Could not load data from URL: {data_field['url']}.')
        except FileNotFoundError:
            raise IOError(f'Could not find local file: {data_field['url']}.')
        except IOError as e:
            raise IOError(f'Could not load data from local file: {data_field['url']}. Error: {e}.')

    elif data_field.get('values'):  # Data is stored as the raw data
        json_data = data_field['values']
        raw_data = pd.DataFrame(json_data)
    else:
        raise ValueError('Data specifications has no correct syntaxis, must have field "url" or "values".')

    # Transform data (if necessary)
    if transform_field:

        for filter_transformation in transform_field:  # The first transformations are the filters
            if filter_transformation.get('filter'):
                filter_object = FilterTransform.from_string(filter_transformation['filter'])
                try:
                    if isinstance(filter_object.value, str):
                        filter_object.value = f'"{filter_object.value}"'  # Add quotes to the value for query search
                    raw_data = raw_data.query(f'{filter_object.field} {filter_object.operator} {filter_object.value}')
                except KeyError:  # There is no field of the filter in data
                    raise ValueError(f'Data has no key "{filter_object.field}".')
                if raw_data.empty:  # Data does not contain any value for the filter
                    warnings.warn(f'Data does not contain values for the filter: {filter_transformation["filter"]}.')
            raw_data = raw_data.reset_index(drop=True)  # Reset the indices of the new data

        for non_filter_transformation in transform_field:  # Non-filter transformations
            if non_filter_transformation.get('aggregate'):
                from aframexr.api.aggregate import AggregatedFieldDef  # To avoid circular import error

                aggregate_object = AggregatedFieldDef.from_dict(non_filter_transformation['aggregate'])
                raw_data = aggregate_object.aggregate_data(raw_data)
            raw_data = raw_data.reset_index(drop=True)  # Reset the indices of the new data

    return raw_data


class ChartCreator:
    """Chart creator base class"""

    def __init__(self, chart_specs: dict):
        base_position = chart_specs.get('position', DEFAULT_CHART_POS)
        [self._base_x, self._base_y, self._base_z] = [float(pos) for pos in base_position.split()]  # Base position
        self._encoding = chart_specs.get('encoding')  # Encoding and parameters of the chart
        rotation = chart_specs.get('rotation', DEFAULT_CHART_ROTATION)  # Rotation of the chart
        [self._x_rotation, self._y_rotation, self._z_rotation] = [float(rot) for rot in rotation.split()]

    @staticmethod
    def create_object(chart_type: str, chart_specs: dict):
        """Returns a ChartCreator instance of the specific chart type."""

        CREATOR_MAP = {
            'arc': ArcChartCreator,
            'bar': BarChartCreator,
            'gltf': GLTFModelCreator,
            'image': ImageCreator,
            'point': PointChartCreator,
        }

        if chart_type not in CREATOR_MAP:
            raise ValueError(f'Invalid chart type: {chart_type}.')
        return CREATOR_MAP[chart_type](chart_specs)

    def get_group_specs(self) -> dict:
        """Returns a dictionary with the base specifications for the group of elements."""

        group_specs = copy.deepcopy(GROUP_DICT_TEMPLATE)
        group_specs.update({'pos': f'{self._base_x} {self._base_y} {self._base_z}',
                            'rotation': f'{self._x_rotation} {self._y_rotation} {self._z_rotation}'})
        return group_specs


class ArcChartCreator(ChartCreator):
    """Arc chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._raw_data = _get_raw_data(chart_specs['data'], chart_specs.get('transform'))  # Raw data
        self._radius = chart_specs['mark'].get('radius', DEFAULT_PIE_RADIUS)  # Radius
        self._set_rotation()
        self._color_data = Series()
        self._theta_data = Series()

    def _set_rotation(self):
        """Sets the rotation of the pie chart."""

        pie_rotation = DEFAULT_PIE_ROTATION.split()  # Default rotation for the pie chart to look at the camera
        self._x_rotation = self._x_rotation + float(pie_rotation[0])
        self._y_rotation = self._y_rotation + float(pie_rotation[1])
        self._z_rotation = self._z_rotation + float(pie_rotation[2])

    def _set_elements_theta(self) -> tuple[Series, Series]:
        """Returns a tuple with a Series storing the theta start of each element, and another storing theta length."""

        sum_data = self._theta_data.sum()  # Sum all the values
        theta_length = (self._theta_data / sum_data) * 360  # Series of theta lengths (in degrees)
        theta_start = theta_length.cumsum().shift(1, fill_value=0)  # Accumulative sum (first value is 0)
        return theta_start, theta_length

    def _set_elements_colors(self) -> Series:
        """Returns a Series of the color for each element composing the chart."""

        colors = cycle(AVAILABLE_COLORS)  # Color cycle iterator
        element_colors = Series(islice(colors, len(self._color_data)))  # Take len(self._color_data) colors
        return element_colors

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        if self._raw_data.empty:  # There is no data to display
            return []

        # Axis
        x_coordinates = Series(data=np.full(len(self._raw_data), 0), index=self._raw_data.index)
        y_coordinates = Series(data=np.full(len(self._raw_data), 0), index=self._raw_data.index)
        z_coordinates = Series(data=np.full(len(self._raw_data), 0), index=self._raw_data.index)

        # Radius
        radius = Series(
            data=np.full(len(self._raw_data), self._radius),
            index=self._raw_data.index
        )

        # Theta
        theta_field = self._encoding['theta']['field']
        try:
            self._theta_data = self._raw_data[theta_field]
        except KeyError:
            raise ValueError(f'Data has no key {theta_field}.')
        theta_starts, theta_lengths = self._set_elements_theta()

        # Color
        color_field = self._encoding['color']['field']
        self._color_data = self._raw_data[color_field]
        colors = self._set_elements_colors()

        # Id
        ids_series = [self._color_data.astype(str), self._theta_data.astype(str)]
        ids = ids_series[0].str.cat(others=ids_series[1:], sep=' : ', na_rep='?')  # Concatenate values of the series

        # Return values
        pos_series = x_coordinates.astype(str).str.cat([y_coordinates.astype(str), z_coordinates.astype(str)], sep=' ')

        temp_df = pd.DataFrame({
            'id': ids,
            'pos': pos_series,
            'radius': radius,
            'theta_start': theta_starts,
            'theta_length': theta_lengths,
            'color': colors
        })
        elements_specs = temp_df.to_dict(orient='records')  # Transform DataFrame into a list of dictionaries
        return elements_specs

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)
        return axis_specs  # Arc chart have no axis


class BarChartCreator(ChartCreator):
    """Bar chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._raw_data = _get_raw_data(chart_specs['data'], chart_specs.get('transform'))  # Raw data
        self._bar_width = chart_specs['mark'].get('width', DEFAULT_BAR_WIDTH)  # Width of the bar
        self._max_height = chart_specs.get('height', DEFAULT_MAX_HEIGHT)  # Maximum height of the bar chart
        self._x_data: Series | None = None
        self._y_data: Series | None = None
        self._z_data: Series | None = None

    def _set_bars_colors(self) -> Series:
        """Returns a Series of the color for each bar composing the bar chart."""

        colors = cycle(AVAILABLE_COLORS)  # Color cycle iterator
        bars_colors = Series(islice(colors, len(self._raw_data)))  # Take len(self._raw_data) colors from the cycle
        return bars_colors

    def _set_bars_heights(self) -> Series:
        """Returns a Series of the height for each bar composing the bar chart."""

        if self._y_data is None:
            heights = Series(  # Series of DEFAULT_BAR_HEIGHT_WHEN_NO_Y_AXIS values
                data=np.full(len(self._raw_data), DEFAULT_BAR_HEIGHT_WHEN_NO_Y_AXIS),
                index=self._raw_data.index
            )
        else:
            max_value = self._y_data.max()
            heights = (self._y_data / max_value) * self._max_height
        return heights

    def _set_x_coordinates(self) -> Series:
        """Returns a Series of the x coordinates for each bar composing the bar chart."""

        relative_x_start = self._bar_width / 2  # Shift because of box creations

        if self._x_data is None:  # No field for x-axis
            x_coordinates = Series(  # Series of relative_x_start values
                data=np.full(len(self._raw_data), relative_x_start),
                index=self._raw_data.index
            )
        else:  # Field for x-axis
            x_coordinates = Series(
                data=relative_x_start + (np.arange(len(self._raw_data)) * self._bar_width),
                index=self._raw_data.index
            )
        return x_coordinates

    def _set_z_coordinates(self) -> Series:
        """Returns a Series of the z coordinates for each bar composing the bar chart."""

        relative_z_start = - DEFAULT_BAR_DEPTH / 2  # Shift because of box creations

        if self._z_data is None:
            z_coordinates = Series(  # Series of relative_z_start values
                data=np.full(len(self._raw_data), relative_z_start),
                index=self._raw_data.index
            )
        else:
            categories = pd.Categorical(self._z_data)  # Assign one number for each category (faster indexation)
            z_coordinates_map = np.linspace(  # Array of equally spaced values
                start=relative_z_start,  # First value of the array
                stop=-DEFAULT_MAX_DEPTH + (DEFAULT_BAR_DEPTH / 2),  # Last value of the array
                num=len(categories.categories)  # Number of elements
            )
            z_coordinates = pd.Series(z_coordinates_map[categories.codes], index=self._z_data.index)
        return z_coordinates

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        if self._raw_data.empty:  # There is no data to display
            return []

        # X-axis
        if self._encoding.get('x'):
            x_field = self._encoding['x']['field']  # Field of the x-axis
            try:
                self._x_data = self._raw_data[x_field]
            except KeyError:
                raise ValueError(f'Data has no key "{x_field}".')

        # Y-axis
        if self._encoding.get('y'):
            y_field = self._encoding['y']['field']  # Field of the y-axis
            try:
                self._y_data = self._raw_data[y_field]
            except KeyError:
                raise ValueError(f'Data has no key "{y_field}".')

        # Z-axis
        if self._encoding.get('z'):
            z_field = self._encoding['z']['field']  # Field of the z-axis
            try:
                self._z_data = self._raw_data[z_field]
            except KeyError:
                raise ValueError(f'Data has no key "{z_field}".')

        bar_widths = Series(  # Series of self._bar_width values
            data=np.full(len(self._raw_data), self._bar_width),
            index=self._raw_data.index
        )
        x_coordinates = self._set_x_coordinates()  # X-axis coordinate for each bar

        bar_heights = self._set_bars_heights()  # Series of the height for each bar
        y_coordinates = bar_heights / 2  # Y-axis coordinates is the height of the bar / 2 (because of box creation)

        z_coordinates = self._set_z_coordinates()

        # Color
        colors = self._set_bars_colors()

        # Id
        ids_series = []
        if self._x_data is not None:
            ids_series.append(self._x_data.astype(str))
        if self._y_data is not None:
            ids_series.append(self._y_data.astype(str))
        if self._z_data is not None:
            ids_series.append(self._z_data.astype(str))

        ids = ids_series[0].str.cat(others=ids_series[1:], sep=' : ', na_rep='?')  # Concatenate values of the series

        # Return values
        pos_series = x_coordinates.astype(str).str.cat([y_coordinates.astype(str), z_coordinates.astype(str)], sep=' ')
        temp_df = pd.DataFrame({
            'id': ids,
            'pos': pos_series,
            'width': bar_widths,
            'height': bar_heights,
            'color': colors,
        })
        elements_specs = temp_df.to_dict(orient='records')  # Transform DataFrame into a list of dictionaries
        return elements_specs

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)

        if self._raw_data.empty:  # There is no data to display
            return axis_specs

        # ---- X-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['x']['axis'] if self._encoding.get('x') else False
        except KeyError or display_axis is True:  # Display axis if key 'axis' not found (default display axis) or True
            axis_specs['x']['start'] = '0 0 0'
            axis_specs['x']['end'] = f'{self._bar_width * len(self._x_data)} 0 0'

            # Axis labels
            x_coords = self._set_x_coordinates()  # X-axis value for each bar
            y_coords = Series(  # Series of LABELS_Y_DELTA values
                data=np.full(len(self._x_data), LABELS_Y_DELTA),
                index=self._x_data.index
            )
            z_coords = Series(  # Series of LABELS_Z_DELTA values
                data=np.full(len(self._x_data), LABELS_Z_DELTA),
                index=self._x_data.index
            )
            label_pos_series = x_coords.astype(str).str.cat([y_coords.astype(str), z_coords.astype(str)], sep=' ')

            axis_specs['x']['labels_pos'] = label_pos_series.tolist()
            axis_specs['x']['labels_values'] = self._x_data.tolist()
            axis_specs['x']['labels_rotation'] = '-90 0 -90'

        # ---- Y-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['y']['axis'] if self._encoding.get('y') else False
        except KeyError or display_axis is True:  # Display axis if key 'axis' not found (default display axis) or True
            axis_specs['y']['start'] = '0 0 0'
            axis_specs['y']['end'] = f'0 {self._max_height} 0'

            # Axis labels
            label_y_positions = np.linspace(
                start=self._max_height / Y_NUM_OF_TICKS,  # The lower label does not start in the ground
                stop=self._max_height,
                num=Y_NUM_OF_TICKS
            )
            label_values = np.linspace(  # Array of Y_NUM_OF_TICKS equally spaced values
                start=self._y_data.max() / Y_NUM_OF_TICKS,
                stop=self._y_data.max(),
                num=Y_NUM_OF_TICKS
            )

            x_coords = pd.Series(  # Series of Y_LABELS_X_DELTA values (repeated Y_NUM_OF_TICKS times)
                data=np.full(Y_NUM_OF_TICKS, Y_LABELS_X_DELTA),
                index=pd.RangeIndex(Y_NUM_OF_TICKS)
            )
            y_coords = pd.Series(label_y_positions, index=pd.RangeIndex(Y_NUM_OF_TICKS))
            z_coords = pd.Series(  # Series of 0 values (repeated Y_NUM_OF_TICKS times)
                data=np.full(Y_NUM_OF_TICKS, 0),
                index=pd.RangeIndex(Y_NUM_OF_TICKS)
            )
            label_pos_series = x_coords.astype(str).str.cat([y_coords.astype(str), z_coords.astype(str)], sep=' ')

            axis_specs['y']['labels_pos'] = label_pos_series.tolist()
            axis_specs['y']['labels_values'] = label_values.tolist()
            axis_specs['y']['labels_rotation'] = '0 0 0'

        # ---- Z-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['z']['axis'] if self._encoding.get('z') else False
        except KeyError or display_axis is True:  # Display axis if key 'axis' not found (default display axis) or True
            axis_specs['z']['start'] = '0 0 0'
            axis_specs['z']['end'] = f'0 0 {-DEFAULT_MAX_DEPTH}'

            # Axis labels
            categories = pd.Categorical(self._z_data)  # Transform categories into numbers (faster indexation)
            unique_label_values = categories.categories.tolist()  # Get only the unique values

            x_coords = pd.Series(  # Series of Z_LABELS_X_DELTA values
                data=np.full(len(categories.categories), Z_LABELS_X_DELTA),
                index=pd.RangeIndex(len(categories.categories))
            )
            y_coords = pd.Series(  # Series of LABELS_Y_DELTA values
                data=np.full(len(categories.categories), LABELS_Y_DELTA),
                index=pd.RangeIndex(len(categories.categories))
            )
            z_coords = self._set_z_coordinates()  # Z-axis coordinates for labels (aligned with bar centers)
            label_pos_series = x_coords.astype(str).str.cat([y_coords.astype(str), z_coords.astype(str)], sep=' ')

            axis_specs['z']['labels_pos'] = label_pos_series.tolist()
            axis_specs['z']['labels_values'] = unique_label_values
            axis_specs['z']['labels_rotation'] = '-90 0 0'

        return axis_specs


class GLTFModelCreator(ChartCreator):
    """GLTF model creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._url = chart_specs['data']['url']  # URL of the image model
        self._scale = chart_specs['mark'].get('scale', DEFAULT_GLTF_SCALE)

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        return [{'src': self._url, 'scale': self._scale}]

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)
        return axis_specs  # GLTF models have no axis


class ImageCreator(ChartCreator):
    """Image creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._url = chart_specs['data']['url']  # URL of the image model
        self._height = chart_specs['mark'].get('height', DEFAULT_IMAGE_HEIGHT)
        self._width = chart_specs['mark'].get('width', DEFAULT_IMAGE_WIDTH)

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        return [{'src': self._url, 'width': self._width, 'height': self._height}]

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)
        return axis_specs  # Images have no axis


class PointChartCreator(ChartCreator):
    """Point chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._raw_data = _get_raw_data(chart_specs['data'], chart_specs.get('transform'))  # Raw data
        self._height = chart_specs.get('height', DEFAULT_MAX_HEIGHT)
        self._max_radius = chart_specs['mark'].get('max_radius', DEFAULT_POINT_RADIUS)
        self._color_data: Series | None = None
        self._size_data: Series | None = None
        self._x_data: Series | None = None
        self._y_data: Series | None = None
        self._z_data: Series | None = None

    def _set_points_colors(self) -> Series:
        """Returns a Series of the color for each point composing the scatter plot."""

        if self._color_data is None:
            raise Exception('Should never enter here.')

        categories = pd.Categorical(self._color_data)  # Transform categories to numbers (faster indexation)
        color_cycle = cycle(AVAILABLE_COLORS)  # Color cycle
        color_map_array = np.array(list(islice(color_cycle, len(categories.categories))))  # Array of colors (moduled)
        point_colors_array = color_map_array[categories.codes]  # Assign one color for each category
        points_colors = pd.Series(point_colors_array, index=self._color_data.index)
        return points_colors

    def _set_points_radius(self) -> Series:
        """Returns a Series of the radius for each point composing the bubble chart."""

        if self._size_data is None:
            raise Exception('Should never enter here.')

        max_value = self._size_data.max()
        points_radius_series = (self._size_data / max_value) * self._max_radius
        return points_radius_series

    def _set_x_coordinates(self, points_radius: Series) -> Series:
        """Returns a Series of the x coordinates for each point composing the point chart."""

        base_x = points_radius.iat[0]  # Take the radius of the first element so the chart starts in the base position
        if self._x_data is None:
            x_coordinates = Series(  # Series of base_x values
                data=np.full(len(self._raw_data), base_x),
                index=self._raw_data.index
            )
        else:
            x_coordinates = Series(
                data=base_x + (np.arange(len(self._x_data)) * DEFAULT_POINT_X_SEPARATION),
                index=self._raw_data.index
            )
        return x_coordinates

    def _set_y_coordinates(self, points_radius: Series) -> Series:
        """Returns a Series of the y coordinates for each point composing the point chart."""

        base_y = points_radius.max()  # Assert no points cross under the chart

        if self._y_data is None:
            y_coordinates = Series(  # Series of base_y values
                data=np.full(len(self._raw_data), base_y),
                index=self._raw_data.index
            )
        else:
            max_value = self._y_data.max()  # Proportional heights of the data
            y_coordinates = base_y + (self._y_data / max_value) * self._height  # Series of y-axis coordinates
        return y_coordinates

    def _set_z_coordinates(self) -> Series:
        """Returns a Series of the z coordinates for each point composing the point chart."""

        base_z = -DEFAULT_POINT_RADIUS

        if self._z_data is None:
            z_coordinates = Series(
                data=np.full(len(self._raw_data), base_z),
                index=self._raw_data.index
            )
        else:
            categories = pd.Categorical(self._z_data)  # Transform categories to numbers (faster indexation)
            z_coordinates_map = np.linspace(
                start=base_z,
                stop=-DEFAULT_MAX_DEPTH + DEFAULT_POINT_RADIUS,
                num=len(categories.categories)
            )
            z_coordinates = pd.Series(z_coordinates_map[categories.codes], index=self._z_data.index)
        return z_coordinates

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        if self._raw_data.empty:  # There is no data to display
            return []

        elements_specs = []

        # X-axis
        radius = Series(  # Series of self._max_radius values
            data=np.full(len(self._raw_data), self._max_radius),
            index=self._raw_data.index
        )

        if self._encoding.get('x'):
            x_field = self._encoding['x']['field']
            self._x_data = self._raw_data[x_field]

            if self._encoding.get('size'):  # Bubbles plot (the size of the point depends on the value of the field)
                size_field = self._encoding['size']['field']
                self._size_data = self._raw_data[size_field]
                radius = self._set_points_radius()
            else:  # Scatter plot (same radius for all points)
                pass

        x_coordinates = self._set_x_coordinates(radius)

        # Y-axis
        if self._encoding.get('y'):
            y_field = self._encoding['y']['field']  # Field of the y-axis
            self._y_data = self._raw_data[y_field]

        y_coordinates = self._set_y_coordinates(radius)

        # Z-axis
        if self._encoding.get('z'):
            z_field = self._encoding['z']['field']  # Field of the z-axis
            self._z_data = self._raw_data[z_field]

        z_coordinates = self._set_z_coordinates()

        # Color
        if self._encoding.get('color'):  # Scatter plot (same color for each type of point)
            color_field = self._encoding['color']['field']
            self._color_data = self._raw_data[color_field]
            colors = self._set_points_colors()
        else:  # Bubbles plot (same color for all points)
            colors = Series(  # Series of DEFAULT_POINT_COLOR values
                data=np.full(len(self._raw_data), DEFAULT_POINT_COLOR),
                index=self._raw_data.index
            )

        # Id
        ids_series = []
        if self._x_data is not None:
            ids_series.append(self._x_data.astype(str))
        if self._y_data is not None:
            ids_series.append(self._y_data.astype(str))
        if self._z_data is not None:
            ids_series.append(self._z_data.astype(str))

        ids = ids_series[0].str.cat(others=ids_series[1:], sep=' : ', na_rep='?')  # Concatenate values of the series

        # Return values
        pos_series = x_coordinates.astype(str).str.cat([y_coordinates.astype(str), z_coordinates.astype(str)], sep=' ')
        temp_df = pd.DataFrame({
            'id': ids,
            'pos': pos_series,
            'radius': radius,
            'color': colors,
        })
        elements_specs = temp_df.to_dict(orient='records')  # Transform DataFrame into a list of dictionaries
        return elements_specs

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)

        if self._raw_data.empty:  # There is no data to display
            return axis_specs

        # ---- X-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['x']['axis'] if self._encoding.get('x') else False
        except KeyError or display_axis is True:  # Display axis if key not found (default display axis) or True
            axis_specs['x']['start'] = '0 0 0'
            axis_specs['x']['end'] = f'{DEFAULT_POINT_X_SEPARATION * len(self._raw_data) + self._max_radius} 0 0'

            # Axis labels
            if self._encoding.get('size'):  # Bubbles plot (the size of the point depends on the value of the field)
                radius = self._set_points_radius()
            else:  # Scatter plot (same radius for all points)
                radius = Series(  # Series of self._max_radius values
                    data=np.full(len(self._raw_data), self._max_radius),
                    index=self._raw_data.index
                )

            x_coords = self._set_x_coordinates(radius)  # X-axis value for each point
            y_coords = Series(  # Series of LABELS_Y_DELTA values
                data=np.full(len(self._x_data), LABELS_Y_DELTA),
                index=self._x_data.index
            )
            z_coords = Series(  # Series of LABELS_Z_DELTA values
                data=np.full(len(self._x_data), LABELS_Z_DELTA),
                index=self._x_data.index
            )
            label_pos_series = x_coords.astype(str).str.cat([y_coords.astype(str), z_coords.astype(str)], sep=' ')

            axis_specs['x']['labels_pos'] = label_pos_series.tolist()
            axis_specs['x']['labels_values'] = self._x_data.tolist()
            axis_specs['x']['labels_rotation'] = '-90 0 -90'  # Rotation of the labels

        # ---- Y-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding['y']['axis'] if self._encoding.get('y') else False
        except KeyError or display_axis is True:  # Display axis if key not found (default display axis) or True
            axis_specs['y']['start'] = '0 0 0'
            axis_specs['y']['end'] = f'0 {self._height} 0'

            # Axis labels
            label_y_positions = np.linspace(
                start=self._height / Y_NUM_OF_TICKS,
                stop=self._height,
                num=Y_NUM_OF_TICKS
            )
            label_values = np.linspace(  # Array of Y_NUM_OF_TICKS equally spaced values
                start=self._y_data.max() / Y_NUM_OF_TICKS,
                stop=self._y_data.max(),
                num=Y_NUM_OF_TICKS
            )

            x_coords = pd.Series(  # Series of Y_LABELS_X_DELTA values (repeated Y_NUM_OF_TICKS)
                data=np.full(Y_NUM_OF_TICKS, Y_LABELS_X_DELTA),
                index=pd.RangeIndex(Y_NUM_OF_TICKS)
            )
            y_coords = pd.Series(label_y_positions, index=pd.RangeIndex(Y_NUM_OF_TICKS))
            z_coords = pd.Series(  # Series of 0 values
                data=np.full(Y_NUM_OF_TICKS, 0),
                index=pd.RangeIndex(Y_NUM_OF_TICKS)
            )
            label_pos_series = x_coords.astype(str).str.cat([y_coords.astype(str), z_coords.astype(str)], sep=' ')

            axis_specs['y']['labels_pos'] = label_pos_series.tolist()
            axis_specs['y']['labels_values'] = label_values.tolist()
            axis_specs['y']['labels_rotation'] = '0 0 0'

        # ---- Z-axis ----
        # Axis line
        display_axis = True
        try:
            display_axis = self._encoding.get('z')['axis'] if self._encoding.get('z') else False
        except KeyError or display_axis is True:  # Display axis if key 'axis' not found (default display axis) or True
            axis_specs['z']['start'] = '0 0 0'
            axis_specs['z']['end'] = f'0 0 {-DEFAULT_MAX_DEPTH}'

            # Axis labels
            categories = pd.Categorical(self._z_data)  # Transform categories into numbers (faster indexation)
            label_z_positions = np.linspace(
                start=-(DEFAULT_POINT_RADIUS / 2),  # Start where the points have the center
                stop=-(DEFAULT_POINT_RADIUS / 2) - DEFAULT_MAX_DEPTH,  # End where the points have the center
                num=len(categories.categories)
            )
            unique_label_values = categories.categories.tolist()  # Get only the unique values

            x_coords = pd.Series(  # Series of Z_LABELS_X_DELTA values
                data=np.full(len(categories.categories), Z_LABELS_X_DELTA),
                index=pd.RangeIndex(len(categories.categories))
            )
            y_coords = pd.Series(  # Series of LABELS_Y_DELTA values
                data=np.full(len(categories.categories), LABELS_Y_DELTA),
                index=pd.RangeIndex(len(categories.categories))
            )
            z_coords = pd.Series(label_z_positions)
            label_pos_series = x_coords.astype(str).str.cat([y_coords.astype(str), z_coords.astype(str)], sep=' ')

            axis_specs['z']['labels_pos'] = label_pos_series.tolist()
            axis_specs['z']['labels_values'] = unique_label_values
            axis_specs['z']['labels_rotation'] = '-90 0 0'

        return axis_specs
