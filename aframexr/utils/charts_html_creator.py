"""AframeXR charts HTML creator"""

from aframexr.utils.chart_creator import BarChartCreator, PointChartCreator


class ChartsHTMLCreator:
    """Charts HTML creator class."""

    def __init__(self):
        pass

    @staticmethod
    def _create_simple_chart_html(chart_specs: dict):
        """
        Returns the HTML of the elements that compose the chart.

        Parameters
        ----------
        chart_specs : dict
            Chart specifications.

        Notes
        -----
        Supposing that chart_specs is a dictionary (at this method has been called from self.create_charts_html).

        Suppose that the parameters are correct for get_chart_specs() method calls.
        """

        # Validate chart type
        valid_chart_types = ['bar', 'point']
        chart_type = chart_specs['mark']['type']
        if chart_type not in valid_chart_types:
            raise NotImplementedError('That chart type is not supported.')

        # Create the HTML of the chart
        chart_html = ''
        if chart_type == 'bar':
            elements_specs = BarChartCreator.get_chart_specs(chart_specs)
            base_html = '<a-box position="{pos}" width="{width}" height="{height}" depth="{depth}" color="{color}"></a-box>'
            for element in elements_specs:
                chart_html += base_html.format(**element) + '\n\t\t'  # Tabulate the lines (better visualization)
        if chart_type == 'point':
            elements_specs = PointChartCreator.get_chart_specs(chart_specs)
            base_html = '<a-sphere position="{pos}" radius="{radius}" color="{color}"></a-sphere>'
            for element in elements_specs:
                chart_html += base_html.format(**element) + '\n\t\t'  # Tabulate the lines (better visualization)

        # Create HTML of the axis

        return chart_html

    @staticmethod
    def create_charts_html(specs: dict):
        """
        Returns the HTML of the charts that compose the scene.

        Parameters
        ----------
        specs : dict
            Specifications of all the charts composing the scene.

        Notes
        -----
        Supposing that specs is a dictionary, at this method has been called from SceneCreator.create_scene().

        Suppose that chart_specs is a dictionary for self._create_simple_chart_html(chart_specs).
        """

        charts_html = ''
        if specs.get('concat'):  # The scene has more than one chart
            for chart in specs.get('concat'):
                charts_html += ChartsHTMLCreator._create_simple_chart_html(chart)
        else:  # The scene has only one chart
            charts_html = ChartsHTMLCreator._create_simple_chart_html(specs)
        charts_html = charts_html.removesuffix('\n\t\t')  # Delete the last tabulation
        return charts_html
