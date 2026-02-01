"""AframeXR elements creator"""

from .constants import DEFAULT_CHART_POS, DEFAULT_CHART_ROTATION, DEFAULT_SINGLE_ELEMENT_COLOR

CREATOR_MAP: dict[str, type['ElementCreator']] = {}  # Creator map of elements, classes are added at the end of the file


class ElementCreator:
    def __init__(self, element_specs: dict):
        self._position = element_specs.get('position', DEFAULT_CHART_POS)
        self._rotation = element_specs.get('rotation', DEFAULT_CHART_ROTATION)

    @staticmethod
    def create_object(element_type: str, element_specs: dict):
        """
        Returns an ElementCreator instance depending on element specifications.
        Notes
        -----
        Supposing that field "element" exists in element specifications, this method is called from ChartsHTMLCreator.
        """
        if element_type not in CREATOR_MAP:
            raise ValueError()
        return CREATOR_MAP[element_type](element_specs)


class BoxCreator(ElementCreator):
    def __init__(self, element_specs: dict):
        super().__init__(element_specs)
        self._color = element_specs.get('color', DEFAULT_SINGLE_ELEMENT_COLOR)
        self._depth = element_specs.get('depth', 1)
        self._height = element_specs.get('height', 1)
        self._width = element_specs.get('width', 1)

    def get_element_specs(self):
        return {
            'position': self._position,
            'rotation': self._rotation,
            'width': self._width,
            'height': self._height,
            'depth': self._depth,
            'color': self._color,
        }


# Add creator classes to CREATOR_MAP dynamically
CREATOR_MAP.update({'box': BoxCreator})
