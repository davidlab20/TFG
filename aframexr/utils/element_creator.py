"""AframeXR elements creator"""

CREATOR_MAP: dict[str, type['ElementCreator']] = {}  # Creator map of elements, classes are added at the end of the file


class ElementCreator:
    _ELEMENT_HTML: str = ''  # Must be defined by child classes
    """
    When defining _ELEMENT_HTML in a subclass:
        * Do NOT add a space before {attributes}.
        * The method get_element_html() automatically adds a leading space if there are attributes.
    """

    def __init__(self, element_specs: dict):
        self._color = element_specs.get('color')
        self._info = element_specs.get('info')
        self._position = element_specs.get('position')
        self._rotation = element_specs.get('rotation')

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

    def get_element_html(self):
        if self._ELEMENT_HTML == '':
            raise RuntimeError('Attribute _ELEMENT_HTML was not initialized')

        attributes = ''.join(
            f' {key[1:].replace("_", "-")}="{value}"'  # Add space at the beginning (using HTML format)
            for key, value in self.__dict__.items()
            if value is not None and key.startswith('_')  # Only add defined private attributes in the HTML
        )

        if self._info is not None:  # Add interaction if there is information to display
            attributes += ' data-raycastable'

        return self._ELEMENT_HTML.format(attributes=attributes)


class BoxCreator(ElementCreator):
    _ELEMENT_HTML = '<a-box{attributes}></a-box>'

    def __init__(self, element_specs: dict):
        super().__init__(element_specs)
        self._depth = element_specs.get('depth')
        self._height = element_specs.get('height')
        self._width = element_specs.get('width')


class CylinderCreator(ElementCreator):
    _ELEMENT_HTML = '<a-cylinder side="double"{attributes}></a-cylinder>'

    def __init__(self, element_specs: dict):
        super().__init__(element_specs)
        self._radius = element_specs.get('radius')
        self._theta_start = element_specs.get('theta_start')
        self._theta_length = element_specs.get('theta_length')


class GLTFCreator(ElementCreator):
    _ELEMENT_HTML = '<a-gltf-model{attributes}></a-gltf-model>'

    def __init__(self, element_specs: dict):
        super().__init__(element_specs)
        self._scale = element_specs.get('scale')
        self._src = element_specs.get('src')


class ImageCreator(ElementCreator):
    _ELEMENT_HTML = '<a-image{attributes}></a-image>'

    def __init__(self, element_specs: dict):
        super().__init__(element_specs)
        self._height = element_specs.get('height')
        self._src = element_specs.get('src')
        self._width = element_specs.get('width')


class SphereCreator(ElementCreator):
    _ELEMENT_HTML = '<a-sphere{attributes}></a-sphere>'

    def __init__(self, element_specs: dict):
        super().__init__(element_specs)
        self._radius = element_specs.get('radius')


# Add creator classes to CREATOR_MAP dynamically
CREATOR_MAP.update({'box': BoxCreator})
CREATOR_MAP.update({'cylinder': CylinderCreator})
CREATOR_MAP.update({'gltf': GLTFCreator})
CREATOR_MAP.update({'image': ImageCreator})
CREATOR_MAP.update({'sphere': SphereCreator})
