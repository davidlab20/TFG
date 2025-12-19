"""AframeXR entity creator"""

import copy
import io
import json
import os
import polars as pl
import urllib.request, urllib.error
import warnings

from itertools import cycle, islice
from polars import DataFrame, Series

from aframexr.utils.constants import *

AXIS_DICT_TEMPLATE = {
    'x': {'start': None, 'end': None, 'labels_pos': [], 'labels_values': [], 'labels_rotation': ''},
    'y': {'start': None, 'end': None, 'labels_pos': [], 'labels_values': [], 'labels_rotation': ''},
    'z': {'start': None, 'end': None, 'labels_pos': [], 'labels_values': [], 'labels_rotation': ''}
}
"""Axis dictionary template for chart creation."""

GROUP_DICT_TEMPLATE = {'pos': '', 'rotation': ''}
"""Group dictionary template for group base specifications creation."""

def _translate_dtype_into_encoding(dtype: pl.DataType) -> str:
    """Translates and returns the encoding for a given data type."""

    if dtype.is_numeric():
        encoding_type = 'quantitative'
    elif dtype in (pl.String, pl.Categorical):
        encoding_type = 'nominal'
    else:
        raise ValueError(f'Unknown dtype: {dtype}.')
    return encoding_type


def _get_data_from_url(url: str) -> DataFrame:
    """Loads the data from the URL (could be a local path) and returns it as a DataFrame."""

    if url.startswith(('http://', 'https://')):  # Data is stored in a URL
        try:
            with urllib.request.urlopen(url) as response:
                file_type = response.info().get_content_type()
                data = io.BytesIO(response.read())  # For polars
        except urllib.error.URLError:
            raise IOError(f'Could not load data from URL: {url}.')
    else:  # Data is stored in a local file
        path = os.path.normpath(url)
        if not os.path.exists(path):
            raise FileNotFoundError(f'Local file "{path}" was not found.')

        data = open(path, 'rb')
        _, file_type = os.path.splitext(path)
        file_type = file_type.lower()
    try:
        if 'csv' in file_type:  # Data is in CSV format
            df_data = pl.read_csv(data)
        elif 'json' in file_type:
            json_data = json.load(data)
            df_data = DataFrame(json_data)
        else:
            raise NotImplementedError(f'Unsupported file type: {file_type}.')
    except Exception as e:
        raise IOError(f'Error when processing data. Error: {e}.')

    if data and not url.startswith(('http', 'https')):
        data.close()  # Close the file

    return df_data


