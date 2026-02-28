"""AframeXR elements creator"""

CREATOR_MAP: dict[str, type['ElementCreator']] = {}  # Creator map of elements, classes are added at the end of the file


class ElementCreator:
    _ELEMENT_HTML: str = ''  # Must be defined by child classes
    """
    When defining _ELEMENT_HTML in a subclass:
        * Do NOT add a space before {attributes}.
        * The method get_element_html() automatically adds a leading space if there are attributes.
    """

    def __init__(self, element_specs: dict, filtered_by_params: bool = False):
        self._filtered_by_params = filtered_by_params

        if type(self) is ElementCreator:
            raise TypeError(f'{self.__class__.__name__} is abstract')

        self._attributes = {
            key: value for key, value in element_specs.items()
            if value is not None and key not in {'element', 'environment'}
        }

    @classmethod
    def create_object(cls, element_type: str, element_specs: dict) -> 'ElementCreator':
        """
        Returns an ElementCreator instance depending on element specifications.
        Notes
        -----
        Supposing that field "element" exists in element specifications, this method is called from ChartsHTMLCreator.
        """
        if element_type not in CREATOR_MAP:  # pragma: no cover (all classes should be added at the end of this file)
            raise RuntimeError(f'Class for {element_type} was not added to CREATOR_MAP')

        return CREATOR_MAP[element_type](element_specs)

    def get_element_html(self) -> str:
        if self._ELEMENT_HTML == '':  # pragma: no cover (all classes should have inner _ELEMENT_HTML constant defined)
            raise RuntimeError('Attribute _ELEMENT_HTML was not initialized')

        attributes = ''.join(
            f' {key.replace("_", "-")}="{value}"'  # Add space at the beginning (using HTML format)
            for key, value in self._attributes.items()
        )

        # Add interaction if there is information to display and the element is not part of a subchart
        if 'info' in self._attributes and not self._filtered_by_params:
            attributes += ' data-raycastable'

        return self._ELEMENT_HTML.format(attributes=attributes)


class BoxCreator(ElementCreator):
    _ELEMENT_HTML = '<a-box{attributes} side="double"></a-box>'


class ConeCreator(ElementCreator):
    _ELEMENT_HTML = '<a-cone{attributes}></a-cone>'


class CylinderCreator(ElementCreator):
    _ELEMENT_HTML = '<a-cylinder side="double"{attributes}></a-cylinder>'


class DodecahedronCreator(ElementCreator):
    _ELEMENT_HTML = '<a-dodecahedron{attributes}></a-dodecahedron>'


class GLTFCreator(ElementCreator):
    _ELEMENT_HTML = '<a-gltf-model{attributes}></a-gltf-model>'


class IcosahedronCreator(ElementCreator):
    _ELEMENT_HTML = '<a-icosahedron{attributes}></a-icosahedron>'


class ImageCreator(ElementCreator):
    _ELEMENT_HTML = '<a-image{attributes}></a-image>'

class OctahedronCreator(ElementCreator):
    _ELEMENT_HTML = '<a-octahedron{attributes}></a-octahedron>'


class PlaneCreator(ElementCreator):
    _ELEMENT_HTML = '<a-plane side="double"{attributes}></a-plane>'


class SphereCreator(ElementCreator):
    _ELEMENT_HTML = '<a-sphere{attributes}></a-sphere>'


class TetrahedronCreator(ElementCreator):
    _ELEMENT_HTML = '<a-tetrahedron{attributes}></a-tetrahedron>'


class TextCreator(ElementCreator):
    _ELEMENT_HTML = '<a-text{attributes}></a-text>'


class TorusCreator(ElementCreator):
    _ELEMENT_HTML = '<a-torus{attributes}></a-torus>'


# Add creator classes to CREATOR_MAP dynamically
CREATOR_MAP.update({
    'box': BoxCreator,
    'cone': ConeCreator,
    'cylinder': CylinderCreator,
    'dodecahedron': DodecahedronCreator,
    'gltf': GLTFCreator,
    'icosahedron': IcosahedronCreator,
    'image': ImageCreator,
    'octahedron': OctahedronCreator,
    'plane': PlaneCreator,
    'sphere': SphereCreator,
    'tetrahedron': TetrahedronCreator,
    'text': TextCreator,
    'torus': TorusCreator,
})
