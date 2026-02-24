"""AframeXR parameters."""

from ..utils.validators import AframeXRValidator

# Selections
def selection_point(name: str, fields: list) -> 'Parameter':
    """Add selection to the chart."""
    AframeXRValidator.validate_type('name', name, str)
    AframeXRValidator.validate_type('fields', fields, list)

    select_config = {'type': 'point', 'fields': fields}
    return Parameter(name=name, select=select_config)


class Parameter:
    def __init__(self, name: str, select: dict):
        AframeXRValidator.validate_type('name', name, str)
        AframeXRValidator.validate_type('select', select, dict)

        self._name = name
        self._select_config = select

    def to_specs(self):
        return {
            'name': self._name,
            'select': self._select_config
        }

    def to_dict(self) -> dict:
        return {'param': self._name}
