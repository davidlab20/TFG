"""AframeXR validators"""
from typing import Literal

from .constants import (
    AVAILABLE_AGGREGATES, AVAILABLE_ENCODING_TYPES, AVAILABLE_MARKS, ERROR_MESSAGES
)
from .element_creator import CREATOR_MAP


def _validate_3_axes_numerical_values(param_name: str, param_value: str) -> None:
    """Raises TypeError or ValueError if parameter is not a string of 3 numerical values."""
    AframeXRValidator.validate_type(param_name, param_value, str)

    pos_axes = param_value.strip().split()
    if len(pos_axes) != 3:
        raise ValueError(ERROR_MESSAGES['NOT_3_AXES_POSITION_OR_ROTATION'].format(
            pos_or_rot=param_name, pos_or_rot_value=param_value)
        )
    for axis in pos_axes:
        try:
            float(axis)
        except ValueError:
            raise ValueError(f'The {param_name} values must be numeric.')


def _validate_align(align: Literal['center', 'left', 'right']) -> None:
    """Raises TypeError or ValueError if align is invalid."""
    AframeXRValidator.validate_type('specs.align', align, str)
    if align not in ('center', 'left', 'right'):
        raise ValueError(ERROR_MESSAGES['ALIGN'].format(align=align))


def _validate_data(data: dict) -> None:
    """Raises TypeError or ValueError if data is invalid."""
    AframeXRValidator.validate_type('specs.data', data, dict)
    if 'values' in data and 'url' in data:
        raise ValueError(ERROR_MESSAGES['DATA_WITH_VALUES_AND_URL_IN_SPECS'])

    if 'values' in data:
        values = data['values']
        AframeXRValidator.validate_type('specs.data.values', values, list)
        if not all(isinstance(v, dict) for v in values):
            raise TypeError(ERROR_MESSAGES['NOT_ALL_DATA_VALUES_ARE_DICT'])

    elif 'url' in data:
        AframeXRValidator.validate_type('specs.data.url', data['url'], str)

    else:
        raise ValueError(ERROR_MESSAGES['DATA_WITH_NOT_VALUES_NEITHER_URL_IN_SPECS'])


def _validate_element(element: str) -> None:
    """Raises TypeError or ValueError if element is invalid."""
    AframeXRValidator.validate_type('specs.element', element, str)

    if element not in CREATOR_MAP.keys():
        raise ValueError(ERROR_MESSAGES['ELEMENT_TYPE'].format(element=element))


def _validate_encoding(encoding: dict):
    """Raises TypeError or ValueError if encoding is invalid."""
    AframeXRValidator.validate_type('specs.encoding', encoding, dict)

    if not all(isinstance(e, dict) for e in encoding.values()):
        raise TypeError(ERROR_MESSAGES['NOT_ALL_ENCODINGS_ARE_DICT'])


def _validate_mark(mark: str | dict) -> None:
    """Raises TypeError or ValueError if "mark" is invalid."""
    AframeXRValidator.validate_type('specs.mark', mark, (str, dict))

    mark_type = mark.get('type') if isinstance(mark, dict) else mark
    if mark_type not in AVAILABLE_MARKS:
        raise ValueError(ERROR_MESSAGES['MARK_TYPE'].format(mark_type=mark_type))


def _validate_mark_encoding(mark: str | dict, encoding: dict) -> None:
    """
    Raises ValueError if "mark" and "encoding" combination is invalid.

    Notes
    -----
    Assuming that mark and encoding are valid, as this method is called after mark and encoding validation.
    """
    mark_type = mark.get('type') if isinstance(mark, dict) else mark

    if mark_type in {'bar', 'point'} \
            and sum([encoding.get('x') is not None, encoding.get('y') is not None, encoding.get('z') is not None]) < 2:
        raise ValueError(ERROR_MESSAGES['LESS_THAN_2_XYZ_ENCODING'])
    if mark_type == 'arc' and (encoding.get('color') is None or encoding.get('theta') is None):
        if encoding.get('color') is None:
            raise ValueError(ERROR_MESSAGES['PARAM_NOT_SPECIFIED_IN_MARK_ARC'].format(param='color'))
        if encoding.get('theta') is None:
            raise ValueError(ERROR_MESSAGES['PARAM_NOT_SPECIFIED_IN_MARK_ARC'].format(param='theta'))


def _validate_transform(transform: list[dict]) -> None:
    """Raises TypeError or ValueError if transform is invalid."""
    AframeXRValidator.validate_type('specs.transform', transform, list)

    for t in transform:
        AframeXRValidator.validate_type(f'specs.transform.{t}', t, dict)

        if t.get('filter'):
            AframeXRValidator.validate_type('specs.transform.filter', t['filter'], str)

        elif t.get('aggregate'):
            AframeXRValidator.validate_type('specs.transform.aggregate', t['aggregate'], list)
            for agg in t['aggregate']:
                if 'op' not in agg:
                    raise ValueError(ERROR_MESSAGES['AGGREGATE_OPERATION_NOT_IN_AGGREGATE'])
                AframeXRValidator.validate_aggregate_operation(agg['op'])

        else:
            raise ValueError(ERROR_MESSAGES['TRANSFORM_TYPE'].format(transform_type=t))


