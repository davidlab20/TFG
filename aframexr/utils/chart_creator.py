import polars as pl
import warnings

from itertools import cycle, islice
from polars import DataFrame, Series
from polars.datatypes.group import NUMERIC_DTYPES
from typing import Literal

from .axis_creator import AxisCreator
from .constants import *
from .element_creator import (
    BoxCreator, CylinderCreator, ElementCreator, PlaneCreator, SphereCreator, TextCreator, LineCreator
)

CREATOR_MAP: dict[str, type['ChartCreator']] = {}  # Creator map of charts, classes are added at the end of this file


def _calculate_point_radius(point_volume: float) -> float:
    return (3 * point_volume / (4 * 3.1416)) ** (1 / 3)


def _translate_dtype_into_encoding(dtype: pl.DataType) -> str:
    """Translates and returns the encoding for a given data type."""

    if dtype in NUMERIC_DTYPES:
        encoding_type = 'quantitative'
    elif dtype in (pl.String, pl.Categorical):
        encoding_type = 'nominal'
    else:
        raise ValueError(f'Unknown dtype: {dtype}.')
    return encoding_type


class ChartCreator:
    """Chart creator base class"""

    def __init__(self, chart_specs: dict):
        base_position = chart_specs.get('position', DEFAULT_CHART_POS)
        [self._base_x, self._base_y, self._base_z] = [float(pos) for pos in base_position.split()]  # Base position
        self._encoding = chart_specs.get('encoding')  # Encoding and parameters of the chart
        rotation = chart_specs.get('rotation', DEFAULT_CHART_ROTATION)  # Rotation of the chart
        [self._x_rotation, self._y_rotation, self._z_rotation] = [float(rot) for rot in rotation.split()]
        self._params = chart_specs.get('params', [])  # Metadata parameters
        self._process_params()
        self._raw_data = DataFrame(chart_specs['data']['values'])

        self._elements_colors_all = chart_specs['mark'].get('color', DEFAULT_ELEMENTS_COLOR_IN_CHART) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_ELEMENTS_COLOR_IN_CHART
        self._color_data: Series | None = None
        self._color_encoding: str = ''

        self._chart_depth = chart_specs.get('depth')  # Maximum depth of the chart

        self._title = chart_specs.get('title')
        # Each self._{channel} attributes must be named by child classes

    def _add_selection_to_specs(self, specs: dict) -> None:
        if not getattr(self, "_selection", None):
            return

        param_name = self._selection['name']
        select_fields = self._selection['fields']

        expressions = [pl.lit(param_name)] + [
            pl.col(f).cast(pl.Utf8).fill_null("")
            for f in select_fields
        ]
        specs['activates_param'] = self._raw_data.select(
            pl.concat_str(expressions, separator="__")
        ).to_series().to_list()

    def _process_channels(self, *channels_name: str):
        """
        Process and stores the necessary channels' information.
        Must have defined self._{ch}_data and self._{ch}_encoding.
        """
        if self._raw_data.is_empty():
            return

        for ch in channels_name:
            if self._encoding.get(ch):
                channel_encoding = self._encoding[ch]
                field = channel_encoding['field']  # Field of the channel
                try:
                    data = self._raw_data[field]

                    detected_encoding = _translate_dtype_into_encoding(data.dtype)
                    user_encoding = channel_encoding.get('type', detected_encoding)
                    setattr(self, f'_{ch}_encoding', user_encoding)

                    # Set value for self._{ch}_data
                    if user_encoding == 'nominal' and detected_encoding == 'quantitative':
                        setattr(self, f'_{ch}_data', data.cast(pl.String))
                    else:
                        setattr(self, f'_{ch}_data', data)
                except pl.exceptions.ColumnNotFoundError:
                    raise KeyError(f'Data has no field "{field}" for {ch}-channel.')

    def _process_params(self):
        for p in self._params:
            if 'select' in p and p['select']['type'] == 'point':
                self._selection = {
                    'name': p['name'],
                    'fields': p['select'].get('fields', [])
                }

    def _set_elements_colors(self) -> Series:
        """Returns a Series of the color for each element composing the chart."""
        if self._color_encoding and self._color_encoding != 'nominal':
            raise ValueError(ERROR_MESSAGES['COLOR_ENCODING_NOT_NOMINAL'].format(color_encoding=self._color_encoding))

        if self._color_data is None:
            points_colors = pl.repeat(
                value=self._elements_colors_all,
                n=self._raw_data.height,  # Number of rows in data
                eager=True  # Returns a Series
            )
        else:
            unique_categories = self._color_data.unique(maintain_order=True).to_list()
            color_map = dict(zip(
                unique_categories,
                islice(cycle(AVAILABLE_COLORS), len(unique_categories))
            ))

            points_colors = self._color_data.replace(color_map)
        return points_colors.alias('color')

    def _set_info(self, *hud_elements: Series) -> Series:
        info_exprs = []
        for i, e in enumerate(hud_elements):
            if e is not None:
                col_name = e.name
                info_exprs.append(
                    pl.concat_str([pl.lit(f'{col_name}: '), pl.col(col_name).cast(pl.String)])
                )

        info = self._raw_data.select(
            pl.concat_str(info_exprs, separator='; ').fill_null('?').alias('info')
        ).to_series()

        return info

    @staticmethod
    def create_object(chart_type: str, chart_specs: dict):
        """Returns a ChartCreator instance of the specific chart type."""
        try:
            creator = CREATOR_MAP[chart_type]
        except KeyError:  # pragma: no cover (creator classes should be added at the end of this file)
            raise RuntimeError(f'Class for {chart_type} was not added to CREATOR_MAP')
        return creator(chart_specs)

    def get_relative_bottom_left_corner_position(self) -> str:
        """Returns the relative position for the bottom left corner of the chart."""
        # Only XYZAxisChannelChartCreator objects has that attribute, if not return '0 0 0'
        return getattr(self, '_relative_bottom_left_corner_position', '0 0 0')

    def get_axes_specs(self):  # pragma: no cover (get_axes_specs() must be implemented by child classes)
        raise RuntimeError('Unreachable code. Method get_axes_specs() must be implemented by child classes')

    def get_elements(self, filtered_by_params: bool) -> list[ElementCreator]:  # pragma: no cover
        raise RuntimeError('Unreachable code. Method get_elements() must be implemented by child classes')

    def get_group_specs(self) -> dict:
        """Returns a dictionary with the base specifications for the group of elements."""
        group_specs = {
            'position': f'{self._base_x} {self._base_y} {self._base_z}',
            'rotation': f'{self._x_rotation} {self._y_rotation} {self._z_rotation}'
        }

        return group_specs

    def get_legend_elements(self, filtered_by_params: bool = False) -> list[ElementCreator]:
        return []  # This method is redefined in charts that could have legend

    def get_title_elements(self, filtered_by_params: bool = False) -> list[ElementCreator]:
        if not self._title:
            return []

        # Relative title position
        if getattr(self, '_chart_width', None) is not None and getattr(self, '_chart_height', None) is not None:
            chart_height = getattr(self, '_chart_height')
            chart_width = getattr(self, '_chart_width')
            rotation = '0 0 0'
            title_position = f'{chart_width / 2} {chart_height + PLANE_TITLE_SEPARATION + PLANE_TITLE_HEIGHT / 2} 0'
        elif getattr(self, '_radius', None) is not None:  # Pie chart
            chart_height = chart_width = getattr(self, '_radius') * 2
            rotation = '90 0 0'  # Invert pie chart's rotation (-90 0 0)
            title_position = f'0 0 {chart_height / 2 + PLANE_TITLE_SEPARATION + PLANE_TITLE_HEIGHT / 2}'  # Z-axis
        else:  # pragma: no cover
            raise RuntimeError('Unreachable code')

        plane = PlaneCreator(
            {
                'position': title_position, 'rotation': rotation, 'height': PLANE_TITLE_HEIGHT, 'width': chart_width
            },
            filtered_by_params=filtered_by_params
        )
        text = TextCreator(
            {
                'position': title_position, 'rotation': rotation, 'value': self._title, 'color': TITLE_TEXT_COLOR,
                'align': 'center', 'scale': TITLE_TEXT_SCALE
            },
            filtered_by_params=filtered_by_params
        )

        return [plane, text]


