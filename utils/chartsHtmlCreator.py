"""BabiaXR charts HTML creator (for SceneCreator)"""


from typing import Literal


class ChartsHTMLCreator:
    """Charts HTML creator class. Used for SceneCreator class."""

    def __init__(self):
        pass

    @staticmethod
    def create_charts_html(specs: dict, concatenation: Literal['concat', 'hconcat', 'vconcat'] = '') -> str:
        """
        Creates the HTML of the charts according to the JSON specifications.

        Parameters
        ----------
        specs : dict
            JSON Schema specifications.
        concatenation : Literal['concat', 'hconcat', 'vconcat'], optional
            Concatenation mode of the charts (optional).

        Returns
        -------
        charts_html : str
            HTML of the charts.

        Raises
        ------
        ValueError
            If a key has an invalid value.

        Notes
        -----
        Should receive specs as a dictionary (as it has been called from ChartsHTMLCreator).

        Suppose concatenation is in ['concat', 'hconcat', 'vconcat'] or no concatenation for posterior functions.
        """

        if not concatenation:
            charts_html = SimpleChartHTMLCreator.create_chart_html(specs)  # Specs are for a single chart
        else:
            if concatenation in ['concat', 'hconcat', 'vconcat']:
                charts_html = MultipleChartHTMLCreator.create_charts_html(specs, concatenation)
            else:
                raise ValueError(f'Incorrect concatenation mode, got {concatenation}.')
        return charts_html