class AframeXRValidator:
    """AframeXR validator class."""

    @staticmethod
    def validate_aggregate_operation(aggregate_operation: str) -> None:
        """Raises TypeError or ValueError if aggregate operation is invalid."""
        AframeXRValidator.validate_type('aggregate operation', aggregate_operation, str)
        if aggregate_operation not in AVAILABLE_AGGREGATES:
            raise ValueError(ERROR_MESSAGES['AGGREGATE_OPERATION'].format(operation=aggregate_operation))

    @staticmethod
    def validate_chart_specs(specs: dict) -> None:
        """Raises ValueError if chart specifications are invalid."""
        AframeXRValidator.validate_type('specifications', specs, dict)
        if 'concat' in specs:
            charts = specs['concat']
            AframeXRValidator.validate_type('specs.concat', charts, list)
            for chart_specs in charts:  # There are several charts in the specifications
                AframeXRValidator.validate_chart_specs(chart_specs)  # Validate each chart specification
            return

        if 'mark' in specs and 'element' in specs:
            raise ValueError(ERROR_MESSAGES['MARK_AND_ELEMENT_IN_SPECS'])

        elif 'mark' in specs:  # Chart
            if 'data' not in specs:
                raise ValueError(ERROR_MESSAGES['DATA_NOT_IN_SPECS'])
            _validate_data(specs['data'])
            _validate_mark(specs['mark'])

            if 'encoding' not in specs:
                raise ValueError(ERROR_MESSAGES['ENCODING_NOT_IN_SPECS'])
            _validate_encoding(specs['encoding'])

            _validate_mark_encoding(specs['mark'], specs['encoding'])

        elif 'element' in specs:  # Single element
            _validate_element(specs['element'])

            if 'align' in specs:
                _validate_align(specs['align'])
            if 'color' in specs:
                AframeXRValidator.validate_type('specs.color', specs['color'], str)
            if 'radius' in specs:
                AframeXRValidator.validate_positive_number('specs.radius', specs['radius'])
            if 'radius_bottom' in specs:
                AframeXRValidator.validate_positive_number('specs.radius_bottom', specs['radius_bottom'])
            if 'radius_top' in specs:
                AframeXRValidator.validate_positive_number('specs.radius_top', specs['radius_top'])
            if 'radius_tubular' in specs:
                AframeXRValidator.validate_positive_number('specs.radius_tubular', specs['radius_tubular'])
            if 'scale' in specs:
                _validate_3_axes_numerical_values('specs.scale', specs['scale'])
            if 'src' in specs:
                AframeXRValidator.validate_type('specs.src', specs['src'], str)
            if 'value' in specs:
                AframeXRValidator.validate_type('specs.value', specs['value'], str)

        else:
            raise ValueError(ERROR_MESSAGES['MARK_AND_ELEMENT_NOT_IN_SPECS'])

        if 'position' in specs:
            AframeXRValidator.validate_type('specs.position', specs['position'], str)
            _validate_3_axes_numerical_values('position', specs['position'])

        if 'rotation' in specs:
            AframeXRValidator.validate_type('specs.rotation', specs['rotation'], str)
            _validate_3_axes_numerical_values('rotation', specs['rotation'])

        if 'depth' in specs:
            AframeXRValidator.validate_positive_number('depth', specs['depth'])

        if 'height' in specs:
            AframeXRValidator.validate_positive_number('height', specs['height'])

        if 'width' in specs:
            AframeXRValidator.validate_positive_number('width', specs['width'])

        if 'transform' in specs:
            _validate_transform(specs['transform'])

    @staticmethod
    def validate_encoding_type(encoding_type: str) -> None:
        """Raises TypeError if encoding type is invalid."""
        if encoding_type not in AVAILABLE_ENCODING_TYPES:
            raise ValueError(ERROR_MESSAGES['ENCODING_TYPE'].format(encoding_type=encoding_type))

    @staticmethod
    def validate_positive_number(name: str, value: float | int):
        """Raises TypeError or ValueError if value is not greater than 0."""
        AframeXRValidator.validate_type(name, value, (float, int))
        if value <= 0:
            raise ValueError(ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name=name))

    @staticmethod
    def validate_type(param_name: str, param, types: type | tuple[type, ...]) -> None:
        """Raises TypeError if type(param) is not in types."""
        if not isinstance(param, types):
            if isinstance(types, tuple):
                expected = ' or '.join(t.__name__ for t in types)
            else:
                expected = types.__name__
            raise TypeError(ERROR_MESSAGES['TYPE'].format(
                param_name=param_name, expected_type=expected, current_type=type(param).__name__)
            )
