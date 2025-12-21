"""AframeXR axis creator"""

import copy
import polars as pl

from polars import Series
from typing import Literal

from aframexr.utils.constants import *


AXIS_DICT_TEMPLATE = {'start': None, 'end': None, 'labels_pos': [], 'labels_values': [], 'labels_rotation': '',
                      'labels_align': None}
"""Template for each axis."""

_X_AXIS_LABELS_ROTATION = '-90 0 -90'
_Y_AXIS_LABELS_ROTATION = '0 0 0'
_Z_AXIS_LABELS_ROTATION = '-90 0 0'


def _get_labels_coords_for_quantitative_axis(axis_size: float) -> Series:
    """Returns the coordinates for the labels of the quantitative axis."""

    return pl.linear_space(  # Equally spaced values
        start=START_LABEL_OFFSET,  # Offset for the
        end=axis_size,
        num_samples=NUM_OF_TICKS_IF_QUANTITATIVE_AXIS,
        eager=True  # Returns a Series
    )

def _get_labels_values_for_quantitateve_axis(axis_data: Series) -> Series:
    """Returns the values for the labels of the quantitative axis."""

    if axis_data.dtype == pl.String:
        axis_data = axis_data.cast(pl.Categorical).to_physical()

    max_value, min_value = axis_data.max(), axis_data.min()

    if max_value == min_value:
        labels_values = pl.repeat(value=max_value, n=NUM_OF_TICKS_IF_QUANTITATIVE_AXIS, eager=True)
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
            num_samples=NUM_OF_TICKS_IF_QUANTITATIVE_AXIS,
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
    def get_axis_specs_for_quantitative_axis(axis_name: Literal['x', 'y', 'z'], axis_data: Series, x_offset: float,
                                             y_offset: float, z_offset: float, axis_size: float) -> dict:
        """Returns the axis specifications for the quantitative x, y or z axis."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)

        coords = _get_labels_coords_for_quantitative_axis(axis_size)

        axis_specs['start'] = f'{x_offset} {y_offset} {z_offset}'
        if axis_name == 'x':
            axis_specs['end'] = f'{axis_size} {y_offset} {z_offset}'
            axis_specs['labels_pos'] = (coords.cast(pl.String) + f' {LABELS_Y_DELTA} {X_LABELS_Z_DELTA}').to_list()
            axis_specs['labels_rotation'] = _X_AXIS_LABELS_ROTATION
            axis_specs['labels_align'] = 'left'
        elif axis_name == 'y':
            axis_specs['end'] = f'{x_offset} {axis_size} {z_offset}'
            axis_specs['labels_pos'] = (f'{LABELS_X_DELTA} ' + coords.cast(pl.String) + ' 0').to_list()
            axis_specs['labels_rotation'] = _Y_AXIS_LABELS_ROTATION
            axis_specs['labels_align'] = 'right'
        elif axis_name == 'z':
            axis_specs['end'] = f'{x_offset} {y_offset} {-axis_size}'  # Negative axis size to go deep
            coords = -coords  # Negative to go deep
            axis_specs['labels_pos'] = (f'{LABELS_X_DELTA} {LABELS_Y_DELTA} ' + coords.cast(pl.String)).to_list()
            axis_specs['labels_rotation'] = _Z_AXIS_LABELS_ROTATION
            axis_specs['labels_align'] = 'right'
        else:
            raise ValueError('Axis must be x or y or z.')

        labels_values = _get_labels_values_for_quantitateve_axis(axis_data)
        axis_specs['labels_values'] = labels_values.to_list()

        return axis_specs

    @staticmethod
    def get_axis_specs_for_nominal_axis(axis_name: Literal['x', 'y', 'z'], axis_data: Series, axis_elems_coords: Series,
                                        x_offset: float, y_offset: float, z_offset: float, step: float) -> dict:
        """Returns the axis specifications for the nominal x, y or z axis."""

        axis_specs = copy.deepcopy(AXIS_DICT_TEMPLATE)

        unique_axis_data = axis_data.unique(maintain_order=True)  # Take only unique values
        coords = axis_elems_coords.unique(maintain_order=True)  # Same as elements to align labels with elements

        axis_specs['start'] = f'{x_offset} {y_offset} {z_offset}'
        if axis_name == 'x':
            axis_specs['end'] = f'{step * unique_axis_data.len()} {y_offset} {z_offset}'
            axis_specs['labels_pos'] = (coords.cast(pl.String) + f' {LABELS_Y_DELTA} {X_LABELS_Z_DELTA}').to_list()
            axis_specs['labels_rotation'] = _X_AXIS_LABELS_ROTATION
            axis_specs['labels_align'] = 'left'
        elif axis_name == 'y':
            axis_specs['end'] = f'{x_offset} {step * unique_axis_data.len()} {z_offset}'
            axis_specs['labels_pos'] = (f'{LABELS_X_DELTA} ' + coords.cast(pl.String) + ' 0').to_list()
            axis_specs['labels_rotation'] = _Y_AXIS_LABELS_ROTATION
            axis_specs['labels_align'] = 'right'
        elif axis_name == 'z':
            axis_specs['end'] = f'{x_offset} {y_offset} {-step * unique_axis_data.len()}'  # Negative depth to go deep
            coords = -coords  # Negative to go deep
            axis_specs['labels_pos'] = (f'{LABELS_X_DELTA} {LABELS_Y_DELTA} ' + coords.cast(pl.String)).to_list()
            axis_specs['labels_rotation'] = _Z_AXIS_LABELS_ROTATION
            axis_specs['labels_align'] = 'right'
        else:
            raise ValueError('Axis must be x or y or z.')

        axis_specs['labels_values'] = unique_axis_data.to_list()
        return axis_specs