class SimpleChartHTMLCreator:
    """Simple chart HTML creator class. Creates the HTML of the chart according to the JSON specifications."""

    def __init__(self):
        pass

    @staticmethod
    def _get_chart_type(mark: str | dict) -> str:
        """
        Returns the labels of the bar chart.

        Parameters
        ----------
        mark : str | dict
            Mark field of the specs.

        Returns
        -------
        babia_chart : str
            Type of the chart in BabiaXR.

        Raises
        ------
        TypeError
            If 'mark' is not a string or a dictionary.

        ValueError
            If a key has an invalid value.
        """

        # Validate mark is OK
        if isinstance(mark, dict):
            vega_type = mark['type']
        elif isinstance(mark, str):
            vega_type = mark
        else:
            raise TypeError('Invalid mark format.')

        # Get the equivalence between the Vega chart and the BabiaXR chart
        valid_types = {'arc': ['pie', 'doughnut'], 'bar': 'bar'}  # Types of charts (Vega: BabiaXR)
        if vega_type == 'arc':
            arc_possibilities = valid_types[mark['type']]
            if mark.get('innerRadius'):
                if mark['innerRadius'] == 0:
                    babia_chart = arc_possibilities[0]
                elif mark['innerRadius'] > 0:
                    babia_chart = arc_possibilities[1]
                else:  # innerRadius < 0
                    raise ValueError('Invalid mark format, innerRadius should be positive.')
            else:  # Default arc chart (pie chart)
                babia_chart = arc_possibilities[0]
        elif vega_type == 'bar':
            babia_chart = valid_types[mark]
        else:  # Type not in valid_types
            raise ValueError(f'Invalid mark type. Expected {valid_types.keys()}, got {vega_type}.')
        return babia_chart

    @staticmethod
    def _get_bar_labels(encoding: dict) -> tuple[str, str]:
        """
        Returns the labels of the bar chart.

        Parameters
        ----------
        encoding : dict
            Dictionary containing the encoding of the chart.

        Returns
        -------
        x, y: tuple[str, str]
            Labels of the bar chart (x, y).

        Raises
        ------
        TypeError
            If encoding, encoding.x or encoding.y are not dictionaries.
        KeyError
            If a key is not found when necessary.
        """

        # Validate specs are OK
        if not isinstance(encoding, dict):
            raise TypeError('Incorrect format of encoding, it must be a dictionary.')
        if not 'x' and 'y' in encoding.keys():
            raise KeyError('Incorrect format of encoding, it does not contain "x" and "y".')
        if not isinstance(encoding['x'], dict):
            raise TypeError('Incorrect format of "encoding.x", it must be a dictionary.')
        if not isinstance(encoding['y'], dict):
            raise TypeError('Incorrect format of "encoding.y", it must be a dictionary.')

        # Validate and get the x-axis and y-axis of the chart
        x = encoding['x']['field']
        if x is None:
            raise KeyError('Incorrect format of "encoding.x", does not contain "field".')
        y = encoding['y']['field']
        if y is None:
            raise KeyError('Incorrect format of "encoding.y", does not contain "field".')
        return x, y

    @staticmethod
    def _get_pie_labels(encoding: dict) -> tuple[str, str]:
        """
        Returns the labels of the pie chart.

        Parameters
        ----------
        encoding : dict
            Dictionary containing the encoding of the chart.

        Returns
        -------
        theta, color: tuple[str, str]
            Labels of the pie chart (theta, color).

        Raises
        ------
        TypeError
            If encoding, encoding.theta or encoding.color are not dictionaries.
        KeyError
            If a key is not found when necessary.
        """

        # Validate specs are OK
        if not isinstance(encoding, dict):
            raise TypeError('Incorrect format of encoding, it must be a dictionary.')
        if not 'theta' and 'color' in encoding.keys():
            raise KeyError('Incorrect format of encoding, it does not contain "theta" and "color".')
        if not isinstance(encoding['theta'], dict):
            raise TypeError('Incorrect format of "encoding.theta", it must be a dictionary.')
        if not isinstance(encoding['color'], dict):
            raise TypeError('Incorrect format of "encoding.color", it must be a dictionary.')

        # Validate and get the theta and color of the chart
        theta = encoding['theta']['field']
        if theta is None:
            raise KeyError('Incorrect format of "encoding.theta", does not contain "field".')
        color = encoding['color']['field']
        if color is None:
            raise KeyError('Incorrect format of "encoding.color", does not contain "field".')
        return theta, color

    @staticmethod
    def create_chart_html(specs: dict) -> str:
        """
        Creates the HTML of the chart according to the JSON specifications.

        Parameters
        ----------
        specs : dict
            JSON Schema specifications.

        Returns
        -------
        chart_html : str
            HTML of the chart.
        position_delta : tuple[int, int, int], optional
            Position delta of the chart.

        Raises
        ------
        TypeError
            If a key has not a valid format.
        KeyError
            If a key is not found in the JSON specification.
        ValueError
            If a key has an invalid value.

        Notes
        -----
        Should receive specs as a dictionary (as it has been called from ChartsHTMLCreator).
        """

        # Validate specs are OK
        if not 'mark' in specs:
            raise KeyError('Specs does not contain "mark".')
        if not 'encoding' in specs:
            raise KeyError('Specs does not contain "encoding".')
        chart_type = SimpleChartHTMLCreator._get_chart_type(specs['mark'])

        # Create the HTML of the chart
        from utils.sceneCreator import DATA_QUERY_ID
        if chart_type in ['pie', 'doughnut']:
            theta, color = SimpleChartHTMLCreator._get_pie_labels(specs['encoding'])
            if not specs.get('position'):  # No position set in specifications (specs from 2D charts)
                specs['position'] = {'x': 0, 'y': 0, 'z': 0}  # Position is set to the coordinate origin
            pos_x = specs['position']['x']
            pos_y = specs['position']['y']
            pos_z = specs['position']['z']
            chart_html = f"""
            <a-entity babia-{chart_type}='from: {DATA_QUERY_ID}; legend: true; palette: blues; key: {theta};
                size: {color}' position="{pos_x} {pos_y} {pos_z}" rotation="90 0 0">
            </a-entity>
            """
        elif chart_type == 'bar':
            x, y = SimpleChartHTMLCreator._get_bar_labels(specs['encoding'])
            if not specs.get('position'):  # No position set in specifications (specs from 2D charts)
                specs['position'] = {'x': 0, 'y': 0, 'z': 0}  # Position is set to the coordinate origin
            pos_x = specs['position']['x']
            pos_y = specs['position']['y']
            pos_z = specs['position']['z']
            chart_html = f"""
                <a-entity babia-bars='from: {DATA_QUERY_ID}; legend: true; palette: ubuntu; x_axis: {x}; height: {y}'
                    position="{pos_x} {pos_y} {pos_z}" rotation="0 0 0">
                </a-entity>
            """
        else:  # Should never enter here; it the chart_type is incorrect en error should have raised before
            raise ValueError('Invalid chart type. Something occurs before, should never get here.')
        return chart_html


class MultipleChartHTMLCreator:
    """Multiple chart HTML creator class. Creates the HTML of the chart according to the JSON specifications."""

    def __init__(self):
        pass

    @staticmethod
    def create_charts_html(specs: dict, concatenation: Literal['concat', 'hconcat', 'vconcat']) -> str:
        """
        Creates the HTML of the concatenated charts according to the JSON specifications.

        Parameters
        ----------
        specs : dict
            JSON Schema specifications.
        concatenation : Literal['concat', 'hconcat', 'vconcat']
            Concatenation mode of the charts.

        Returns
        -------
        charts_html : str
            HTML of the chart.

        Notes
        -----
        Should receive specs as a dictionary (as it has been called from ChartsHTMLCreator).

        Should receive concatenation in ['concat', 'hconcat', 'vconcat'], as it has been called from ChartsHTMLCreator.
        """

        charts_html = ''
        for chart_specs in specs[concatenation]:
            charts_html += SimpleChartHTMLCreator.create_chart_html(chart_specs)
        return charts_html
