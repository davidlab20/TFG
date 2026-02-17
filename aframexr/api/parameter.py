"""AframeXR parameters."""

from ..utils.validators import AframeXRValidator


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
