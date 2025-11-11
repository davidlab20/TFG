"""AframeXR components"""

import json
import marimo
from typing import Literal

from aframexr.api.data import Data, URLData
from aframexr.utils.defaults import *
from aframexr.utils.scene_creator import SceneCreator


class TopLevelMixin:
    """Top level chart class."""

    def __init__(self, specs: dict = None):
        if specs is None:  # For calls of Chart.__init__(), calling super().__init__()
            self._specifications = {}  # Specifications of the scene, in JSON format
        else:  # For calls of __add__(), to create a new object and do not modify the rest
            self._specifications = specs

    # Concatenating charts
    def __add__(self, other):
        """
        Concatenation of charts (place charts in the same scene).
        Creates and returns a new scene with the charts. The original charts are not modified.
        """

        if not isinstance(other, TopLevelMixin):
            raise TypeError(f"Cannot add {type(other).__name__} to {type(self).__name__}")
        concatenated_chart = TopLevelMixin({'concat': [self._specifications, other._specifications]})
        return concatenated_chart

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

        if not isinstance(specs, dict):
            raise TypeError(f'Expected dict, got {type(specs).__name__} instead.')
        return TopLevelMixin(specs)

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
        """

        if not isinstance(specs, str):
            raise TypeError(f'Expected str, got {type(specs).__name__} instead.')
        return TopLevelMixin(json.loads(specs))

    # Exporting charts
    def save(self, fp: str, fileFormat: Literal['json', 'html'] = None):
        """
        Saves the chart into a file, supported formats are JSON and HTML.

        Parameters
        ----------
        fp : str
            File path.
        fileFormat : str (optional)
            Format of the file could be ['html', 'json'].
            If no format is specified, the chart will be saved depending on the file extension.

        Raises
        ------
        NotImplementedError
            If fileFormat is invalid.
        """

        if fileFormat == 'html' or fp.endswith('.html'):
            with open(fp, 'w') as file:
                file.write(self.to_html())
        elif fileFormat == 'json' or fp.endswith('.json'):
            with open(fp, 'w') as file:
                json.dump(self._specifications, file, indent=4)
        else:
            raise NotImplementedError('That format is not supported.')

    # Showing the scene
    def show(self):
        """Show the scene in the Marimo notebook."""

        html_scene = SceneCreator.create_scene(self._specifications)
        return marimo.iframe(html_scene)

    # Chart formats
    def to_dict(self) -> dict:
        """Returns the scene specifications as a dictionary."""

        return self._specifications

    def to_html(self) -> str:
        """Returns the HTML representation of the scene."""

        return SceneCreator.create_scene(self._specifications)

    def to_json(self) -> str:
        """Returns the JSON string of the scene."""

        return json.dumps(self._specifications)


class Chart(TopLevelMixin):
    """
    Simple chart class.

    Parameters
    ----------
    data : Data | URLData
        Data or URLData object of the data.

    position : str (optional)
        Position of the chart. The format is: 'x y z', 'x y' or 'x'.
        The not given axis position will be set to 0. For example, 'x y' is equal to 'x y 0'

    Raises
    ------
    TypeError
        If data is not a Data or URLData object.
    """

    def __init__(self, data: Data | URLData, position: str = DEFAULT_CHART_POS):
        super().__init__()

        # Data
        if isinstance(data, Data):
            self._specifications.update({'data': {'values': data.values}})
        elif isinstance(data, URLData):
            self._specifications.update({'data': {'url': data.url}})
        else:
            raise TypeError(f'Expected Data | URLData, got {type(data).__name__} instead.')

        # Position
        _, default_y, default_z = DEFAULT_CHART_POS.split()  # Default value of axis Y and Z
        all_axis = position.strip().split()  # Split axis by spaces
        for axis in all_axis:
            try:
                float(axis)  # Verify if the axis is correct (if it is numeric)
            except ValueError:
                raise ValueError(f'The position: {position} is not correct.')
        if len(all_axis) == 3:  # Position is 'x y z'
                self._specifications.update({'position': f'{all_axis[0]} {all_axis[1]} {all_axis[2]}'})
        elif len(all_axis) == 2:  # Position is 'x y'
                self._specifications.update({'position': f'{all_axis[0]} {all_axis[1]} {default_z}'})
        elif len(all_axis) == 1:  # Position is 'x'
                self._specifications.update({'position': f'{all_axis[0]} {default_y} {default_z}'})
        else:
            raise ValueError(f'The position: {position} is not correct.')

    # Types of charts
    def mark_arc(self, outer_radius: float = DEFAULT_PIE_RADIUS, inner_radius: float = DEFAULT_PIE_INNER_RADIUS):
        """
        Pie chart and doughnut chart.

        Parameters
        ----------
        outer_radius : float (optional)
            Outer radius of the pie chart. If not specified, using default. Must be greater than 0.
        inner_radius : float (optional)
            Inner radius of the pie chart. If not specified, using default. Must be greater than 0.
        """

        self._specifications.update({'mark': {'type': 'arc'}})
        if outer_radius >= 0:
            self._specifications['mark'].update({'outerRadius': outer_radius})
        else:
            raise ValueError('radius must be greater than 0.')
        if inner_radius >= 0:
            self._specifications['mark'].update({'innerRadius': inner_radius})
        else:
            raise ValueError('inner_radius must be greater than 0.')
        if inner_radius > outer_radius:
            raise ValueError('inner_radius must be smaller than outer_radius.')
        return self

    def mark_bar(self, width: float = DEFAULT_BAR_CHART_WIDTH, height: float = DEFAULT_MAX_HEIGHT):
        """
        Bars chart.

        Parameters
        ----------
        width : float (optional)
            Maximum width of the bar chart. If not specified, using default. Must be greater than 0.
        height : float (optional)
            Maximum height of the bar (the highest bar). If not specified, using default. Must be greater than 0.
        """

        self._specifications.update({'mark': {'type': 'bar'}})
        if width >= 0:
            self._specifications.update({'width': width})
        else:
            raise ValueError('width must be greater than 0.')
        if height >= 0:
            self._specifications.update({'height': height})
        else:
            raise ValueError('height must be greater than 0.')
        return self

    def mark_point(self, width: float = DEFAULT_BAR_CHART_WIDTH, height: float = DEFAULT_MAX_HEIGHT):
        """
        Scatter plot and bubble chart.

        Parameters
        ----------
        width : float (optional)
            Maximum width of the chart. If not specified, using default. Must be greater than 0.
        height : float (optional)
            Maximum height of the chart. If not specified, using default. Must be greater than 0.
        """

        self._specifications.update({'mark': {'type': 'point'}})
        if width >= 0:
            self._specifications.update({'width': width})
        else:
            raise ValueError('width must be greater than 0.')
        if height >= 0:
            self._specifications.update({'height': height})
        else:
            raise ValueError('height must be greater than 0.')
        return self

    # Parameters of the chart
    @staticmethod
    def _split_pram_and_encoding(param: str) -> tuple[str, str | None]:
        """
        Splits and returns the parameter and the encoding data type of the parameter.

        Raises
        ------
        TypeError
            If the encoding type is incorrect.

        Notes
        -----
        Supposing that param is a string, as it has been called from encode() method.
        """

        valid_encoding_types = {'Q': 'quantitative', 'O': 'ordinal', 'N': 'nominal', 'T': 'temporal'}
        param_parts = param.split(':')  # Split parameter in field:encoding_type
        if len(param_parts) == 1:  # No encoding data type is specified
            return param, None
        if len(param_parts) == 2:
            field = param_parts[0]
            encoding_type = param_parts[1].upper()  # Convert to upper case (to accept lower case also)
            if encoding_type not in valid_encoding_types:
                raise ValueError(f'Invalid encoding type: {encoding_type}')
            return field, valid_encoding_types[encoding_type]
        else:
            raise ValueError(f'Invalid encoding type: {param}.')

    def encode(self, color: str = '', size: str = '', theta: str = '', x: str = '', y: str = ''):
        """
        Add properties to the chart.

        Encoding data types (must be specified):
            * Q --> quantitative --> real value number.
            * O --> ordinal --> discrete ordered value.
            * N --> nominal --> discrete unordered category.
            * T --> temporal --> time value or date value.

        Parameters
        ----------
        color : str (optional)
            Field of the data that will determine the color of sphere in the scatter plot (must be nominal).
        size : str (optional)
            Field of the data that will determine the size of the sphere in the bubble chart (must be quantitative).
        theta : str (optional)
            Field of the data that will determine the arcs of the pie and doughnut chart (must be quantitative).
        x : str (optional)
            Field of the data that will determine the x-axis of the chart.
        y : str (optional)
            Field of the data what will determine the y-axis of the chart.

        Raises
        ------
        TypeError
            If the encoding type is incorrect.
        ValueError
            If no encoding data type is specified.
        """

        filled_params = {}  # Dictionary that will store the parameters that have been filled

        # Verify the type of the arguments and store the filled parameters
        if color:
            if not isinstance(color, str):
                raise TypeError(f'Expected color as str, got {type(color).__name__} instead.')
            filled_params.update({'color': color})
        if size:
            if not isinstance(size, str):
                raise TypeError(f'Expected size as str, got {type(size).__name__} instead.')
            filled_params.update({'size': size})
        if theta:
            if not isinstance(theta, str):
                raise TypeError(f'Expected theta as str, got {type(theta).__name__} instead.')
            filled_params.update({'theta': theta})
        if x:
            if not isinstance(x, str):
                raise TypeError(f'Expected x as str, got {type(x).__name__} instead.')
            filled_params.update({'x': x})
        if y:
            if not isinstance(y, str):
                raise TypeError(f'Expected y as str, got {type(y).__name__} instead.')
            filled_params.update({'y': y})

        # Verify the argument combinations
        if self._specifications['mark']['type'] != 'arc' and (not x or not y):
            raise ValueError('x and y must be specified.')
        if color and size:
            raise ValueError('color and size cannot be specified at the same time.')
        if self._specifications['mark']['type'] == 'arc' and (not theta or not color):
            if not theta: raise ValueError('theta must be specified in arc chart.')
            if not color: raise ValueError('color must be specified in arc chart.')
        if self._specifications['mark']['type'] == 'bar' and (color or size):
            if color: raise ValueError('bar chart does not support color.')
            if size: raise ValueError('bar chart does not support size.')
        if self._specifications['mark']['type'] == 'point' and (not color and not size):
            raise ValueError('point chart has to receive "color" or "size".')

        # Do the encoding
        self._specifications.update({'encoding': {}})
        for param_key in filled_params:
            param_value = filled_params[param_key]
            field, encoding_type = self._split_pram_and_encoding(param_value)
            self._specifications['encoding'].update({param_key: {'field': field}})
            if encoding_type:
                self._specifications['encoding'][param_key]['type'] = encoding_type
        return self