def _get_raw_data(chart_specs: dict) -> DataFrame:
    """Returns the raw data from the chart specifications, transformed if necessary."""

    # Get the raw data of the chart
    data_field = chart_specs['data']
    if data_field.get('url'):  # Data is stored in a file
        raw_data = _get_data_from_url(data_field['url'])

    elif data_field.get('values'):  # Data is stored as the raw data
        json_data = data_field['values']
        raw_data = DataFrame(json_data)
    else:
        raise ValueError('Data specifications has no correct syntaxis, must have field "url" or "values".')

    # Transform data (if necessary)
    from aframexr.api.aggregate import AggregatedFieldDef  # To avoid circular import error
    from aframexr.api.filters import FilterTransform
    transform_field = chart_specs.get('transform')
    if transform_field:

        for filter_transformation in transform_field:  # The first transformations are the filters
            if filter_transformation.get('filter'):
                filter_object = FilterTransform.from_string(filter_transformation['filter'])
                raw_data = filter_object.get_filtered_data(raw_data)
                if raw_data.is_empty():  # Data does not contain any value for the filter
                    warnings.warn(f'Data does not contain values for the filter: {filter_transformation["filter"]}.')

        for non_filter_transf in transform_field:  # Non-filter transformations
            groupby = set(non_filter_transf.get('groupby')) if non_filter_transf.get('groupby') else set()
            if non_filter_transf.get('aggregate'):

                for aggregate in non_filter_transf.get('aggregate'):
                    aggregate_object = AggregatedFieldDef.from_dict(aggregate)

                    encoding_channels = {  # Using a set to have the possibility of getting differences
                        ch_spec['field'] for ch_spec in chart_specs['encoding'].values()  # Take the encoding channels
                        if ch_spec['field'] != aggregate_object.as_field  # Except the aggregate field channel
                    }

                    if groupby:
                        not_defined_channels = encoding_channels - set(groupby)  # Difference between sets
                        if not_defined_channels:  # There are channels in encoding_channels not defined in groupby
                            raise ValueError(
                                f'Encoding channel(s) "{not_defined_channels}" must be defined in aggregate groupby: '
                                f'{groupby}, otherwise that fields will disappear.'
                            )
                    else:
                        groupby = list(encoding_channels)  # Use the encoding channels as groupby
                    raw_data = aggregate_object.get_aggregated_data(raw_data, groupby)

    # Aggregate in encoding
    encoding_channels = chart_specs['encoding']
    aggregate_fields = [ch['field'] for ch in encoding_channels.values() if ch.get('aggregate')]
    aggregate_ops = [ch['aggregate'] for ch in encoding_channels.values() if ch.get('aggregate')]
    groupby_fields = [spec['field'] for spec in encoding_channels.values() if not spec.get('aggregate')]

    for ag in range(len(aggregate_fields)):
        aggregate_object = AggregatedFieldDef(aggregate_ops[ag], aggregate_fields[ag])
        raw_data = aggregate_object.get_aggregated_data(raw_data, groupby_fields)

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

    @staticmethod
    def get_axis_specs():
        """Returns a dictionary with the specifications for each axis of the charts that does not have an axis."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)
        return axis_specs

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
        self._raw_data = _get_raw_data(chart_specs)  # Raw data
        self._radius = chart_specs['mark'].get('radius', DEFAULT_PIE_RADIUS) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_PIE_RADIUS
        self._set_rotation()
        self._color_data = Series(name='Color data', values=[], dtype=pl.String)
        self._theta_data = Series(name='Theta data', values=[], dtype=pl.Float32)

    def _set_rotation(self):
        """Sets the rotation of the pie chart."""

        pie_rotation = DEFAULT_PIE_ROTATION.split()  # Default rotation for the pie chart to look at the camera
        self._x_rotation = self._x_rotation + float(pie_rotation[0])
        self._y_rotation = self._y_rotation + float(pie_rotation[1])
        self._z_rotation = self._z_rotation + float(pie_rotation[2])

    def _set_elements_theta(self) -> tuple[Series, Series]:
        """Returns a tuple with a Series storing the theta start of each element, and another storing theta length."""

        abs_theta_data = self._theta_data.abs()
        sum_data = abs_theta_data.sum()  # Sum all the values
        theta_length = Series((abs_theta_data / sum_data) * 360)  # Series of theta lengths (in degrees)
        theta_start = theta_length.cum_sum().shift(1).fill_null(0)  # Accumulative sum (first value is 0)
        return theta_start.alias('theta_start'), theta_length.alias('theta_length')

    def _set_elements_colors(self) -> Series:
        """Returns a Series of the color for each element composing the chart."""

        colors = cycle(AVAILABLE_COLORS)  # Color cycle iterator
        element_colors = Series(islice(colors, len(self._color_data)))  # Take len(self._color_data) colors
        return element_colors.alias('color')

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        if self._raw_data.is_empty():  # There is no data to display
            return []

        data_length = len(self._raw_data)

        # Axis
        x_coordinates = pl.repeat(value=0, n=data_length).alias('x_coordinates')
        y_coordinates = pl.repeat(value=0, n=data_length).alias('y_coordinates')
        z_coordinates = pl.repeat(value=0, n=data_length).alias('z_coordinates')

        # Radius
        radius = pl.repeat(
            value=self._radius,
            n=data_length,
            eager=True  # Returns a Series
        ).alias('radius')

        # Theta
        theta_field = self._encoding['theta']['field']
        try:
            self._theta_data = self._raw_data.get_column(theta_field)
        except pl.exceptions.ColumnNotFoundError:
            raise KeyError(f'Data has no field "{theta_field}".')
        theta_starts, theta_lengths = self._set_elements_theta()

        # Color
        color_field = self._encoding['color']['field']
        try:
            self._color_data = self._raw_data.get_column(color_field)
        except pl.exceptions.ColumnNotFoundError:
            raise KeyError(f'Data has no field "{color_field}".')
        colors = self._set_elements_colors()

        # Id
        ids = pl.select(pl.concat_str(
            [self._color_data.cast(pl.String), self._theta_data.cast(pl.String)],
            separator=' : ',
        ).fill_null('?').alias('id')).to_series()

        # Return values
        temp_df = DataFrame({
            'id': ids,
            'pos': pl.select(pl.concat_str(
                [x_coordinates, y_coordinates, z_coordinates],
                separator=' '
            ).alias('pos')).to_series(),
            'radius': radius,
            'theta_start': theta_starts,
            'theta_length': theta_lengths,
            'color': colors
        })
        elements_specs = temp_df.to_dicts()  # Transform DataFrame into a list of dictionaries
        return elements_specs

    # Using get_axis_specs from ChartCreator


class BarChartCreator(ChartCreator):
    """Bar chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._raw_data = _get_raw_data(chart_specs)  # Raw data
        self._bar_width = chart_specs['mark'].get('width', DEFAULT_BAR_WIDTH) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_BAR_WIDTH
        self._max_height = chart_specs.get('height', DEFAULT_MAX_HEIGHT)  # Maximum height of the bar chart
        self._x_data: Series | None = None
        self._x_encoding: str = ''
        self._y_data: Series | None = None
        self._y_encoding: str = ''
        self._z_data: Series | None = None
        self._z_encoding: str = ''

    def _set_bars_colors(self) -> Series:
        """Returns a Series of the color for each bar composing the bar chart."""

        colors = cycle(AVAILABLE_COLORS)  # Color cycle iterator
        bars_colors = Series(islice(colors, len(self._raw_data)))  # Take len(self._raw_data) colors from the cycle
        return bars_colors.alias('color')

    @staticmethod
    def _set_coordinates_for_quantitative_axis(axis_data: Series, max_size: float) -> Series:
        if axis_data.dtype == pl.String:
            axis_data = axis_data.cast(pl.Categorical).to_physical()

        max_value, min_value = axis_data.max(), axis_data.min()  # For proportions
        range_value = max_value - min_value  # Range (positive value)
        if range_value == 0:  # All the values are the same
            return pl.repeat(
                value=max_size / 2,  # Divided by 2 because of bars creation
                n=len(axis_data),
                eager=True  # Returns a Series
            )

        if max_value < 0:  # All data is negative
            scale_factor = max_size / -min_value
        elif min_value > 0:  # All data is positive
            scale_factor = max_size / max_value
        else:  # Positive and negative data
            scale_factor = max_size / range_value
        return axis_data * scale_factor / 2  # Divided by 2 because of elements creation

    @staticmethod
    def _set_coordinates_for_nominal_axis(axis_data: Series, step: float) -> Series:
        base = step / 2  # Shift because of box creations
        category_codes = axis_data.cast(pl.String).cast(pl.Categorical).to_physical()  # Codes (0, 1, 2, ..., len(axis_data) - 1)
        return base + (step * category_codes)

    def _set_x_coords_and_widths(self) -> tuple[Series, Series]:
        """
        Returns a tuple of Series for the x-axis:
        One for the x coordinates of each bar composing the bar chart.
        One for the widths of each bar composing the bar chart.
        """

        if self._x_data is None:
            x_coordinates = pl.repeat(
                value=self._bar_width / 2,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            )
            bars_widths = pl.repeat(
                value=self._bar_width,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            )
        else:
            if self._x_encoding == 'quantitative':
                max_size = DEFAULT_MAX_HEIGHT  # TODO --> CAMBIAR POR UNA CONSTANTE BUENA (UN DEFAULT MAX WIDTH O ASI)
                x_coordinates = self._set_coordinates_for_quantitative_axis(self._x_data, max_size)
                bars_widths = 2 * x_coordinates.abs()
            elif self._x_encoding == 'nominal':
                step = self._bar_width  # TODO --> SE PUEDE AÑADIR ESPACIO ENTRE BARRAS SUMANDO AQUI EL VALOR
                x_coordinates = self._set_coordinates_for_nominal_axis(self._x_data, step)
                bars_widths = pl.repeat(
                    value=self._bar_width,
                    n=self._x_data.len(),
                    eager=True  # Returns a Series
                )
            else:
                raise ValueError(f'Invalid encoding type: {self._x_encoding}.')
        return x_coordinates.alias('x_coordinates'), bars_widths.alias('width')

    def _set_y_coords_and_heights(self) -> tuple[Series, Series]:
        """
        Returns a tuple of Series for the y-axis:
        One for the y coordinates of each bar composing the bar chart.
        One for the heights of each bar composing the bar chart.
        """

        if self._y_data is None:
            y_coordinates = pl.repeat(
                value=DEFAULT_BAR_HEIGHT_WHEN_NO_Y_AXIS / 2,  # Divided by 2 because of bars creation
                n=len(self._raw_data),
                eager=True  # Returns a Series
            )
            bars_heights = pl.repeat(
                value=DEFAULT_BAR_HEIGHT_WHEN_NO_Y_AXIS,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            )
        else:
            if self._y_encoding == 'quantitative':
                y_coordinates = self._set_coordinates_for_quantitative_axis(self._y_data, self._max_height)
                bars_heights = 2 * y_coordinates.abs()
            elif self._y_encoding == 'nominal':
                step = self._max_height / self._y_data.len()
                y_coordinates = self._set_coordinates_for_nominal_axis(self._y_data, step)
                bars_heights = pl.repeat(
                    value=step,
                    n=self._y_data.len(),
                    eager=True  # Returns a Series
                )
            else:
                raise ValueError(f'Invalid encoding type: {self._y_encoding}.')
        return y_coordinates.alias('y_coordinates'), bars_heights.alias('height')

    def _set_z_coords_and_depths(self) -> tuple[Series, Series]:
        """
        Returns a tuple of Series for the z-axis:
        One for the z coordinates of each bar composing the bar chart.
        One for the depths of each bar composing the bar chart.
        """

        if self._z_data is None:
            z_coordinates = pl.repeat(
                value=DEFAULT_BAR_DEPTH / 2,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            )
            bars_depths = pl.repeat(
                value=DEFAULT_BAR_DEPTH,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            )
        else:
            if self._z_encoding == 'quantitative':
                z_coordinates = self._set_coordinates_for_quantitative_axis(self._z_data, DEFAULT_MAX_DEPTH)
                bars_depths = 2 * z_coordinates.abs()
            elif self._z_encoding == 'nominal':
                z_coordinates = self._set_coordinates_for_nominal_axis(self._z_data, DEFAULT_BAR_DEPTH)
                bars_depths = pl.repeat(
                    value=DEFAULT_BAR_DEPTH,
                    n=self._z_data.len(),
                    eager=True  # Returns a Series
                )
            else:
                raise ValueError(f'Invalid encoding type: {self._z_encoding}.')
        return z_coordinates.alias('z_coordinates'), bars_depths.alias('depth')

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        if self._raw_data.is_empty():  # There is no data to display
            return []

        from aframexr import AframeXRValidator  # To avoid circular import

        # X-axis
        if self._encoding.get('x'):
            x_field = self._encoding['x']['field']  # Field of the x-axis
            try:
                self._x_data = self._raw_data[x_field]

                detected_x_encoding = _translate_dtype_into_encoding(self._x_data.dtype)
                self._x_encoding = self._encoding['x'].get('type', detected_x_encoding)

                AframeXRValidator.compare_user_encoding_detected_encoding(
                    axis_name='x',
                    user_encoding=self._x_encoding,
                    detected_encoding=detected_x_encoding
                )
            except pl.exceptions.ColumnNotFoundError:
                raise KeyError(f'Data has no field "{x_field}".')

        x_coordinates, bar_widths = self._set_x_coords_and_widths()
        x_coordinates = x_coordinates + 2 * abs(x_coordinates.min()) if x_coordinates.min() < 0 else x_coordinates

        # Y-axis
        if self._encoding.get('y'):
            y_field = self._encoding['y']['field']  # Field of the y-axis
            try:
                self._y_data = self._raw_data[y_field]

                detected_y_encoding = _translate_dtype_into_encoding(self._y_data.dtype)
                self._y_encoding = self._encoding['y'].get('type', detected_y_encoding)

                AframeXRValidator.compare_user_encoding_detected_encoding(
                    axis_name='y',
                    user_encoding=self._y_encoding,
                    detected_encoding=detected_y_encoding
                )
            except pl.exceptions.ColumnNotFoundError:
                raise KeyError(f'Data has no field "{y_field}".')

        y_coordinates, bar_heights = self._set_y_coords_and_heights()
        y_coordinates = y_coordinates + 2 * abs(y_coordinates.min()) if y_coordinates.min() < 0 else y_coordinates

        # Z-axis
        if self._encoding.get('z'):
            z_field = self._encoding['z']['field']  # Field of the z-axis
            try:
                self._z_data = self._raw_data[z_field]
                detected_z_encoding = _translate_dtype_into_encoding(self._z_data.dtype)
                self._z_encoding = self._encoding['z'].get('type', _translate_dtype_into_encoding(self._z_data.dtype))

                AframeXRValidator.compare_user_encoding_detected_encoding(
                    axis_name='z',
                    user_encoding=self._z_encoding,
                    detected_encoding=detected_z_encoding
                )
            except pl.exceptions.ColumnNotFoundError:
                raise KeyError(f'Data has no field "{z_field}".')

        z_coordinates, bar_depths = self._set_z_coords_and_depths()
        z_coordinates = z_coordinates + 2 * abs(z_coordinates.min()) if z_coordinates.min() < 0 else z_coordinates
        z_coordinates = -z_coordinates  # Invert the coordinates to do deep

        # Color
        colors = self._set_bars_colors()

        # Id
        ids_series = []
        if self._x_data is not None:
            ids_series.append(self._x_data.cast(pl.String))
        if self._y_data is not None:
            ids_series.append(self._y_data.cast(pl.String))
        if self._z_data is not None:
            ids_series.append(self._z_data.cast(pl.String))

        ids = pl.select(pl.concat_str(
            ids_series,
            separator=' : '
        ).fill_null('?').alias('id')).to_series()

        # Return values
        temp_df = DataFrame({
            'id': ids,
            'pos': pl.select(pl.concat_str(
                [x_coordinates, y_coordinates, z_coordinates],
                separator=' '
            ).alias('pos')).to_series(),
            'width': bar_widths,
            'height': bar_heights,
            'color': colors
        })
        elements_specs = temp_df.to_dicts()  # Transform DataFrame into a list of dictionaries
        return elements_specs

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)

        if self._raw_data.is_empty():  # There is no data to display
            return axis_specs

        # ---- X-axis ----
        # Axis line
        display_axis = self._encoding['x'].get('axis', True) if self._encoding.get('x') else False
        if display_axis:  # Display axis if key 'axis' not found (default display axis) or True
            axis_specs['x']['start'] = '0 0 0'
            axis_specs['x']['end'] = f'{self._bar_width * len(self._x_data)} 0 0'

            # Axis labels
            x_coords = self._set_x_coordinates()  # X-axis value for each bar
            y_coords = pl.repeat(
                value=LABELS_Y_DELTA,
                n=len(self._x_data),
                eager=True  # Returns a Series
            ).alias('y_coords')
            z_coords = pl.repeat(
                value=LABELS_Z_DELTA,
                n=len(self._x_data),
                eager=True  # Returns a Series
            ).alias('z_coords')
            label_pos_series = pl.select(pl.concat_str(
                [x_coords, y_coords, z_coords],
                separator=' '
            ).fill_null('?').alias('id')).to_series()

            axis_specs['x']['labels_pos'] = label_pos_series.to_list()
            axis_specs['x']['labels_values'] = self._x_data.to_list()
            axis_specs['x']['labels_rotation'] = '-90 0 -90'

        # ---- Y-axis ----
        # Axis line
        display_axis = self._encoding['y'].get('axis', True) if self._encoding.get('y') else False
        if display_axis:  # Display axis if key 'axis' not found (default display axis) or True
            axis_specs['y']['start'] = '0 0 0'
            axis_specs['y']['end'] = f'0 {self._max_height} 0'

            # Axis labels
            y_coords = pl.linear_space(  # Equally spaced values
                start=self._max_height / Y_NUM_OF_TICKS,  # The lower label does not start in the ground
                end=self._max_height,
                num_samples=Y_NUM_OF_TICKS,
                eager=True  # Returns a Series
            ).alias('y_coords')
            label_values = pl.linear_space(  # Equally spaced values
                start=self._y_data.max() / Y_NUM_OF_TICKS,
                end=self._y_data.max(),
                num_samples=Y_NUM_OF_TICKS,
                eager=True  # Returns a Series
            ).round(2)  # Round to the second decimal

            x_coords = pl.repeat(
                value=Y_LABELS_X_DELTA,
                n=Y_NUM_OF_TICKS,
                eager=True  # Returns a Series
            ).alias('x_coords')
            z_coords = pl.repeat(
                value=0,
                n=Y_NUM_OF_TICKS,
                eager=True  # Returns a Series
            ).alias('z_coords')
            label_pos_series = pl.select(pl.concat_str(
                [x_coords, y_coords, z_coords],
                separator=' ',
            ).fill_null('?').alias('id')).to_series()

            axis_specs['y']['labels_pos'] = label_pos_series.to_list()
            axis_specs['y']['labels_values'] = label_values.to_list()
            axis_specs['y']['labels_rotation'] = '0 0 0'

        # ---- Z-axis ----
        # Axis line
        display_axis = self._encoding['z'].get('axis', True) if self._encoding.get('z') else False
        if display_axis:  # Display axis if key 'axis' not found (default display axis) or True
            axis_specs['z']['start'] = '0 0 0'
            axis_specs['z']['end'] = f'0 0 {-DEFAULT_MAX_DEPTH}'

            # Axis labels
            categories = self._z_data.unique()

            x_coords = pl.repeat(
                value=Z_LABELS_X_DELTA,
                n=len(categories),
                eager=True  # Returns a Series
            ).alias('x_coords')
            y_coords = pl.repeat(
                value=LABELS_Y_DELTA,
                n=len(categories),
                eager=True  # Returns a Series
            )
            z_coords = self._set_z_coordinates().unique()  # Z-axis coordinates for labels (aligned with bar centers)
            label_pos_series = pl.select(pl.concat_str(
                [x_coords, y_coords, z_coords],
                separator=' ',
            ).fill_null('?').alias('id')).to_series()

            axis_specs['z']['labels_pos'] = label_pos_series.to_list()
            axis_specs['z']['labels_values'] = categories.to_list()
            axis_specs['z']['labels_rotation'] = '-90 0 0'

        return axis_specs


