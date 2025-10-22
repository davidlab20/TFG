"""BabiaXR like Vega-Altair library"""


import copy
import json
import marimo
from typing import Literal
from utils.sceneCreator import SceneCreator


class TopLevelMixin:
    """Top level chart class."""

    def __init__(self):
        self.specifications = {}  # Specifications of the chart(s), in JSON format

    # Importing charts
    @staticmethod
    def _create_chart_from_specs(specs: dict) -> 'TopLevelMixin':
        """
        Returns the chart from the received specifications in a JSON dictionary format.

        Parameters
        ----------
        specs : dict
            Specification dictionary in JSON format.

        Notes
        -----
        Suppose that specs is a dictionary (as this function is called by from_dict and from_json).
        """

        if specs['data'].get('url'):
            data = specs['data']['url']
        elif specs['data'].get('values'):
            data = specs['data']['values']
        else:
            raise KeyError('Specification must contain "data" key.')
        if specs.get('concat'):  # XConcat chart
            top_left_chart = Chart(data)
            top_left_chart.specifications.update(specs['concat'][0])
            top_right_chart = Chart(data)
            top_right_chart.specifications.update(specs['concat'][1])
            bottom_left_chart = Chart(data)
            bottom_left_chart.specifications.update(specs['concat'][2])
            bottom_right_chart = Chart(data)
            bottom_right_chart.specifications.update(specs['concat'][3])
            return XConcatChart(top_left_chart, top_right_chart, bottom_left_chart, bottom_right_chart)
        elif specs.get('hconcat'):  # HConcat chart
            left_chart = Chart(data)
            left_chart.specifications.update(specs['hconcat'][0])
            right_chart = Chart(data)
            right_chart.specifications.update(specs['hconcat'][1])
            return HConcatChart(left_chart, right_chart)
        elif specs.get('vconcat'):  # VConcat chart
            top_chart = Chart(data)
            top_chart.specifications.update(specs['vconcat'][0])
            bottom_chart = Chart(data)
            bottom_chart.specifications.update(specs['vconcat'][1])
            return VConcatChart(top_chart, bottom_chart)
        else:  # Chart
            simple_chart = Chart(data)
            simple_chart.specifications.update(specs)
            return simple_chart

    @staticmethod
    def from_dict(specs: dict) -> 'TopLevelMixin':
        """
        Create the chart from the JSON dict specifications.

        Parameters
        ----------
        specs : dict
            JSON specifications of the chart.

        Raises
        ------
        TypeError
            If specs is not a dictionary.
        """

        if isinstance(specs, dict):
            specifications = specs
        else:
            raise TypeError(f'Expected dict, got {type(specs).__name__} instead.')
        return TopLevelMixin._create_chart_from_specs(specifications)

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

        if isinstance(specs, str):
            specifications = json.loads(specs)
        else:
            raise TypeError(f'Expected str, got {type(specs).__name__} instead.')
        return TopLevelMixin._create_chart_from_specs(specifications)

    # Exporting charts
    def save(self, fp: str, fileFormat: Literal["json", "html"] = None):
        """
        Saves the chart into a file, supported formats are JSON and HTML.

        Parameters
        ----------
        fp : str
            File path.
        fileFormat : str (optional)
            Format of the file could be ["html", "json"].
            If no format is specified, the chart will be saved depending on the file extension.

        Raises
        ------
        NotImplementedError
            If fileFormat is invalid.
        """

        if fileFormat == 'html' or fp.endswith('.html'):
            with open(fp, 'w') as file:
                file.write(self.to_html())
                file.close()
        elif fileFormat == 'json' or fp.endswith('.json'):
            with open(fp, 'w') as file:
                json.dump(self.specifications, file)
                file.close()
        else:
            raise NotImplementedError

    # Showing the chart
    def show(self):
        """Shows the scene in the marimo notebook."""

        html_iframe_scene = SceneCreator.create_iframe_scene(self.specifications)
        return marimo.iframe(html_iframe_scene)

    # Chart formats
    def to_dict(self) -> dict:
        """Returns the chart specifications to a dictionary."""

        return self.specifications

    def to_html(self) -> str:
        """Returns the HTML representation of the scene."""

        return SceneCreator.create_iframe_scene(self.specifications)

    def to_json(self) -> str:
        """Returns the JSON string of the scene."""

        return str(self.specifications).replace("\'", "\"")  # Replace ' to " because of syntaxis


