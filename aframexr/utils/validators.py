"""AframeXR validators"""
from aframexr import ELEMENTS_TEMPLATES
from aframexr.utils.constants import AVAILABLE_AGGREGATES, AVAILABLE_ENCODING_TYPES, CHART_TEMPLATES


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
        AframeXRValidator.validate_type(specs, dict)
        if 'concat' in specs:
            for chart_specs in specs['concat']:  # There are several charts in the specifications
                AframeXRValidator.validate_chart_specs(chart_specs)  # Validate each chart specification
            return

        if 'mark' in specs:  # Chart
            if 'data' not in specs:
                raise ValueError(f'Invalid chart specifications. Must contain key "data".')
            mark = specs['mark']
            mark_type = mark['type'] if isinstance(mark, dict) else mark
            if mark_type not in {'image', 'gltf'} and 'encoding' not in specs:
                raise ValueError("Invalid chart specifications. Must contain key 'encoding'.")
        elif 'element' in specs:  # Single element
            pass
        else:
            raise ValueError(f'Invalid chart specifications. Must contain key "mark" or "element".')

    @staticmethod
    def validate_chart_type(chart_type: str) -> None:
        """Raises ValueError if the chart type is invalid."""
        if chart_type not in CHART_TEMPLATES:
            raise ValueError(f'Invalid chart type: {chart_type}.')

    @staticmethod
    def validate_encoding_type(encoding_type: str) -> None:
        """Raises ValueError if encoding type is not valid."""
        if encoding_type not in AVAILABLE_ENCODING_TYPES:
            raise ValueError(f'Invalid encoding type: {encoding_type}.')

    @staticmethod
    def validate_element_type(element_type: str) -> None:
        """Raises ValueError if element type is not valid."""
        if element_type not in ELEMENTS_TEMPLATES:
            raise ValueError(f'Invalid element type: {element_type}.')

    @staticmethod
    def validate_type(param, types: type | tuple[type, ...]) -> None:
        """Raises TypeError if type(param) is not in types."""
        if not isinstance(param, types):
            if isinstance(types, tuple):
                expected = ' or '.join(t.__name__ for t in types)
            else:
                expected = types.__name__
            raise TypeError(
                f'Expected {expected}, got {type(param).__name__} instead.'
            )