class GLTFModelCreator(ChartCreator):
    """GLTF model creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._url = chart_specs['data']['url']  # URL of the image model
        self._scale = chart_specs['mark'].get('scale', DEFAULT_GLTF_SCALE) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_GLTF_SCALE

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        return [{'src': self._url, 'scale': self._scale}]

    # Using get_axis_specs from ChartCreator


class ImageCreator(ChartCreator):
    """Image creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._url = chart_specs['data']['url']  # URL of the image model
        self._height = chart_specs['mark'].get('height', DEFAULT_IMAGE_HEIGHT) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_IMAGE_HEIGHT
        self._width = chart_specs['mark'].get('width', DEFAULT_IMAGE_WIDTH) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_IMAGE_WIDTH

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        return [{'src': self._url, 'width': self._width, 'height': self._height}]

    # Using get_axis_specs from ChartCreator


class PointChartCreator(ChartCreator):
    """Point chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._raw_data = _get_raw_data(chart_specs)  # Raw data
        self._height = chart_specs.get('height', DEFAULT_MAX_HEIGHT)
        self._max_radius = chart_specs['mark'].get('max_radius', DEFAULT_POINT_RADIUS) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_POINT_RADIUS
        self._color_data: Series | None = None
        self._size_data: Series | None = None
        self._x_data: Series | None = None
        self._y_data: Series | None = None
        self._z_data: Series | None = None

    def _set_points_colors(self) -> Series:
        """Returns a Series of the color for each point composing the scatter plot."""

        if self._color_data is None:
            raise Exception('Should never enter here.')

        category_codes = sorted(self._color_data.unique().to_list())  # Sorted for consistency
        mapping_dict = dict(zip(
            category_codes,  # Dict keys
            list(islice(  # Dict values
                cycle(AVAILABLE_COLORS),  # Color cycle
                len(category_codes)  # Moduled to category codes
            ))
        ))
        points_colors = self._color_data.replace(list(mapping_dict.keys()), list(mapping_dict.values()))
        return points_colors.alias('color')

    def _set_points_radius(self) -> Series:
        """Returns a Series of the radius for each point composing the bubble chart."""

        if self._size_data is None:
            raise Exception('Should never enter here.')

        max_value = self._size_data.max()
        points_radius_series = (self._size_data / max_value) * self._max_radius
        return points_radius_series.alias('radius')

    def _set_x_coordinates(self, points_radius: Series) -> Series:
        """Returns a Series of the x coordinates for each point composing the point chart."""

        base_x = points_radius.item(0)  # Take the radius of the first element so the chart starts in the base position
        if self._x_data is None:
            x_coordinates = pl.repeat(
                value=base_x,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            )
        else:
            x_coordinates = (
                    base_x + (
                    pl.int_range(
                        start=0,
                        end=len(self._x_data),
                        step=1,
                        eager=True  # Returns a Series
                    ) * DEFAULT_POINT_X_SEPARATION)
            )
        return x_coordinates.alias('x_coordinates')

    def _set_y_coordinates(self) -> Series:
        """Returns a Series of the y coordinates for each point composing the point chart."""

        if self._y_data is None:
            y_coordinates = pl.repeat(
                value=self._max_radius,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            )
        else:
            max_value = self._y_data.max()  # Proportional heights of the data
            y_coordinates = (self._y_data / max_value) * self._height  # Series of y-axis coordinates
        return y_coordinates.alias('y_coordinates')

    def _set_z_coordinates(self) -> Series:
        """Returns a Series of the z coordinates for each point composing the point chart."""

        base_z = -DEFAULT_POINT_RADIUS

        if self._z_data is None:
            z_coordinates = pl.repeat(
                value=base_z,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            )
        else:
            category_names = sorted(self._z_data.unique().to_list())  # Sorted for consistency
            z_coordinates_map = pl.linear_space(
                start=base_z,
                end=-DEFAULT_MAX_DEPTH + DEFAULT_POINT_RADIUS,
                num_samples=len(category_names),
                eager=True  # Returns a Series
            )
            mapping_dict = dict(zip(category_names, z_coordinates_map))
            z_coordinates = self._z_data.replace(mapping_dict)
        return z_coordinates.alias('z_coordinates')

    def get_elements_specs(self) -> list[dict]:
        """Returns a list of dictionaries with the specifications for each element of the chart."""

        if self._raw_data.is_empty():  # There is no data to display
            return []

        # X-axis
        radius = pl.repeat(
            value=self._max_radius,
            n=len(self._raw_data),
            eager=True  # Returns a Series
        ).alias('radius')

        if self._encoding.get('x'):
            x_field = self._encoding['x']['field']
            try:
                self._x_data = self._raw_data[x_field]
            except pl.exceptions.ColumnNotFoundError:
                raise KeyError(f'Data has no field "{x_field}".')

        if self._encoding.get('size'):  # Bubbles plot (the size of the point depends on the value of the field)
            size_field = self._encoding['size']['field']
            try:
                self._size_data = self._raw_data[size_field]
            except pl.exceptions.ColumnNotFoundError:
                raise KeyError(f'Data has no field "{size_field}".')

            radius = self._set_points_radius()
        else:  # Scatter plot (same radius for all points)
            pass

        x_coordinates = self._set_x_coordinates(radius)

        # Y-axis
        if self._encoding.get('y'):
            y_field = self._encoding['y']['field']  # Field of the y-axis
            try:
                self._y_data = self._raw_data[y_field]
            except pl.exceptions.ColumnNotFoundError:
                raise KeyError(f'Data has no field "{y_field}".')

        y_coordinates = self._set_y_coordinates()

        # Z-axis
        if self._encoding.get('z'):
            z_field = self._encoding['z']['field']  # Field of the z-axis
            try:
                self._z_data = self._raw_data[z_field]
            except pl.exceptions.ColumnNotFoundError:
                raise KeyError(f'Data has no field "{z_field}".')

        z_coordinates = self._set_z_coordinates()

        # Color
        if self._encoding.get('color'):  # Scatter plot (same color for each type of point)
            color_field = self._encoding['color']['field']
            try:
                self._color_data = self._raw_data[color_field]
            except pl.exceptions.ColumnNotFoundError:
                raise KeyError(f'Data has no field "{color_field}".')

            colors = self._set_points_colors()
        else:  # Bubbles plot (same color for all points)
            colors = pl.repeat(
                value=DEFAULT_POINT_COLOR,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            ).alias('color')

        # Id
        ids_series = []
        if self._x_data is not None:
            ids_series.append(self._x_data.cast(pl.String))
        if self._y_data is not None:
            ids_series.append(self._y_data.cast(pl.String))
        if self._z_data is not None:
            ids_series.append(self._z_data.cast(pl.String))

        ids = pl.select(pl.concat_str(
            ids_series,
            separator=' : ',
        ).fill_null('?').alias('id')).to_series()

        # Return values
        temp_df = DataFrame({
            'id': ids,
            'pos': pl.select(pl.concat_str(
                [x_coordinates, y_coordinates, z_coordinates],
                separator=' '
            ).alias('pos')).to_series(),
            'radius': radius,
            'color': colors,
        })
        elements_specs = temp_df.to_dicts()  # Transform DataFrame into a list of dictionaries
        return elements_specs

    def get_axis_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)

        if self._raw_data.is_empty():  # There is no data to display
            return axis_specs

        # ---- X-axis ----
        # Axis line
        display_axis = self._encoding['x'].get('axis', True) if self._encoding.get('x') else False
        if display_axis:  # Display axis if key not found (default display axis) or True
            axis_specs['x']['start'] = '0 0 0'
            axis_specs['x']['end'] = f'{DEFAULT_POINT_X_SEPARATION * len(self._raw_data) + self._max_radius} 0 0'

            # Axis labels
            if self._size_data is not None:  # Bubbles plot (the size of the point depends on the value of the field)
                radius = self._set_points_radius()
            else:  # Scatter plot (same radius for all points)
                radius = pl.repeat(
                    value=self._max_radius,
                    n=len(self._raw_data),
                    eager=True  # Returns a Series
                ).alias('radius')

            x_coords = self._set_x_coordinates(radius)  # X-axis value for each point
            y_coords = pl.repeat(
                value=LABELS_Y_DELTA,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            ).alias('y_coords')
            z_coords = pl.repeat(
                value=LABELS_Z_DELTA,
                n=len(self._raw_data),
                eager=True  # Returns a Series
            ).alias('z_coords')
            label_pos_series = pl.select(pl.concat_str(
                [x_coords, y_coords, z_coords],
                separator=' '
            ).fill_null('?').alias('id')).to_series()

            axis_specs['x']['labels_pos'] = label_pos_series.to_list()
            axis_specs['x']['labels_values'] = self._x_data.to_list()
            axis_specs['x']['labels_rotation'] = '-90 0 -90'  # Rotation of the labels

        # ---- Y-axis ----
        # Axis line
        display_axis = self._encoding['y'].get('axis', True) if self._encoding.get('y') else False
        if display_axis:  # Display axis if key not found (default display axis) or True
            axis_specs['y']['start'] = '0 0 0'
            axis_specs['y']['end'] = f'0 {self._height} 0'

            # Axis labels
            y_coords = pl.linear_space(  # Equally spaced values
                start=self._height / Y_NUM_OF_TICKS,  # The lower label does not start in the ground
                end=self._height,
                num_samples=Y_NUM_OF_TICKS,
                eager=True  # Returns a Series
            ).alias('y_coords')
            label_values = pl.linear_space(  # Equally spaced values
                start=self._y_data.max() / Y_NUM_OF_TICKS,
                end=self._y_data.max(),
                num_samples=Y_NUM_OF_TICKS,
                eager=True  # Returns a Series
            ).round(2)  # Round to the second decimal

            x_coords = pl.repeat(
                value=Y_LABELS_X_DELTA,
                n=Y_NUM_OF_TICKS,
                eager=True  # Returns a Series
            ).alias('x_coords')
            z_coords = pl.repeat(
                value=0,
                n=Y_NUM_OF_TICKS,
                eager=True  # Returns a Series
            ).alias('z_coords')
            label_pos_series = pl.select(pl.concat_str(
                [x_coords, y_coords, z_coords],
                separator=' '
            ).fill_null('?').alias('id')).to_series()

            axis_specs['y']['labels_pos'] = label_pos_series.to_list()
            axis_specs['y']['labels_values'] = label_values.to_list()
            axis_specs['y']['labels_rotation'] = '0 0 0'

        # ---- Z-axis ----
        # Axis line
        display_axis = self._encoding['z'].get('axis', True) if self._encoding.get('z') else False
        if display_axis:  # Display axis if key 'axis' not found (default display axis) or True
            axis_specs['z']['start'] = '0 0 0'
            axis_specs['z']['end'] = f'0 0 {-DEFAULT_MAX_DEPTH}'

            # Axis labels
            categories = self._z_data.unique()

            x_coords = pl.repeat(
                value=Z_LABELS_X_DELTA,
                n=len(categories),
                eager=True  # Returns a Series
            ).alias('x_coords')
            y_coords = pl.repeat(
                value=LABELS_Y_DELTA,
                n=len(categories),
                eager=True  # Returns a Series
            ).alias('y_coords')
            z_coords = self._set_z_coordinates().unique()  # Z-axis coordinates for labels (aligned with centers)
            label_pos_series = pl.select(pl.concat_str(
                [x_coords, y_coords, z_coords],
                separator=' ',
            ).fill_null('?').alias('id')).to_series()

            axis_specs['z']['labels_pos'] = label_pos_series.to_list()
            axis_specs['z']['labels_values'] = categories.to_list()
            axis_specs['z']['labels_rotation'] = '-90 0 0'

        return axis_specs