class Chart(TopLevelMixin):
    """
    Simple chart class.

    Parameters
    ----------
        data : str | list
            String like JSON format containing the data or JSON object of the data.

            It can also receive the url of the JSON file storing the data.

    Raises
    ------
    TypeError
        If data is not a string or a list of dictionaries.
    """

    def __init__(self, data: str | list[dict] = ''):

        super().__init__()
        if isinstance(data, str):
            if data.endswith('.json'):  # URL of the JSON file storing data
                self.specifications.update({'data': {'url': data}})
            else:  # Raw data in string
                self.specifications.update({'data': {'values': json.loads(data)}})
        elif isinstance(data, list):  # Data has been loaded
            self.specifications.update({'data': {'values': data}})
        else:
            raise TypeError(f'Expected str, got {type(data).__name__} instead.')

    # Concatenate charts
    def __and__(self, other):
        """
        Vertical concatenation of charts using symbol &.

        Examples
        --------
            >>> import babiaAltair
            >>> data1 = '...'
            >>> data2 = '...'
            >>> top_chart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
            >>> bottom_chart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
            >>> final_chart = top_chart & bottom_chart
            >>> #final_chart.show()
        """

        return VConcatChart(self, other)

    def __or__(self, other):
        """
        Horizontal concatenation of charts using symbol |.

        Examples
        --------
              >>> import babiaAltair
              >>> data1 = '...'
              >>> data2 = '...'
              >>> left_chart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
              >>> right_chart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
              >>> final_chart = left_chart | right_chart
              >>> #final_chart.show()
        """

        return HConcatChart(self, other)

    # Types of charts
    def mark_arc(self, inner_radius: int = 0):
        """
        Pie chart (default) and doughnut chart.

        Parameters
        ----------
        inner_radius : int (optional)
            Radius of inner arc (must be positive).

                - If the radius is 0 or not set, the chart would be a pie chart.
                - If the radius is greater than 0, the chart would be a doughnut chart.

        Raises
        ------
        ValueError
            If the inner_radius is lower than 0.
        """

        if inner_radius < 0:
            raise ValueError('Inner radius cannot be negative.')
        elif inner_radius == 0:  # Pie chart
            self.specifications.update({'mark': {'type': 'arc'}})
        else:  # Doughnut chart
            self.specifications.update({'mark': {'type': 'arc', 'innerRadius': inner_radius}})
        posX, posY, posZ = 0, 5, -5  # Default axis position of the pie chart
        self.specifications.update({'position': {'x': posX, 'y': posY, 'z': posZ}})
        return self

    def mark_bar(self):
        """Bars chart."""

        self.specifications.update({'mark': {'type': 'bar'}})
        posX, posY, posZ = 0, 0.5, -10  # Default axis position of the bar chart
        self.specifications.update({'position': {'x': posX, 'y': posY, 'z': posZ}})
        return self

    # Parameters of the chart
    def encode(self, theta: str = '', color: str = '', x: str = '', y: str = ''):
        """
        Completes and returns the necessary HTML to view the chart.

        Parameters
        ----------
        theta : str (optional)
            The key of the chart (use when marc_arc() is called).
        color : str (optional)
            Color of the chart (use when marc_arc() is called).
        x : str (optional)
            X axis of the chart (use when marc_bar() is called).
        y : str (optional)
            Y axis of the chart (use when marc_bar() is called).

        Raises
        ------
        SyntaxError
            If the arguments are not valid. Should receive "theta" and "color" or "x" and "y".
        """

        if theta and color:  # Pie chart
            self.specifications.update({'encoding': {'theta': {'field': theta, 'type': 'quantitative'},
                                                     'color': {'field': color, 'type': 'nominal'}}})
        elif x and y:  # Bar chart
            self.specifications.update({'encoding': {'x': {'field': x}, 'y': {'field': y}}})
        else:
            raise SyntaxError('Incorrect arguments using encode(). Should receive "theta" and "color" or "x" and "y".')
        return self

    # Copying the chart
    def copy(self):
        """Returns a copy of the chart."""

        return copy.deepcopy(self)  # Return a deep copy of the chart (changes in the copy do not affect the original)


