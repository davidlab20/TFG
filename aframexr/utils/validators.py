"""AframeXR validators"""

from typing import Union

from aframexr.utils.constants import ALL_TEMPLATES, AVAILABLE_AGGREGATES, AVAILABLE_ENCODING_TYPES


class AframeXRValidator:
    """AframeXR validator class."""

    @staticmethod
    def validate_aggregate_operation(aggregate: str) -> None:
        """Raises ValueError if the aggregate operation is invalid."""

        if aggregate not in AVAILABLE_AGGREGATES:
            raise ValueError(f'Invalid aggregate operation: {aggregate}.')

    @staticmethod
    def validate_chart_specs(specs: dict) -> None:
        """Raises ValueError if chart specifications are invalid."""

        if 'concat' in specs:
            for chart_specs in specs['concat']:  # There are several charts in the specifications
                AframeXRValidator.validate_chart_specs(chart_specs)  # Validate each chart specification
            return

        for key in ('data', 'mark'):
            if key not in specs:
                raise ValueError(f'Invalid chart specifications. Must contain key "{key}".')

        mark = specs['mark']
        mark_type = mark['type'] if isinstance(mark, dict) else mark
        if mark_type not in {'image', 'gltf'} and 'encoding' not in specs:
            raise ValueError("Invalid chart specifications. Must contain key 'encoding'.")

    @staticmethod
    def validate_chart_type(chart_type: str) -> None:
        """Raises ValueError if the chart type is invalid."""

        if chart_type not in ALL_TEMPLATES:
            raise ValueError(f'Invalid chart type: {chart_type}.')

    @staticmethod
    def validate_encoding_type(encoding_type: str) -> None:
        """Raises ValueError if encoding type is not valid."""

        if not isinstance(encoding_type, str):
            raise TypeError(f'Expected str, got {type(encoding_type).__name__} instead.')

        if encoding_type not in AVAILABLE_ENCODING_TYPES:
            raise ValueError(f'Invalid encoding type: {encoding_type}.')

    @staticmethod
    def validate_type(param, types: Union[type]) -> None:
        """Raises TypeError if type(param) is not in types."""

        if not isinstance(param, types):
            raise TypeError(f'Expected {types.__name__}, got {type(param).__name__} instead.')