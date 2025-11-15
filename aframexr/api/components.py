"""AframeXR components"""

import copy
import json
import marimo
from typing import Literal

from aframexr.api.data import Data, URLData
from aframexr.api.encoding import *
from aframexr.api.filters import *
from aframexr.utils.constants import *
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

    # Copy of the chart
    def copy(self):
        """Returns a deep copy of the chart."""

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
    ValueError
        If position is invalid.
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

    def mark_bar(self, size: float = DEFAULT_BAR_WIDTH, height: float = DEFAULT_MAX_HEIGHT):
        """
        Bars chart.

        Parameters
        ----------
        size : float (optional)
            Width of the bars. If not specified, using default. Must be greater than 0.
        height : float (optional)
            Maximum height of the chart (the highest bar). If not specified, using default. Must be greater than 0.
        """

        self._specifications.update({'mark': {'type': 'bar'}})
        if size >= 0:
            self._specifications['mark'].update({'width': size})
        else:
            raise ValueError('size must be greater than 0.')
        if height >= 0:
            self._specifications.update({'height': height})
        else:
            raise ValueError('height must be greater than 0.')
        return self

    def mark_point(self, size: float = DEFAULT_POINT_RADIUS, height: float = DEFAULT_MAX_HEIGHT):
        """
        Scatter plot and bubble chart.

        Parameters
        ----------
        size : float (optional)
            Maximum radius of the point. If not specified, using default. Must be greater than 0.
        height : float (optional)
            Maximum height of the chart. If not specified, using default. Must be greater than 0.
        """

        self._specifications.update({'mark': {'type': 'point'}})
        if size >= 0:
            self._specifications['mark'].update({'max_radius': size})
        else:
            raise ValueError('size must be greater than 0.')
        if height >= 0:
            self._specifications.update({'height': height})
        else:
            raise ValueError('height must be greater than 0.')
        return self

    # Parameters of the chart
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
            Field of the data that will determine the color of the sphere in the scatter plot.
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
            if not isinstance(x, str | X):
                raise TypeError(f'Expected x as str | aframexr.X, got {type(x).__name__} instead.')
            filled_params.update({'x': x})
        if y:
            if not isinstance(y, str | Y):
                raise TypeError(f'Expected y as str | aframexr.Y, got {type(y).__name__} instead.')
            filled_params.update({'y': y})

        # Verify the argument combinations
        if self._specifications['mark']['type'] != 'arc' and (not x or not y):
            raise ValueError('x and y must be specified.')
        if self._specifications['mark']['type'] == 'arc' and (not theta or not color):
            if not theta: raise ValueError('theta must be specified in arc chart.')
            if not color: raise ValueError('color must be specified in arc chart.')
        if self._specifications['mark']['type'] == 'bar' and (color or size):
            if color: raise ValueError('bar chart does not support color.')
            if size: raise ValueError('bar chart does not support size.')

        # Do the encoding
        self._specifications.update({'encoding': {}})
        for param_key in filled_params:
            param_value = filled_params[param_key]
            if isinstance(param_value, Encoding):
                self._specifications['encoding'].update(param_value.to_dict())
            else:
                self._specifications['encoding'].update({param_key: {'field': param_value}})
        return self

    # Filtering data
    def transform_filter(self, equation_filter: str | FilterTransform):
        """
        Filters the chart with the given transformation.

        Parameters
        ----------
        equation_filter : str | FilterTransform
            The equation string of the filter transformation, or a Filter object (see Examples).

        Raises
        ------
        TypeError
            If equation is not a string or a Filter object.

        Notes
        -----
        Can be concatenated with the rest of functions of the Chart, without needing an asignation.

        Examples
        --------
        *Using transform_filter() giving the equation string:*

        >>> import aframexr
        >>> data = aframexr.URLData('./data.json')
        >>> filtered_chart = aframexr.Chart(data).mark_bar().encode(x='model', y='sales')
        >>> filtered_chart = filtered_chart.transform_filter('datum.motor=diesel')
        >>> #filtered_chart.show()

        *Using transform_filter() giving a Filter object*

        >>> import aframexr
        >>> data = aframexr.URLData('./data.json')
        >>> filtered_chart = aframexr.Chart(data).mark_bar().encode(x='model', y='sales')
        >>> filter_object = aframexr.FieldEqualPredicate(field='motor', equal='diesel')
        >>> filtered_chart = filtered_chart.transform_filter(filter_object)
        >>> #filtered_chart.show()
        """

        # Create a copy of the chart (in case of assignation, to preserve the main chart)
        filt_chart = self.copy()

        # Validate the type of equation_filter and get a filter object from the equation_filter
        if isinstance(equation_filter, str):
            filter_transform = FilterTransform.from_string(equation_filter)
        elif isinstance(equation_filter, FilterTransform):
            filter_transform = equation_filter
        else:
            raise TypeError(f'Expected string or FilterTransform object, got {type(equation_filter).__name__}.')

        # Add the information of the filter object to the specifications
        if not filt_chart._specifications.get('transform'):  # First time filtering the chart
            filt_chart._specifications.update({'transform': [filter_transform.equation_to_dict()]})  # Create field in specs
        else:  # Not the first filter of the chart
            filt_chart._specifications['transform'].append(filter_transform.equation_to_dict())  # Add filter to field
        return filt_chart  # Returns the copy of the chart