# Multiple charts in the same scene
class HConcatChart(TopLevelMixin):
    """
    Horizontal concatenation o charts class. The concatenated chart stores copies of the charts.

    Parameters
    ----------
    left : Chart
        Chart to be concatenated (placed on the left).
    right : Chart
        Chart to be concatenated (placed on the right).

    Raises
    ------
    TypeError
        If left_chart is not a Chart or right_chart is not a Chart.

    Examples
    --------
        >>> import babiaAltair
        >>> data1 = '...'
        >>> data2 = '...'
        >>> left_chart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
        >>> right_chart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
        >>> final_chart = babiaAltair.HConcatChart(left_chart, right_chart)
        >>> #final_chart.show()
    """

    def __init__(self, left: Chart, right: Chart):

        super().__init__()
        if not isinstance(left, Chart) or not isinstance(right, Chart):
            raise TypeError('leftChart and rightChart must be of type Chart.')
        self.left = left.copy()  # Store a deep copy of the chart
        self.right = right.copy()  # Store a deep copy of the chart
        self.specifications = {'data': self.left.specifications['data']}  # Data is the same for both charts
        del self.left.specifications['data']  # Delete the data field of the left chart
        del self.right.specifications['data']  # Delete the data field of the right chart
        self.specifications.update({'hconcat': [self.left.specifications, self.right.specifications]})
        self.__reposition_charts()  # Change the position of the charts

    def __reposition_charts(self):
        """Repositions the charts in the scene (for horizontal concatenation)."""

        self.left.specifications['position']['x'] -= 5
        self.right.specifications['position']['x'] += 5

def concat(left: Chart, right: Chart) -> HConcatChart:
    """
    Horizontal concatenation of charts.

    Parameters
    ----------
    left : Chart
        Left chart.
    right : Chart
        Right chart.

    Raises
    ------
    TypeError
        If left or right are not of type Chart.

    Examples
    --------
        >>> import babiaAltair
        >>> data1 = '...'
        >>> data2 = '...'
        >>> left_chart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
        >>> right_chart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
        >>> final_chart = babiaAltair.concat(left_chart, right_chart)
        >>> #final_chart.show()
    """

    return HConcatChart(left, right)

def hconcat(left: Chart, right: Chart) -> HConcatChart:
    """
    Horizontal concatenation of charts.

    Parameters
    ----------
    left : Chart
        Left chart.
    right : Chart
        Right chart.

    Raises
    ------
    TypeError
        If left or right are not of type Chart.

    Examples
    --------
        >>> import babiaAltair
        >>> data1 = '...'
        >>> data2 = '...'
        >>> left_chart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
        >>> right_chart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
        >>> final_chart = babiaAltair.concat(left_chart, right_chart)
        >>> #final_chart.show()
    """

    return HConcatChart(left, right)


class VConcatChart(TopLevelMixin):
    """
    Vertical concatenation of charts class. The concatenated chart stores copies of the charts.

    Parameters
    ----------
    top : Chart
        Chart to be concatenated (placed on the top).
    bottom : Chart
        Chart to be concatenated (placed on the bottom).

    Raises
    ------
    TypeError
        If top is not a Chart or bottom is not a Chart.

    Examples
    --------
        >>> import babiaAltair
        >>> data1 = '...'
        >>> data2 = '...'
        >>> top_chart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
        >>> bottom_chart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
        >>> final_chart = babiaAltair.VConcatChart(top_chart, bottom_chart)
        >>> #final_chart.show()
    """

    def __init__(self, top: Chart, bottom: Chart):

        super().__init__()
        if not isinstance(top, Chart) or not isinstance(bottom, Chart):
            raise TypeError('upperChart and lowerChart must be of type Chart.')
        self.top = top.copy()  # Store a deep copy of the chart
        self.bottom = bottom.copy()  # Store a deep copy of the chart
        self.specifications = {'data': self.top.specifications['data']}  # Data is the same for both charts
        del self.top.specifications['data']  # Delete the data field of the top chart
        del self.bottom.specifications['data']  # Delete the data field of the bottom chart
        self.specifications.update({'vconcat': [self.top.specifications, self.bottom.specifications]})
        self.__repositionCharts()

    def __repositionCharts(self):
        """Repositions the charts in the scene (for vertical concatenation)."""

        self.top.specifications['position']['y'] += 5  # The top chart is moved in the Y axis
        self.top.specifications['position']['z'] -= 3  # The chart is placed farther for better visualization
        self.bottom.specifications['position']['z'] -= 3  # The chart is placed farther for better visualization

