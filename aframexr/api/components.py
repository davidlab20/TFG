"""AframeXR components"""

import copy
import json
import marimo

try:
    import pandas as pd
    from pandas import DataFrame
except ImportError:
    DataFrame = object
    pd = None

from typing import Literal, Union

from aframexr.api.aggregate import AggregatedFieldDef
from aframexr.api.data import Data, URLData
from aframexr.api.encoding import Encoding, X, Y, Z
from aframexr.api.filters import FilterTransform
from aframexr.utils.constants import *
from aframexr.utils.scene_creator import SceneCreator
from aframexr.utils.validators import AframeXRValidator


class TopLevelMixin:
    """Top level chart class."""

    def __init__(self, specs: dict):
        if specs: AframeXRValidator.validate_chart_specs(specs)  # Validate specs if not initializing empty dict
        self._specifications = specs

    # Concatenating charts
    def __add__(self, other):
        """
        Concatenation of charts (place charts in the same scene).
        Creates and returns a new scene with the charts. The original charts are not modified.
        """

        if not isinstance(other, TopLevelMixin):
            raise TypeError(f"Cannot add {type(other).__name__} to {type(self).__name__}.")

        self_specs_list = self._specifications.get('concat', [self._specifications])
        other_specs_list = other._specifications.get('concat', [other._specifications])

        copy_of_the_chart = self.copy()  # Create a copy to modify
        copy_of_the_chart._specifications = {'concat': self_specs_list + other_specs_list}
        return copy_of_the_chart

    # Copy of the chart
    def __deepcopy__(self, memo):
        """Optimized deepcopy method."""

        new_instance = self.__class__.__new__(self.__class__)
        memo[id(self)] = new_instance
        new_instance._specifications = copy.deepcopy(self._specifications, memo)
        return new_instance

    def copy(self):
        """Returns a deep copy of the chart."""

        return copy.deepcopy(self)

    # Importing charts
    @staticmethod
    def from_dict(specs: dict) -> 'Chart':
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

        AframeXRValidator.validate_type(specs, dict)
        chart = Chart()
        chart._specifications = specs
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
        """

        AframeXRValidator.validate_type(specs, str)
        chart = Chart()
        chart._specifications = json.loads(specs)
        return chart

    # Exporting charts
    def save(self, fp: str, file_format: Literal['json', 'html'] = None):
        """
        Saves the chart into a file, supported formats are JSON and HTML.

        Parameters
        ----------
        fp : str
            File path.
        file_format : str (optional)
            Format of the file could be ['html', 'json'].
            If no format is specified, the chart will be saved depending on the file extension.

        Raises
        ------
        ValueError
            If file_format is invalid.
        """

        AframeXRValidator.validate_type(fp, str)
        if file_format == 'html' or fp.endswith('.html'):
            with open(fp, 'w') as file:
                file.write(self.to_html())
        elif file_format == 'json' or fp.endswith('.json'):
            with open(fp, 'w') as file:
                json.dump(self._specifications, file, indent=4)
        else:
            raise ValueError('Invalid file format.')

    # Showing the scene
    def show(self):
        """Show the scene in the Marimo notebook."""

        AframeXRValidator.validate_chart_specs(self._specifications)
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
        Position of the chart. The format is: 'x y z'. Refers to the position for the origin of coordinate system.
    rotation : str (optional)
        Rotation of the chart in degrees. The format is: 'x y z'. The rotation axis is the coordinate system.

    Raises
    ------
    TypeError
        If data is not a Data or URLData object.
    ValueError
        If position or rotation are invalid.
    """

    def _define_data(self, data: Data | URLData | DataFrame):
        """Defines the data field in the specifications."""

        if isinstance(data, Data):
            self._specifications.update({'data': {'values': data.values}})
        elif isinstance(data, URLData):
            self._specifications.update({'data': {'url': data.url}})
        elif pd is not None and isinstance(data, pd.DataFrame):
            self._specifications.update({'data': {'values': data.to_dict(orient='records')}})
        else:
            raise TypeError(f'Expected Data | URLData | pd.DataFrame, got {type(data).__name__} instead.')

    def _define_position(self, position: str):
        """Defines the position field in the specifications."""

        pos_axes = position.strip().split()
        if len(pos_axes) != 3:
            raise ValueError(f'The position: {position} is not correct. Must be "x y z".')
        for axis in pos_axes:
            try:
                float(axis)
            except ValueError:
                raise ValueError('The position values must be numeric.')
        self._specifications.update({'position': f'{pos_axes[0]} {pos_axes[1]} {pos_axes[2]}'})
        return self

    def _define_rotation(self, rotation: str):
        rot_axes = rotation.strip().split()
        if len(rot_axes) != 3:
            raise ValueError(f'The rotation: {rotation} is not correct. Must be "x y z".')
        for axis in rot_axes:
            try:
                float(axis)
            except ValueError:
                raise ValueError('The rotation values must be numeric.')
        self._specifications.update({'rotation': f'{rot_axes[0]} {rot_axes[1]} {rot_axes[2]}'})
        return self

    def __init__(self, data: Data | URLData | DataFrame = None, position: str = DEFAULT_CHART_POS,
                 rotation: str = DEFAULT_CHART_ROTATION, height: float = DEFAULT_MAX_HEIGHT,
                 width: float = DEFAULT_MAX_WIDTH):
        super().__init__({})  # Initiate specifications

        if data is not None: self._define_data(data)
        self._define_position(position)
        self._define_rotation(rotation)

        AframeXRValidator.validate_type(height, Union[float | int])
        AframeXRValidator.validate_type(width, Union[float | int])

        if height <= 0:
            raise ValueError('The height must be greater than 0.')
        self._specifications.update({'height': height})
        if width <= 0:
            raise ValueError('The width must be greater than 0.')
        self._specifications.update({'width': width})

    # Types of charts
    def mark_arc(self, radius: float = DEFAULT_PIE_RADIUS):
        """
        Pie chart and doughnut chart.

        Parameters
        ----------
        radius : float (optional)
            Outer radius of the pie chart. If not specified, using default. Must be greater than 0.
        """

        AframeXRValidator.validate_type(radius, Union[float | int])

        self._specifications.update({'mark': {'type': 'arc'}})
        if radius <= 0:
            raise ValueError('The radius must be greater than 0.')
        self._specifications['mark'].update({'radius': radius})
        return self

    def mark_bar(self, size: float = DEFAULT_BAR_AXIS_SIZE):
        """
        Bars chart.

        Parameters
        ----------
        size : float (optional)
            Width of the bars. If not specified, using default. Must be greater than 0.
        """

        AframeXRValidator.validate_type(size, Union[float | int])

        self._specifications.update({'mark': {'type': 'bar'}})
        if size <= 0:
            raise ValueError('The size must be greater than 0.')
        self._specifications['mark'].update({'size': size})
        return self

    def mark_gltf(self, scale: str = DEFAULT_GLTF_SCALE):
        """
        GLTF model.

        Parameters
        ----------
        scale : str (optional)
            Scale of the GLTF model (from its original scale).

            **Format: 'x y z'** (values can be negative, works like a mirror).

            If an axis value is not specified, that value will be 1 (for example, '2 2' is the same as '2 2 1').

            If more than 3 axes are specified, then the first 3 axes will be used.
        """

        AframeXRValidator.validate_type(scale, str)

        self._specifications.update({'mark': {'type': 'gltf'}})
        self._specifications['mark'].update({'scale': scale})
        return self

    def mark_image(self, width: float = DEFAULT_IMAGE_WIDTH, height: float = DEFAULT_IMAGE_HEIGHT):
        """
        Image.

        Parameters
        ----------
        width : float (optional)
            Width of the image. If not specified, using default. Must be greater than 0.
        height : float (optional)
            Height of the image. If not specified, using default. Must be greater than 0.

        Raises
        ------
        ValueError
            If width or height are not greater than 0.
        """

        AframeXRValidator.validate_type(width, Union[float | int])
        AframeXRValidator.validate_type(height, Union[float | int])

        self._specifications.update({'mark': {'type': 'image'}})
        if width <= 0:
            raise ValueError('The width must be greater than 0.')
        self._specifications['mark'].update({'width': width})
        if height <= 0:
            raise ValueError('The height must be greater than 0.')
        self._specifications['mark'].update({'height': height})
        return self

    def mark_point(self, size: float = DEFAULT_POINT_RADIUS):
        """
        Scatter plot and bubble chart.

        Parameters
        ----------
        size : float (optional)
            Maximum radius of the point. If not specified, using default. Must be greater than 0.

        Raises
        ------
        ValueError
            If size or height are not greater than 0.
        """

        AframeXRValidator.validate_type(size, Union[float | int])

        self._specifications.update({'mark': {'type': 'point'}})
        if size <= 0:
            raise ValueError('The size must be greater than 0.')
        self._specifications['mark'].update({'max_radius': size})
        return self

    # Parameters of the chart
    def encode(self, color: str = '', size: str = '', theta: str = '', x: str | X = '', y: str | Y = '',
               z: str | Z = ''):
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
        if color:
            AframeXRValidator.validate_type(color, str)
            filled_params.update({'color': color})
        if size:
            AframeXRValidator.validate_type(size, str)
            filled_params.update({'size': size})
        if theta:
            AframeXRValidator.validate_type(theta, str)
            filled_params.update({'theta': theta})
        if x:
            AframeXRValidator.validate_type(x, Union[str | X])
            filled_params.update({'x': x})
        if y:
            AframeXRValidator.validate_type(y, Union[str | Y])
            filled_params.update({'y': y})
        if z:
            AframeXRValidator.validate_type(z, Union[str | Z])
            filled_params.update({'z': z})

        # Verify the argument combinations
        if self._specifications['mark']['type'] in ['bar', 'point'] and sum([x != '', y != '', z != '']) < 2:
            raise ValueError('At least 2 of (x, y, z) must be specified.')
        if self._specifications['mark']['type'] == 'arc' and (not theta or not color):
            if not theta: raise ValueError('Parameter theta must be specified in arc chart.')
            if not color: raise ValueError('Parameter color must be specified in arc chart.')

        # Do the encoding
        self._specifications.update({'encoding': {}})
        for param_key in filled_params:
            param_value = filled_params[param_key]
            if isinstance(param_value, Encoding):
                self._specifications['encoding'].update(param_value.to_dict())
            else:
                formula, encoding_type = Encoding.split_field_and_encoding(param_value)
                field, aggregate_op = AggregatedFieldDef.split_operator_field(formula)

                self._specifications['encoding'].update({param_key: {'field': field}})
                if aggregate_op:
                    self._specifications['encoding'][param_key].update({'aggregate': aggregate_op})
                if encoding_type:
                    self._specifications['encoding'][param_key].update({'type': encoding_type})
        return self

    def properties(self, data: Data | URLData | DataFrame = None, position: str = '',
                   rotation: str = ''):
        """Modify general properties of the chart."""

        if data is not None: self._define_data(data)
        if position: self._define_position(position)
        if rotation: self._define_rotation(rotation)

        return self

    # Modifying data
    def transform_aggregate(self, groupby: list | None = None, **kwargs):
        """
        Aggregates the data with the specified aggregate function, grouped by the specified groupby.

        Parameters
        ----------
        groupby : list | None
            Data fields that will be grouped, optional. If not set, the defined fields in encode() method will be taken.
        kwargs : dict
            Format is: <new_field>=<aggregate_op>(<data_field>).
        """

        AframeXRValidator.validate_type(groupby, Union[list | None])

        # Create a copy of the chart (in case of assignation, to preserve the main chart)
        aggreg_chart = self.copy()

        if len(kwargs) == 0:  # At least one aggregation needs to be defined in kwargs
            raise TypeError('transform_aggregate() missing required aggregate fields.')

        aggregates_to_dict = []
        for as_field, aggregate_formula in kwargs.items():
            field, aggregate_op = AggregatedFieldDef.split_operator_field(str(aggregate_formula))
            aggregate_object = AggregatedFieldDef(aggregate_op, field, as_field)
            aggregates_to_dict.append(aggregate_object.to_dict())

        aggregate_specs = {'aggregate': aggregates_to_dict}
        if groupby:
            aggregate_specs['groupby'] = groupby

        if not aggreg_chart._specifications.get('transform'):  # First time filtering the chart (create field)
            aggreg_chart._specifications.update({'transform': [aggregate_specs]})
        else:  # Not the first filter of the chart (add to aggregates)
            aggreg_chart._specifications['transform'].append(aggregate_specs)
        return aggreg_chart

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
        Can be concatenated with the rest of functions of the Chart, without needing an asignation. It can also be
        concatenated several times (the result will be an addition of the filters, in order of assignation).

        If the result of the filters is empty data, a warning is raised.

        Examples
        --------
        *Using transform_filter() giving the equation string:*

        >>> import aframexr
        >>> data = aframexr.URLData('./data.json')
        >>> chart = aframexr.Chart(data).mark_bar().encode(x='model', y='sales')
        >>> filtered_chart = chart.transform_filter('datum.motor == diesel')
        >>> #filtered_chart.show()

        *Using transform_filter() giving a Filter object*

        >>> import aframexr
        >>> data = aframexr.URLData('./data.json')
        >>> chart = aframexr.Chart(data).mark_bar().encode(x='model', y='sales')
        >>> filter_object = aframexr.FieldEqualPredicate(field='motor', equal='diesel')
        >>> filtered_chart = chart.transform_filter(filter_object)
        >>> #filtered_chart.show()
        """

        # Validate the type of equation_filter and get a filter object from the equation_filter
        if isinstance(equation_filter, str):
            filter_transform = FilterTransform.from_string(equation_filter)
        elif isinstance(equation_filter, FilterTransform):
            filter_transform = equation_filter
        else:
            raise TypeError(f'Expected str | FilterTransform, got {type(equation_filter).__name__} instead.')

        # Create a copy of the chart (in case of assignation, to preserve the main chart)
        filt_chart = self.copy()

        # Add the information of the filter object to the specifications
        if not filt_chart._specifications.get('transform'):  # First time filtering the chart
            filt_chart._specifications.update({'transform': [filter_transform.equation_to_dict()]})  # Create field
        else:  # Not the first filter of the chart
            filt_chart._specifications['transform'].append(filter_transform.equation_to_dict())  # Add filter to field
        return filt_chart  # Returns the copy of the chart
