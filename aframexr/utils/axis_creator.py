"""AframeXR axis creator"""

import copy
import polars as pl

from polars import Series
from typing import Literal, Final

from aframexr.utils.constants import *


AXIS_DICT_TEMPLATE = {'start': None, 'end': None, 'labels_pos': [], 'labels_values': [], 'labels_rotation': '',
                      'labels_align': None}
"""Template for each axis."""

_X_AXIS_LABELS_ROTATION: Final = '-90 0 -90'
_Y_AXIS_LABELS_ROTATION: Final = '0 0 0'
_Z_AXIS_LABELS_ROTATION: Final = '-90 0 0'


def _get_labels_coords_for_quantitative_axis(axis_data: Series, axis_size: float) -> Series:
    """Returns the coordinates for the labels of the quantitative axis."""

    if axis_data.dtype == pl.String:  # Axis data contains nominal values, but user wants to encode as quantitative
        coords = pl.linear_space(  # Equally spaced values
            start=START_LABEL_OFFSET,  # Offset for the lowest label (for not being on the ground)
            end=axis_size,
            num_samples=axis_data.n_unique(),  # Same number of ticks as unique categories
            eager=True  # Returns a Series
        )
    else:
        coords = pl.linear_space(  # Equally spaced values
            start=START_LABEL_OFFSET,  # Offset for the lowest label (for not being on the ground)
            end=axis_size,
            num_samples=DEFAULT_NUM_OF_TICKS_IF_QUANTITATIVE_AXIS,
            eager=True  # Returns a Series
        )
    return coords

def _get_labels_values_for_quantitateve_axis(axis_data: Series) -> Series:
    """Returns the values for the labels of the quantitative axis."""

    if axis_data.dtype == pl.String:  # Axis data contains nominal values, but user wants to encode as quantitative
        return axis_data.unique(maintain_order=True)  # Return the same values

    max_value, min_value = axis_data.max(), axis_data.min()

    if max_value == min_value:
        labels_values = pl.repeat(value=max_value, n=DEFAULT_NUM_OF_TICKS_IF_QUANTITATIVE_AXIS, eager=True)
    else:
        if max_value < 0:  # All data is negative
            start = min_value
            end = 0
        elif min_value > 0:  # All data is positive
            start = 0
            end = max_value
        else:
            start, end = min_value, max_value

        labels_values = pl.linear_space(
            start=start,
            end=end,
            num_samples=DEFAULT_NUM_OF_TICKS_IF_QUANTITATIVE_AXIS,
            eager=True  # Returns a Series
        )
    return labels_values


class AxisCreator:
    """Axis creator class."""

    @staticmethod
    def create_axis_html(start: str | None, end: str | None) -> str:
        """
        Create a line for the axis and returns its HTML.

        Parameters
        ----------
        start : str | None
            The base position of each axis. If None, no axis is displayed.
        end : str | None
            The end position of the axis. If None, no axis is displayed.
        """

        if start and end:
            return f'<a-entity line="start: {start}; end: {end}; color: black"></a-entity>'
        return ''

    @staticmethod
    def create_label_html(pos: str, rotation: str, value: str, align: Literal['left', 'center', 'right']) -> str:
        """
        Create a text with the value of the label in the correct position and returns its HTML.

        Parameters
        ----------
        pos : str
            The position of the label.
        rotation : str
            The rotation of the label (for better visualization).
        value : str
            The value of the label.
        align : Literal['left', 'center', 'right']
            The alignment of the label. The default is 'left'.
        """

        return f'<a-text position="{pos}" rotation="{rotation}" value="{value}" scale="3 3 3" align="{align}"></a-text>'

    @staticmethod
    def create_axis_specs(axis: Literal['x', 'y', 'z'], axis_data: Series, axis_encoding: str, axis_size: float,
                          elements_coords: Series, x_offset: float, y_offset: float, z_offset: float) -> dict:
        """Returns the axis specifications for x, y or z axis depending on its encoding."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)

        if axis_encoding == 'quantitative':
            coords = _get_labels_coords_for_quantitative_axis(axis_data, axis_size)
            labels_values = _get_labels_values_for_quantitateve_axis(axis_data)
        elif axis_encoding == 'nominal':
            coords = elements_coords.unique(maintain_order=True)  # Align labels with elements
            labels_values = axis_data.unique(maintain_order=True)
        else:
            raise ValueError(f'Invalid encoding type: {axis_encoding}.')

        axis_specs['start'] = f'{x_offset} {y_offset} {z_offset}'
        if axis == 'x':
            axis_specs['end'] = f'{axis_size} {y_offset} {z_offset}'
            axis_specs['labels_pos'] = (coords.cast(pl.String) + f' {LABELS_Y_DELTA} {X_LABELS_Z_DELTA}').to_list()
            axis_specs['labels_rotation'] = _X_AXIS_LABELS_ROTATION
            axis_specs['labels_align'] = 'left'
        elif axis == 'y':
            axis_specs['end'] = f'{x_offset} {axis_size} {z_offset}'
            axis_specs['labels_pos'] = (f'{LABELS_X_DELTA} ' + coords.cast(pl.String) + ' 0').to_list()
            axis_specs['labels_rotation'] = _Y_AXIS_LABELS_ROTATION
            axis_specs['labels_align'] = 'right'
        elif axis == 'z':
            axis_specs['end'] = f'{x_offset} {y_offset} {-axis_size}'  # Negative axis size to go deep
            axis_specs['labels_pos'] = (f'{LABELS_X_DELTA} {LABELS_Y_DELTA} ' + coords.cast(pl.String)).to_list()
            axis_specs['labels_rotation'] = _Z_AXIS_LABELS_ROTATION
            axis_specs['labels_align'] = 'right'
        else:
            raise ValueError('Axis must be x or y or z.')

        axis_specs['labels_values'] = labels_values.to_list()
        return axis_specs