# First-level subclasses of ChartCreator.
class XYZAxisChannelChartCreator(ChartCreator):
    """
    Chart creator base class for charts that have channels and XYZ axis.

    Notes
    -----
    XYZ-axes are processed instantly when creating this class or derivatives.
    """

    _AXIS_SIZE_MAP = {'x': 'width', 'y': 'height', 'z': 'depth'}

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._chart_height = chart_specs.get('height')  # Maximum height of the chart
        self._chart_width = chart_specs.get('width')  # Maximum width of the chart

        self._x_elements_coordinates: Series | None = None
        self._x_data: Series | None = None
        self._x_encoding: str = ''
        self._x_offset: float = 0

        self._y_elements_coordinates: Series | None = None
        self._y_data: Series | None = None
        self._y_encoding: str = ''
        self._y_offset: float = 0

        self._z_elements_coordinates: Series | None = None
        self._z_data: Series | None = None
        self._z_encoding: str = ''
        self._z_offset: float = 0

        self._process_channels('color', 'x', 'y', 'z')  # Process and set self._{axis} attributes

    def _apply_axis_offset(self, coordinates: Series, axis: str, invert: bool = False,
                           extra_offset: float = 0) -> Series:
        min_val = coordinates.min()
        offset = abs(min_val) + extra_offset if min_val < 0 else 0

        if invert:
            result = -(offset + coordinates)
            setattr(self, f'_{axis}_offset', -offset)
        else:
            result = offset + coordinates
            setattr(self, f'_{axis}_offset', offset)

        setattr(self, f'_{axis}_elements_coordinates', result)
        return result

    def _correct_axes_position(self, elem_size: float | None) -> None:
        """
        Corrects the axes' position for inner the calculations and processing.
        Must be called by child classes when initiating.
        """

        def _calculate_axis_size(axis_data: Series, default_axis_size: float) -> float:
            if elem_size is None or axis_data is None:  # User did not define bars' size, or there is no data
                return default_axis_size  # Set default value

            if _translate_dtype_into_encoding(axis_data.dtype) == 'quantitative':
                return default_axis_size  # User did not define bars' size or axis is quantitative

            return elem_size * axis_data.n_unique()

        # X-axis
        if self._chart_width is None:  # User did not define chart width
            self._chart_width = _calculate_axis_size(self._x_data, DEFAULT_CHART_WIDTH)

        # Y-axis
        if self._chart_height is None:  # User did not define chart height
            self._chart_height = _calculate_axis_size(self._y_data, DEFAULT_CHART_HEIGHT)

        # Z-axis
        if self._chart_depth is None:  # User did not define chart depth
            self._chart_depth = _calculate_axis_size(self._z_data, DEFAULT_CHART_DEPTH)

        self._relative_bottom_left_corner_position = (
            f'{-self._chart_width / 2} '
            f'{-self._chart_height / 2} '
            f'{self._chart_depth / 2}'
        )

    def get_axes_specs(self) -> dict:
        """Returns a dictionary with the specifications for each axis of the chart."""
        if self._raw_data.is_empty():  # There is no data to display
            return {}

        axis_specs = {}

        for axis in ('x', 'y', 'z'):  # type: Literal['x', 'y', 'z']
            encoding = self._encoding.get(axis)
            if not encoding:
                continue

            if not encoding.get('axis', True):
                continue  # Display axis if key 'axis' not found (default display axis) or True

            axis_specs[axis] = AxisCreator.create_axis_specs(
                axis=axis,
                axis_data=getattr(self, f'_{axis}_data'),
                axis_encoding=getattr(self, f'_{axis}_encoding'),
                axis_size=getattr(self, f'_chart_{self._AXIS_SIZE_MAP[axis]}'),
                elements_coords=getattr(self, f'_{axis}_elements_coordinates'),
                x_offset=0 if axis == 'x' else self._x_offset,
                y_offset=0 if axis == 'y' else self._y_offset,
                z_offset=0 if axis == 'z' else self._z_offset,
            )

        return axis_specs

    def get_legend_elements(self, filtered_by_params: bool = False) -> list[ElementCreator]:
        """Returns a list for the elements of the legend."""
        if self._color_data is None:
            return []

        color_mapping = {}
        colors = self._set_elements_colors()
        for m, c in zip(self._color_data, colors):
            color_mapping.setdefault(m, c)

        center_x_pos = self._chart_width + LEGEND_WIDTH - 1

        # Plane
        plane_height = LEGEND_HEIGHT_PER_ELEMENT * len(color_mapping)
        plane = PlaneCreator({
            'position': f'{center_x_pos} {self._chart_height / 2} 0',
            'height': plane_height, 'width': LEGEND_WIDTH
        }, filtered_by_params=filtered_by_params)

        # Text
        text_base_y = self._chart_height / 2 - plane_height / 2 + LEGEND_HEIGHT_PER_ELEMENT / 2
        text = [
            TextCreator({
                'position': f'{center_x_pos} {text_base_y + LEGEND_HEIGHT_PER_ELEMENT * index} 0',
                'value': item[0].title(), 'color': item[1],
                'align': 'center', 'scale': LABELS_SCALE
            }, filtered_by_params=filtered_by_params)
            for index, item in enumerate(color_mapping.items())
        ]

        return [plane, *text]

    @staticmethod
    def set_elems_coordinates_for_quantitative_axis(axis_data: Series, axis_size: float,
                                                    extremes_offset: float) -> Series:
        """
        Returns a Series with the positions for each element in the quantitative axis.

        Parameters
        ----------
        axis_data: Series
            The data of the quantitative axis.
        axis_size : float
            The total size of the axis.
        extremes_offset : float
            The offset used in each extreme of the axis, so the elements do not exceed the chart dimensions.
        """
        if axis_data.dtype == pl.String:
            axis_data = axis_data.cast(pl.Categorical).to_physical()

        max_value, min_value = axis_data.max(), axis_data.min()  # For proportions
        range_value = max_value - min_value  # Range (positive value)
        if range_value == 0:  # All the values are the same
            return pl.repeat(
                value=axis_size / 2,  # Center elements in the axis
                n=axis_data.len(),
                eager=True  # Returns a Series
            )

        usable_axis_size = axis_size - (2 * extremes_offset)  # Reduce the axis space size
        if max_value < 0:  # All data is negative
            scale_factor = usable_axis_size / -min_value
            final_offset = -extremes_offset  # Negative offset
        elif min_value >= 0:  # All data is positive (including 0)
            scale_factor = usable_axis_size / max_value
            final_offset = extremes_offset  # Positive offset
        else:  # Positive and negative data
            scale_factor = usable_axis_size / range_value
            final_offset = 0
        return axis_data * scale_factor + final_offset  # Add final offset to center

    @staticmethod
    def set_elems_coordinates_for_nominal_axis(axis_data: Series, axis_size: float, extremes_offset: float) -> Series:
        """
        Returns a Series with the positions for each element in the nominal axis.

        Parameters
        ----------
        axis_data : Series
            The data of the nominal axis.
        axis_size : float
            The total size of the axis.
        extremes_offset : float
            The offset used in each extreme of the axis, so the elements do not exceed the chart dimensions.
        """
        category_codes = axis_data.cast(pl.Categorical).to_physical()
        unique_categories = axis_data.n_unique()

        step = (axis_size - 2 * extremes_offset) / (unique_categories - 1) if unique_categories > 1 else 0
        return (extremes_offset + step * category_codes).cast(pl.Float32)