def vconcat(top: Chart, bottom: Chart) -> VConcatChart:
    """
    Vertical concatenation of charts.

    Parameters
    ----------
    top : Chart
        Top chart.
    bottom : Chart
        Bottom chart.

    Raises
    ------
    TypeError
        If top or bottom are not of type Chart.

    Examples
    --------
        >>> import babiaAltair
        >>> data1 = '...'
        >>> data2 = '...'
        >>> top_chart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
        >>> bottom_chart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
        >>> final_chart = babiaAltair.vconcat(top_chart, bottom_chart)
        >>> #final_chart.show()
    """

    return VConcatChart(top, bottom)


class XConcatChart(TopLevelMixin):
    """
    Concatenation of chart class. The concatenated chart stores copies of the charts.

    Parameters
    ----------
    top_left : Chart
        Chart to be concatenated (placed on the top left).
    top_right : Chart
        Chart to be concatenated (placed on the top right).
    bottom_left : Chart
        Chart to be concatenated (placed on the bottom left).
    bottom_right : Chart
        Chart to be concatenated (placed on the bottom right).

    Raises
    ------
    TypeError
        If top_left, top_right, bottom_left or bottom_right are not of type Chart.

    Examples
    --------
        >>> import babiaAltair
        >>> data1 = '...'
        >>> data2 = '...'
        >>> data3 = '...'
        >>> data4 = '...'
        >>> top_left_chart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
        >>> top_right_chart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
        >>> bottom_left = babiaAltair.Chart(data3).mark_bar().encode(x='xAxis3', y='yAxis3')
        >>> bottom_right = babiaAltair.Chart(data4).mark_bar().encode(x='xAxis4',y='yAxis4')
        >>> final_chart = babiaAltair.XConcatChart(top_left_chart, top_right_chart, bottom_left, bottom_right)
        >>> #final_chart.show()
    """

    def __init__(self, top_left: Chart, top_right: Chart, bottom_left: Chart, bottom_right: Chart):

        super().__init__()
        if not isinstance(top_left, Chart) or not isinstance(top_right, Chart) \
                or not isinstance(bottom_left, Chart) or not isinstance(bottom_right, Chart):
            raise TypeError('topLeftChart, topRightChart, bottomLeftChart and bottomRightChart must be of type Chart.')
        self.charts = [top_left.copy(), top_right.copy(), bottom_left.copy(), bottom_right.copy()]
        self.specifications = {'data': self.charts[0].specifications['data']}  # Data is the same for every chart
        self.specifications.update({'columns': 2})
        concat_specs = []
        for chart in self.charts:
            del chart.specifications['data']
            concat_specs.append(chart.specifications)
        self.specifications.update({'concat': concat_specs})
        self.__repositionCharts()

    def __repositionCharts(self):
        """Repositions the charts in the scene (for concatenation)."""

        # Top left chart
        self.charts[0].specifications['position']['x'] -= 5
        self.charts[0].specifications['position']['y'] += 5
        self.charts[0].specifications['position']['z'] -= 3  # The chart is placed farther for better visualization

        # Top right chart
        self.charts[1].specifications['position']['x'] += 5
        self.charts[1].specifications['position']['y'] += 5
        self.charts[1].specifications['position']['z'] -= 3  # The chart is placed farther for better visualization

        # Bottom left chart
        self.charts[2].specifications['position']['x'] -= 5
        self.charts[2].specifications['position']['z'] -= 3  # The chart is placed farther for better visualization

        # Bottom right chart
        self.charts[3].specifications['position']['x'] += 5
        self.charts[3].specifications['position']['z'] -= 3  # The chart is placed farther for better visualization
