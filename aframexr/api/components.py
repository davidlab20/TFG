from abc import ABC, abstractmethod
import copy
import html
import json
import warnings

try:
    import pandas as pd
    from pandas import DataFrame
except ImportError:
    DataFrame = object
    pd = None

from IPython.display import display, HTML
from typing import Literal

from .aggregate import AggregatedFieldDef
from .data import Data, UrlData
from .encoding import Encoding, X, Y, Z
from .filters import FilterTransform
from .parameter import Parameter
from ..utils.scene_creator import SceneCreator
from ..utils.validators import AframeXRValidator


class TopLevelMixin:
    """Top level chart class."""

    def __init__(self, specs: dict):
        self._specifications = specs

    def _generate_iframe_html(self, ar_scale: str = None, environment: Literal['default', 'contact', 'egypt',
    'checkerboard', 'forest', 'goaland', 'yavapai', 'goldmine', 'arches', 'threetowers', 'poison', 'tron', 'japan',
    'dream', 'volcano', 'starry', 'osiris'] = 'default'):
        return (
            '<iframe '
            f'srcdoc="{html.escape(self.to_html(ar_scale=ar_scale, environment=environment), quote=True)}" '  # Raw HTML
            'width="100%" '  # Adjust to maximum width
            'height="400" '  # Height of the iframe
            'style="border:none;" '
            'sandbox="allow-scripts allow-forms allow-same-origin" '
            'loading="lazy" '  # For optimization
            '></iframe>'
        )

    def _resolve_data(self):
        """Resolves the data reference of the specifications."""
        def materialize_data(data):
            AframeXRValidator.validate_type(
                'data', data, (Data, UrlData, DataFrame)  # type: ignore[arg-type] --> DataFrame
            )

            if isinstance(data, Data):
                return {'values': data.values}
            elif isinstance(data, UrlData):
                return {'url': data.url}
            elif pd is not None and isinstance(data, pd.DataFrame):
                arr = data.to_numpy()  # type: ignore --> because of DataFrame
                cols = data.columns.tolist()  # type: ignore --> because of DataFrame
                return {'values': [dict(zip(cols, row)) for row in arr]}
            else:  # pragma: no cover (AframeXRValidator.validate_type() should have validate data type)
                raise RuntimeError('Unreachable code: AframeXRValidator.validate_type() should have validate data type')

        for specs in self._specifications.get('concat', [self._specifications]):
            if 'data_ref' in specs:
                specs['data'] = materialize_data(specs.pop('data_ref'))

    def _repr_html_(self):  # pragma: no cover (as this method is called in notebooks)
        """Returns the iframe HTML for showing the scene in the notebook."""
        return self._generate_iframe_html()

    # Concatenating charts
    def __add__(self, other):
        """
        Concatenation of charts (place charts in the same scene).
        Creates and returns a new scene with the charts. The original charts are not modified.
        """
        if not isinstance(other, TopLevelMixin):
            raise TypeError(f"Cannot add {type(other).__name__} to {type(self).__name__}.")

        self_specs_list = copy.deepcopy(self._specifications.get('concat', [self._specifications]))
        other_specs_list = copy.deepcopy(other._specifications.get('concat', [other._specifications]))

        new = self.copy()  # Create a copy to modify
        new._specifications = {'concat': self_specs_list + other_specs_list}
        return new

    # Copy of the chart
    def __deepcopy__(self, memo):
        """Optimized deepcopy avoiding copying large data values."""
        if id(self) in memo:  # Avoid copying several times the same object
            return memo[id(self)]

        new_instance = self.__class__.__new__(self.__class__)
        memo[id(self)] = new_instance

        # Separate data reference from the rest of the specifications
        specs_copy = self._specifications.copy()  # Shallow copy
        data_ref = specs_copy.pop('data_ref', None)

        # Deep copy of the rest
        new_instance._specifications = copy.deepcopy(specs_copy, memo)

        # Restore data reference
        if data_ref is not None:
            new_instance._specifications['data_ref'] = data_ref

        return new_instance

    def copy(self):
        """Return a deep copy of the chart while keeping large data as reference."""
        return copy.deepcopy(self)

    # Importing charts
    @staticmethod
    def from_dict(specs: dict) -> 'TopLevelMixin':
        """
        Import the chart from the JSON dict specifications.

        Parameters
        ----------
        specs : dict
            JSON specifications of the chart.

        Raises
        ------
        TypeError
            If specs is not a dictionary.
        """
        AframeXRValidator.validate_type('specs', specs, dict)
        chart = Chart()
        chart._specifications = copy.deepcopy(specs)
        return chart

    @staticmethod
    def from_json(specs: str) -> 'TopLevelMixin':
        """
        Create the chart from the JSON string specifications.

        Parameters
        ----------
        specs : str
            JSON specifications of the chart.

        Raises
        ------
        TypeError
            If specs is not a string.
        JSONDecodeError
            If specs is not a valid JSON.
        """
        AframeXRValidator.validate_type('specs', specs, str)
        chart = Chart()
        chart._specifications = copy.deepcopy(json.loads(specs))
        AframeXRValidator.validate_chart_specs(chart._specifications)
        return chart

    # Movable
    def movable(self):
        """
        Make the entity movable.

        Concatenated charts cannot be movable, each chart must be defined as movable before concatenating.
        """
        self_copy = self.copy()
        if 'concat' in self_copy._specifications:
            raise ValueError('Concatenated charts cannot be movable.')

        self_copy._specifications['movable'] = True
        return self_copy

    # Exporting charts
    def save(self, fp: str, file_format: Literal['json', 'html'] = None, environment: Literal['default', 'contact',
    'egypt', 'checkerboard', 'forest', 'goaland', 'yavapai', 'goldmine', 'arches', 'threetowers', 'poison', 'tron',
    'japan', 'dream', 'volcano', 'starry', 'osiris'] = 'default'):
        """
        Saves the chart into a file, supported formats are JSON and HTML.

        Parameters
        ----------
        fp : str
            File path.
        file_format : str (optional)
            Format of the file could be ['html', 'json'].
            If no format is specified, the chart will be saved depending on the file extension.
        environment : str (optional)
            Environment of the scene.

        Raises
        ------
        ValueError
            If file_format is invalid.
        """
        AframeXRValidator.validate_type('fp', fp, str)
        self_copy = self.copy()

        if file_format == 'html' or fp.endswith('.html'):
            with open(fp, 'w') as file:
                file.write(self_copy.to_html(environment=environment))
        elif file_format == 'json' or fp.endswith('.json'):
            with open(fp, 'w') as file:
                specs = self_copy.to_dict()
                specs['environment'] = environment
                AframeXRValidator.validate_chart_specs(specs)
                json.dump(specs, file, indent=4)
        else:
            raise ValueError('Invalid file format. Must be "json" or "html"')

    # Showing the scene
    def show(self, ar_scale: str = None, environment: Literal['default', 'contact', 'egypt', 'checkerboard', 'forest',
    'goaland', 'yavapai', 'goldmine', 'arches', 'threetowers', 'poison', 'tron', 'japan', 'dream', 'volcano', 'starry',
    'osiris'] = 'default'):
        """Show the scene in the notebook."""
        with warnings.catch_warnings():
            # Do not show the warning --> UserWarning: Consider using IPython.display.IFrame instead
            warnings.filterwarnings('ignore', message='Consider using IPython.display.IFrame instead')

            self_copy = self.copy()
            self_copy._resolve_data()

            html_obj = HTML(self_copy._generate_iframe_html(
                ar_scale=ar_scale,
                environment=environment
            ))

            display(html_obj)
            return html_obj

    # Chart formats
    def to_dict(self) -> dict:
        """Returns the scene specifications as a dictionary."""
        self_copy = self.copy()
        self_copy._resolve_data()

        AframeXRValidator.validate_chart_specs(self_copy._specifications)
        return self_copy._specifications

    def to_html(self, ar_scale: str = None, environment: Literal['default', 'contact', 'egypt', 'checkerboard',
    'forest', 'goaland', 'yavapai', 'goldmine', 'arches', 'threetowers', 'poison', 'tron', 'japan', 'dream', 'volcano',
    'starry', 'osiris'] = 'default') -> str:
        """Returns the HTML representation of the scene."""
        self_copy = self.copy()
        self_copy._resolve_data()

        if ar_scale is not None: self_copy._specifications['ar_scale'] = ar_scale
        self_copy._specifications['environment'] = environment
        AframeXRValidator.validate_chart_specs(self_copy._specifications)
        return SceneCreator.create_scene(self_copy._specifications)

    def to_json(self) -> str:
        """Returns the JSON string of the scene."""
        return json.dumps(self.to_dict())  # Method to_dict() validates chart specifications