class NonAxisChannelChartCreator(ChartCreator):
    """Chart creator base class for charts that have channels but do not have XYZ axis."""

    def get_axes_specs(self):
        """Returns a Series with the specifications for each axis of the chart."""
        return {}  # Returns an empty dictionary, because it has no axis


# Second-level subclasses of ChartCreator.
class ArcChartCreator(NonAxisChannelChartCreator):
    """Arc chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._radius = chart_specs['mark'].get('radius', DEFAULT_PIE_RADIUS) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_PIE_RADIUS
        self._set_rotation()

        self._theta_data: Series | None = None
        self._theta_encoding: str = ''

        self._process_channels('color', 'theta')

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
        theta_length = (360 / sum_data) * abs_theta_data  # Series of theta lengths (in degrees)
        theta_start = theta_length.cum_sum().shift(1).fill_null(0)  # Accumulative sum (first value is 0)
        return theta_start.alias('theta_start'), theta_length.alias('theta_length')

    def get_elements(self, filtered_by_params: bool) -> list[ElementCreator]:
        """Returns a list of each element composing the chart."""
        if self._raw_data.is_empty():  # There is no data to display
            return []

        data_length = self._raw_data.height  # Number of rows in data

        # Axis
        zeros = pl.repeat(0, data_length, eager=True)
        x_coordinates = y_coordinates = z_coordinates = zeros

        # Color and theta
        if self._theta_encoding != 'quantitative':
            raise ValueError('Theta-channel data must be quantitative')

        colors = self._set_elements_colors()
        theta_starts, theta_lengths = self._set_elements_theta()

        # Depth
        depth = pl.repeat(
            value=self._chart_depth,
            n=data_length,
            eager=True  # Returns a Series
        ).alias('depth')

        # Radius
        radius = pl.repeat(
            value=self._radius,
            n=data_length,
            eager=True  # Returns a Series
        ).alias('radius')

        # Information display
        info = self._set_info(self._color_data, self._theta_data)

        # Return values
        temp_dict = {
            'info': info,
            'height': depth,  # Using height, as pie's slices are rotated cylinders
            'position': pl.select(pl.concat_str(
                [x_coordinates, y_coordinates, z_coordinates],
                separator=' '
            ).alias('position')).to_series(),
            'radius': radius,
            'theta_start': theta_starts,
            'theta_length': theta_lengths,
            'color': colors
        }

        # Selection
        self._add_selection_to_specs(temp_dict)

        elements_specs = pl.from_dict(temp_dict).to_dicts()  # Transform into a list of dictionaries
        return [
            CylinderCreator(specification, filtered_by_params=filtered_by_params)
            for specification in elements_specs
        ]


class BarChartCreator(XYZAxisChannelChartCreator):
    """Bar chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._bar_size_if_nominal_axis: float | None = chart_specs['mark'].get('size') \
            if isinstance(chart_specs['mark'], dict) else None
        self._correct_axes_position(elem_size=self._bar_size_if_nominal_axis)

    def _set_bars_coords_size_in_axis(self, axis_data: Series, axis_name: Literal['x', 'y', 'z'],
                                      encoding_type: str) -> tuple[Series, Series]:
        """
        Returns a tuple of Series.
        The first contains the axis coordinates of each bar for the given axis.
        The second contains the dimensions of each bar for the given axis.
        """
        try:
            axis_size = getattr(self, f'_chart_{self._AXIS_SIZE_MAP[axis_name]}')  # Get axis dimension
            bars_size_alias = self._AXIS_SIZE_MAP[axis_name]  # Get alias of bar size Series depending on axis
        except KeyError:  # pragma: no cover (should never enter here, except code errors)
            raise RuntimeError('Unreachable code. Axis must be x or y or z')

        if axis_data is None:
            coordinates = pl.repeat(
                value=axis_size / 2,
                n=self._raw_data.height,  # Number of rows in data
                eager=True  # Returns a Series
            )
            bars_axis_size = 2 * coordinates  # Multiplied by 2 because of how boxes are created
        else:
            if encoding_type == 'quantitative':
                coordinates = 0.5 * self.set_elems_coordinates_for_quantitative_axis(  # Half because of bar's creation
                    axis_data=axis_data,
                    axis_size=axis_size,
                    extremes_offset=0  # The greatest bar reaches axis size
                )
                bars_axis_size = 2 * coordinates.abs()
            elif encoding_type == 'nominal':
                unique_values = axis_data.n_unique()
                if self._bar_size_if_nominal_axis is not None:  # User defined bars' size
                    if self._bar_size_if_nominal_axis * unique_values > axis_size:  # Bars would overlap
                        bar_size = axis_size / unique_values  # Adjust bars' axis size automatically
                        warnings.warn(
                            f'Defined bar size will make bars overlap on the {axis_name}-axis, adjusting automatically '
                            f'for this axis. Consider changing {bars_size_alias}.'
                        )

                    else:  # Bars do not overlap with user's defined size
                        bar_size = self._bar_size_if_nominal_axis  # Use user's defined size
                else:  # User did not define bars' size
                    bar_size = axis_size / unique_values * (1 - DEFAULT_BAR_PADDING)  # Adjust bars' axis size

                coordinates = self.set_elems_coordinates_for_nominal_axis(
                    axis_data=axis_data, axis_size=axis_size,
                    extremes_offset=bar_size / 2
                )
                bars_axis_size = pl.repeat(
                    value=bar_size,
                    n=axis_data.len(),
                    eager=True  # Returns a Series
                )
            else:
                raise ValueError(f'Invalid encoding type: {encoding_type}.')
        return coordinates.alias(f'{axis_name}_coordinates'), bars_axis_size.alias(bars_size_alias)

    def get_elements(self, filtered_by_params: bool) -> list[ElementCreator]:
        """Returns a list of each element composing the chart."""
        if self._raw_data.is_empty():  # There is no data to display
            return []

        # XYZ-axis
        x_coordinates, bar_widths = self._set_bars_coords_size_in_axis(
            axis_data=self._x_data, axis_name='x', encoding_type=self._x_encoding
        )
        self._apply_axis_offset(x_coordinates, 'x')

        y_coordinates, bar_heights = self._set_bars_coords_size_in_axis(
            axis_data=self._y_data, axis_name='y', encoding_type=self._y_encoding
        )
        self._apply_axis_offset(y_coordinates, 'y')

        z_coordinates, bar_depths = self._set_bars_coords_size_in_axis(
            axis_data=self._z_data, axis_name='z', encoding_type=self._z_encoding
        )
        self._apply_axis_offset(z_coordinates, 'z', invert=True)  # Invert sign (to go deep)

        # Color
        colors = self._set_elements_colors()

        # Information display
        info = self._set_info(self._x_data, self._y_data, self._z_data)

        # Return values
        temp_dict = {
            'info': info,
            'position': pl.select(pl.concat_str(
                [self._x_elements_coordinates, self._y_elements_coordinates, self._z_elements_coordinates],
                separator=' '
            ).alias('position')).to_series(),
            'width': bar_widths,
            'height': bar_heights,
            'depth': bar_depths,
            'color': colors
        }

        # Selection
        self._add_selection_to_specs(temp_dict)

        elements_specs = pl.from_dict(temp_dict).to_dicts()  # Transform into a list of dictionaries
        return [
            BoxCreator(specification, filtered_by_params=filtered_by_params)
            for specification in elements_specs
        ]