class Chart(TopLevelMixin):
    """
    Simple chart class.

    Parameters
    ----------
    data : Data | UrlData | DataFrame
        Data, UrlData object or pandas DataFrame of the data.
    depth : float (optional)
        Depth of the chart. If not defined, using DEFAULT_CHART_DEPTH.
    height : float (optional)
        Height of the chart. If not defined, using DEFAULT_CHART_HEIGHT.
    position : str (optional)
        Position of the chart. The format is: 'x y z'. Refers to the position for the origin of coordinate system.
        If not defined, using DEFAULT_CHART_POS.
    rotation : str (optional)
        Rotation of the chart in degrees. The format is: 'x y z'. The rotation axis is the coordinate system.
        If not defined, using DEFAULT_CHART_ROTATION.
    width : float (optional)
        Width of the chart. If not defined, using DEFAULT_CHART_WIDTH.

    Raises
    ------
    TypeError
        If any parameter has invalid type.
    ValueError
        If depth, height, position, rotation or width is invalid.
    """
    def __init__(self, data: Data | UrlData | DataFrame = None, depth: float = None, height: float = None,
                 title: str = None, position: str = None, rotation: str = None, width: float = None):
        super().__init__({})  # Initiate specifications

        if data is not None: self._specifications['data_ref'] = data
        if position is not None: self._specifications['position'] = position
        if rotation is not None: self._specifications['rotation'] = rotation
        if depth is not None: self._specifications['depth'] = depth
        if height is not None: self._specifications['height'] = height
        if width is not None: self._specifications['width'] = width
        if title is not None: self._specifications['title'] = title

    # Parameters
    def add_params(self, *params: Parameter):
        self_copy = self.copy()

        for p in params:
            AframeXRValidator.validate_type('params', p, Parameter)

        if 'params' not in self_copy._specifications:
            self_copy._specifications['params'] = []

        self_copy._specifications['params'].extend(
            [p.to_specs() for p in params]
        )

        return self_copy

    # Types of charts
    def mark_arc(self, radius: float = None):
        """
        Pie chart and doughnut chart.

        Parameters
        ----------
        radius : float (optional)
            Outer radius of the pie chart. If not specified, using DEFAULT_PIE_RADIUS. Must be greater than 0.
        """
        self_copy = self.copy()

        self_copy._specifications['mark'] = {'type': 'arc'}

        if radius is not None:
            AframeXRValidator.validate_positive_number('radius', radius)
            self_copy._specifications['mark']['radius'] = radius

        return self_copy

    def mark_bar(self, color: str = None, size: float = None):
        """
        Bars chart.

        Parameters
        ----------
        color: str (optional)
            Color of the bars. If not defined, using DEFAULT_ELEMENTS_COLOR_IN_CHART.
        size : float (optional)
            Width of the bars. If not specified, bars will be adjusted automatically. Must be greater than 0.

        Raises
        ------
        ValueError
            If defined size is not greater than 0.
        """
        self_copy = self.copy()

        self_copy._specifications['mark'] = {'type': 'bar'}

        if color is not None:
            AframeXRValidator.validate_type('color', color, str)
            self_copy._specifications['mark']['color'] = color

        if size is not None:
            AframeXRValidator.validate_positive_number('size', size)
            self_copy._specifications['mark']['size'] = size

        return self_copy

    def mark_line(self, color: str = None, point: bool = None):
        """
        Line chart.

        Parameters
        ----------
        color: str (optional)
            Color of the line. If not defined, using DEFAULT_ELEMENTS_COLOR_IN_CHART.
        point : bool (optional)
            Either if add points in vertices or not. If not defined, using
        """
        self_copy = self.copy()

        self_copy._specifications['mark'] = {'type': 'line'}

        if color is not None:
            AframeXRValidator.validate_type('color', color, str)
            self_copy._specifications['mark']['color'] = color

        if point is not None:
            AframeXRValidator.validate_type('point', point, bool)
            self_copy._specifications['mark']['point'] = point

        return self_copy

    def mark_point(self, color: str = None, size: float = None):
        """
        Scatter plot and bubble chart.

        Parameters
        ----------
        color: str (optional)
            Color of the spheres. If not defined, using DEFAULT_ELEMENTS_COLOR_IN_CHART.
        size : float (optional)
            Maximum radius of the point. If not specified, using DEFAULT_POINT_RADIUS. Must be greater than 0.

        Raises
        ------
        ValueError
            If size is not greater than 0.
        """
        self_copy = self.copy()

        self_copy._specifications['mark'] = {'type': 'point'}

        if color is not None:
            AframeXRValidator.validate_type('color', color, str)
            self_copy._specifications['mark']['color'] = color

        if size is not None:
            AframeXRValidator.validate_positive_number('size', size)
            self_copy._specifications['mark']['size'] = size

        return self_copy

    # Parameters of the chart
    def encode(self, color: str = None, size: str = None, theta: str = None, x: str | X = None, y: str | Y = None,
               z: str | Z = None):
        """
        Add properties to the chart.

        Parameters
        ----------
        color : str (optional)
            Field of the data that will determine the color of the sphere in the scatter plot.
        size : str (optional)
            Field of the data that will determine the size of the sphere in the bubble chart (must be quantitative).
        theta : str (optional)
            Field of the data that will determine the arcs of the pie and doughnut chart (must be quantitative).
        x : str | X (optional)
            Field of the data that will determine the x-axis of the chart.
        y : str | Y (optional)
            Field of the data what will determine the y-axis of the chart (must be quantitative).
        z : str | Z (optional)
            Field of the data what will determine the z-axis of the chart.

        Raises
        ------
        TypeError
            If the encoding type is incorrect.
        ValueError
            If the encoding values are incorrect.
        """
        filled_params = {}  # Dictionary that will store the parameters that have been filled

        # Verify the type of the arguments and store the filled parameters
        if color is not None:
            AframeXRValidator.validate_type('color', color, str)
            filled_params['color'] = color
        if size is not None:
            AframeXRValidator.validate_type('size', size, str)
            filled_params['size'] = size
        if theta is not None:
            AframeXRValidator.validate_type('theta', theta, str)
            filled_params['theta'] = theta
        if x is not None:
            AframeXRValidator.validate_type('x', x, (str, X))
            filled_params['x'] = x
        if y is not None:
            AframeXRValidator.validate_type('y', y, (str, Y))
            filled_params['y'] = y
        if z is not None:
            AframeXRValidator.validate_type('z', z, (str, Z))
            filled_params['z'] = z

        # Do the encoding
        self_copy = self.copy()

        encoding = self_copy._specifications.setdefault('encoding', {})  # For merging possible further encodings
        for param_key in filled_params:
            param_value = filled_params[param_key]
            if isinstance(param_value, Encoding):
                encoding.update(param_value.to_dict())
            else:
                formula, encoding_type = Encoding.split_field_and_encoding(param_value)
                field, aggregate_op = AggregatedFieldDef.split_operator_field(formula)
                encoding[param_key] = {'field': field}
                if aggregate_op:
                    encoding[param_key]['aggregate'] = aggregate_op
                if encoding_type:
                    encoding[param_key]['type'] = encoding_type

        return self_copy

    def properties(self, data: Data | UrlData | DataFrame = None, depth: str = None, height: str = None,
                   position: str = None, rotation: str = None, title: str = None, width: str = None):
        """Modify general properties of the chart."""
        self_copy = self.copy()

        if data is not None: self_copy._specifications['data_ref'] = data
        if position is not None: self_copy._specifications['position'] = position
        if rotation is not None: self_copy._specifications['rotation'] = rotation
        if depth is not None: self_copy._specifications['depth'] = depth
        if height is not None: self_copy._specifications['height'] = height
        if width is not None: self_copy._specifications['width'] = width
        if title is not None: self_copy._specifications['title'] = title

        return self_copy

    # Modifying data
    def transform_aggregate(self, groupby: list = None, **kwargs):
        """
        Aggregates the data with the specified aggregate function, grouped by the specified groupby.

        Parameters
        ----------
        groupby : list | None
            Data fields that will be grouped, optional. If not set, the defined fields in encode() method will be taken.
        kwargs : dict
            Format is: <new_field>=<aggregate_op>(<data_field>).
        """
        AframeXRValidator.validate_type('groupby', groupby, (list, type(None)))

        # Create a copy of the chart (in case of assignation, to preserve the main chart)
        aggreg_chart = self.copy()

        aggregates_to_dict = []
        for as_field, aggregate_formula in kwargs.items():
            field, aggregate_op = AggregatedFieldDef.split_operator_field(str(aggregate_formula))
            aggregate_object = AggregatedFieldDef(aggregate_op, field, as_field)
            aggregates_to_dict.append(aggregate_object.to_dict())

        aggregate_specs = {'aggregate': aggregates_to_dict}
        if groupby:
            aggregate_specs['groupby'] = groupby

        if not aggreg_chart._specifications.get('transform'):  # First time filtering the chart (create field)
            aggreg_chart._specifications['transform'] = [aggregate_specs]
        else:  # Not the first filter of the chart (add to aggregates)
            aggreg_chart._specifications['transform'].append(aggregate_specs)
        return aggreg_chart

    def transform_filter(self, equation_filter: str | FilterTransform | Parameter):
        """
        Filters the chart with the given transformation.

        Parameters
        ----------
        equation_filter : str | FilterTransform | Parameter
            The equation string of the filter transformation, a Filter object (see Examples) or Parameter object.

        Raises
        ------
        TypeError
            If equation is not a string, a Filter object or a Parameter object.

        Notes
        -----
        Can be concatenated with the rest of functions of the Chart, without needing an asignation. It can also be
        concatenated several times (the result will be an addition of the filters, in order of assignation).

        Examples
        --------
        *Using transform_filter() giving the equation string:*

        >>> import aframexr
        >>> data = aframexr.UrlData('./data.json')
        >>> chart = aframexr.Chart(data).mark_bar().encode(x='model', y='sales')
        >>> filtered_chart = chart.transform_filter('datum.motor == diesel')
        >>> #filtered_chart.show()

        *Using transform_filter() giving a Filter object*

        >>> import aframexr
        >>> data = aframexr.UrlData('./data.json')
        >>> chart = aframexr.Chart(data).mark_bar().encode(x='model', y='sales')
        >>> filter_object = aframexr.FieldEqualPredicate(field='motor', equal='diesel')
        >>> filtered_chart = chart.transform_filter(filter_object)
        >>> #filtered_chart.show()
        """
        # Validate the type of equation_filter and get a filter object from the equation_filter
        AframeXRValidator.validate_type(
            'equation_filter', equation_filter, (str, FilterTransform, Parameter)
        )
        if isinstance(equation_filter, str):
            filter_transform = FilterTransform.from_equation(equation_filter)
        elif isinstance(equation_filter, (FilterTransform, Parameter)):
            filter_transform = equation_filter
        else:  # pragma: no cover
            raise RuntimeError('Unreachable code. Parameter should have been validated before')

        # Create a copy of the chart (in case of assignation, to preserve the main chart)
        filt_chart = self.copy()

        # Add the information of the filter object to the specifications
        if not filt_chart._specifications.get('transform'):  # First time filtering the chart
            filt_chart._specifications['transform'] = [{'filter': filter_transform.to_dict()}]
        else:  # Not the first filter of the chart
            filt_chart._specifications['transform'].append({'filter': filter_transform.to_dict()})
        return filt_chart  # Returns the copy of the chart