class LineChartCreator(XYZAxisChannelChartCreator):
    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        self._correct_axes_position(elem_size=DEFAULT_VERTICES_SPACING)
        self._line_color = chart_specs['mark'].get('color', DEFAULT_ELEMENTS_COLOR_IN_CHART) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_ELEMENTS_COLOR_IN_CHART
        self._display_points_in_vertices = chart_specs['mark'].get('point', DEFAULT_VERTICES_POINT_DISPLAY) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_VERTICES_POINT_DISPLAY
        self._marker_bbox_size_half = _calculate_point_radius(DEFAULT_VERTICES_POINT_VOLUME) \
            if self._display_points_in_vertices else 0  # Half of the markers bounding box's axes size

    def _set_extremes_coords_in_axis(self, axis_data: Series, axis_name: Literal['x', 'y', 'z'],
                                     encoding_type: str) -> Series:
        """Returns a Series containing the coordinates for each extreme of the line, for the given axis."""
        attr_name = self._AXIS_SIZE_MAP.get(axis_name)
        if not attr_name:  # pragma: no cover (this method is internally called)
            raise RuntimeError('Unreachable code. Parameter axis_name is not correct')

        axis_size = getattr(self, f'_chart_{attr_name}')  # Get axis dimensions depending on the given axis

        if axis_data is None:
            coordinates = pl.repeat(
                value=self._marker_bbox_size_half,
                n=self._raw_data.height,  # Number of rows in data
                eager=True  # Returns a Series
            )
        else:
            if encoding_type == 'quantitative':
                coordinates = self.set_elems_coordinates_for_quantitative_axis(
                    axis_data=axis_data,
                    axis_size=axis_size,
                    extremes_offset=self._marker_bbox_size_half
                )
            elif encoding_type == 'nominal':
                coordinates = self.set_elems_coordinates_for_nominal_axis(
                    axis_data=axis_data, axis_size=axis_size,
                    extremes_offset=self._marker_bbox_size_half
                )
            else:
                raise ValueError(f'Invalid encoding type: {encoding_type}.')
        return coordinates.alias(f'{axis_name}_coordinates')

    def get_elements(self, filtered_by_params: bool) -> list[ElementCreator]:
        """Returns a list of each element composing the chart."""
        if self._raw_data.is_empty():  # There is no data to display
            return []

        x_coordinates = self._set_extremes_coords_in_axis(self._x_data, axis_name='x', encoding_type=self._x_encoding)
        self._apply_axis_offset(x_coordinates, 'x')

        y_coordinates = self._set_extremes_coords_in_axis(self._y_data, axis_name='y', encoding_type=self._y_encoding)
        self._apply_axis_offset(y_coordinates, 'y')

        z_coordinates = self._set_extremes_coords_in_axis(self._z_data, axis_name='z', encoding_type=self._z_encoding)
        self._apply_axis_offset(z_coordinates, 'z', invert=True)  # Invert sign (to go deep)

        # Colors
        colors = self._set_elements_colors()

        # Positions
        positions = pl.select(pl.concat_str(
            [self._x_elements_coordinates, self._y_elements_coordinates, self._z_elements_coordinates],
            separator=' '
        ).alias('position')).to_series()

        # Lines
        lines_df = (
            pl.DataFrame({'start': positions, 'color': colors})
            .with_columns(pl.col('start').shift(-1).over('color').alias('end'))  # Shift one position up (of same color)
            .drop_nulls('end')  # Remove last row (NULL value)
        )

        # Points
        info = self._set_info(self._x_data, self._y_data, self._z_data)

        points_df = pl.DataFrame({
            'position': positions,
            'info': info,
            'color': colors,
            'radius': pl.repeat(
                _calculate_point_radius(DEFAULT_VERTICES_POINT_VOLUME),
                n=self._raw_data.height,
                eager=True
            )
        })

        # Selection
        for df in (lines_df, points_df):
            self._add_selection_to_specs(df.to_dict(as_series=False))

        # Return elements
        elements_lines = [LineCreator(spec, filtered_by_params=filtered_by_params) for spec in lines_df.to_dicts()]
        elements_points = (
            [SphereCreator(spec, filtered_by_params=filtered_by_params) for spec in points_df.to_dicts()]
            if self._display_points_in_vertices
            else []
        )

        return elements_lines + elements_points