class Element(TopLevelMixin, ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        element_name = self.__class__.__name__.lower()  # Use child class's name for defining the element
        super().__init__({'element': element_name})

        self._specifications.update(
            {key: value for key, value in kwargs.items()
             if value is not None}
        )


# Single elements
class Box(Element):
    def __init__(self, color: str = None, depth: float = None, height: float = None, position: str = None,
                 rotation: str = None, width: float = None):
        super().__init__(color=color, depth=depth, height=height, position=position, rotation=rotation, width=width)


class Cone(Element):
    def __init__(self, color: str = None, height: float = None, position: str = None, radius_bottom: float = None,
                 radius_top: float = None):
        super().__init__(color=color, height=height, position=position, radius_bottom=radius_bottom,
                         radius_top=radius_top)


class Cylinder(Element):
    def __init__(self, color: str = None, height: float = None, position: str = None, radius: float = None,
                 rotation: str = None):
        super().__init__(color=color, height=height, position=position, radius=radius, rotation=rotation)


class Dodecahedron(Element):
    def __init__(self, color: str = None, position: str = None, radius: float = None):
        super().__init__(color=color, position=position, radius=radius)


class GLTF(Element):
    def __init__(self, src: str, scale: str = None, position: str = None, rotation: str = None):
        super().__init__(src=src, scale=scale, position=position, rotation=rotation)


class Icosahedron(Element):
    def __init__(self, color: str = None, position: str = None, radius: float = None):
        super().__init__(color=color, position=position, radius=radius)


class Image(Element):
    def __init__(self, src: str, height: float = None, position: str = None, rotation: str = None, width: float = None):
        super().__init__(src=src, height=height, position=position, rotation=rotation, width=width)


class Line(Element):
    def __init__(self, start: str, end: str, color: str = None):
        super().__init__(start=start, end=end, color=color)


class Octahedron(Element):
    def __init__(self, color: str = None, position: str = None, radius: float = None):
        super().__init__(color=color, position=position, radius=radius)


class Plane(Element):
    def __init__(self, color: str = None, height: float = None, position: str = None, rotation: str = None,
                 width: float = None):
        super().__init__(color=color, height=height, position=position, rotation=rotation, width=width)


class Sphere(Element):
    def __init__(self, color: str = None, position: str = None, radius: float = None):
        super().__init__(color=color, position=position, radius=radius)


class Tetrahedron(Element):
    def __init__(self, color: str = None, position: str = None, radius: float = None):
        super().__init__(color=color, position=position, radius=radius)


class Text(Element):
    def __init__(self, value: str, align: Literal['center', 'left', 'right'] = None, color: str = None,
                 position: str = None, rotation: str = None, scale: str = None):
        super().__init__(align=align, color=color, position=position, rotation=rotation, value=value, scale=scale)


class Torus(Element):
    def __init__(self, color: str = None, position: str = None, radius: float = None, radius_tubular: float = None,
                 rotation: str = None):
        super().__init__(color=color, position=position, radius=radius, radius_tubular=radius_tubular,
                         rotation=rotation)