class PointChartCreator(XYZAxisChannelChartCreator):
    """Point chart creator class."""

    def __init__(self, chart_specs: dict):
        super().__init__(chart_specs)
        max_sphere_volume: float = chart_specs['mark'].get('size', DEFAULT_POINT_VOLUME) \
            if isinstance(chart_specs['mark'], dict) else DEFAULT_POINT_VOLUME
        self._max_radius = _calculate_point_radius(max_sphere_volume)
        self._correct_axes_position(elem_size=self._max_radius * 2)

        self._size_data: Series | None = None
        self._size_encoding: str = ''

        self._process_channels('size')  # Process and set self._{ch} attributes

    def _set_points_coords_in_axis(self, axis_data: Series, axis_name: Literal['x', 'y', 'z'],
                                   encoding_type: str) -> Series:
        """Returns a Series containing the coordinates for each point of the chart, for the given axis."""
        attr_name = self._AXIS_SIZE_MAP.get(axis_name)
        if not attr_name:  # pragma: no cover (this method is internally called)
            raise RuntimeError('Unreachable code. Parameter axis_name is not correct')

        axis_size = getattr(self, f'_chart_{attr_name}')  # Get axis dimensions depending on the given axis

        if axis_data is None:
            coordinates = pl.repeat(
                value=axis_size / 2,  # Center points in the axis
                n=self._raw_data.height,  # Number of rows in data
                eager=True  # Returns a Series
            )
        else:
            if encoding_type == 'quantitative':
                coordinates = self.set_elems_coordinates_for_quantitative_axis(
                    axis_data=axis_data,
                    axis_size=axis_size,
                    extremes_offset=self._max_radius + EPSILON  # Points do not exceed the dimensions of the axis
                )
            elif encoding_type == 'nominal':
                coordinates = self.set_elems_coordinates_for_nominal_axis(
                    axis_data=axis_data, axis_size=axis_size,
                    extremes_offset=self._max_radius + EPSILON  # Points do not exceed the dimensions of the axis
                )
            else:
                raise ValueError(f'Invalid encoding type: {encoding_type}.')
        return coordinates.alias(f'{axis_name}_coordinates')

    def _set_points_radius(self) -> Series:
        """Returns a Series of the radius for each point composing the bubble chart."""
        if self._size_encoding and self._size_encoding != 'quantitative':
            raise ValueError(ERROR_MESSAGES['SIZE_ENCODING_NOT_QUANTITATIVE'].format(size_encoding=self._size_encoding))

        if self._size_data is None:  # Scatter plot (same radius for all points)
            points_radius = pl.repeat(
                value=self._max_radius,  # Same radius for all points
                n=self._raw_data.height,  # Number of rows in data
                eager=True  # Returns a Series
            )
        else:  # Bubbles plot (the size of the point depends on the value of the field)
            max_value = self._size_data.max()
            points_radius = (self._size_data / max_value) * self._max_radius
        return points_radius.alias('radius')

    def get_elements(self, filtered_by_params: bool) -> list[ElementCreator]:
        """Returns a list of each element composing the chart."""
        if self._raw_data.is_empty():  # There is no data to display
            return []

        # Channels
        colors = self._set_elements_colors()
        radius = self._set_points_radius()

        x_coordinates = self._set_points_coords_in_axis(
            axis_data=self._x_data, axis_name='x', encoding_type=self._x_encoding
        )
        self._apply_axis_offset(x_coordinates, 'x', extra_offset=self._max_radius)

        y_coordinates = self._set_points_coords_in_axis(
            axis_data=self._y_data, axis_name='y', encoding_type=self._y_encoding
        )
        self._apply_axis_offset(y_coordinates, 'y', extra_offset=self._max_radius)

        z_coordinates = self._set_points_coords_in_axis(
            axis_data=self._z_data, axis_name='z', encoding_type=self._z_encoding
        )
        self._apply_axis_offset(z_coordinates, 'z', invert=True, extra_offset=self._max_radius)  # Invert (go deep)

        # Information display
        info = self._set_info(self._x_data, self._y_data, self._z_data, self._size_data)

        # Return values
        temp_dict = {
            'info': info,
            'position': pl.select(pl.concat_str(
                [self._x_elements_coordinates, self._y_elements_coordinates, self._z_elements_coordinates],
                separator=' '
            ).alias('position')).to_series(),
            'radius': radius,
            'color': colors,
        }

        # Selection
        self._add_selection_to_specs(temp_dict)

        elements_specs = pl.from_dict(temp_dict).to_dicts()  # Transform into a list of dictionaries
        return [
            SphereCreator(specifications, filtered_by_params=filtered_by_params)
            for specifications in elements_specs
        ]


# Add classes to CREATOR_MAP
CREATOR_MAP.update({
    'arc': ArcChartCreator,
    'bar': BarChartCreator,
    'line': LineChartCreator,
    'point': PointChartCreator,
})
