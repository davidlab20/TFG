"""AframeXR charts HTML creator"""

from aframexr.utils.axis_html_creator import AxisHTMLCreator
from aframexr.utils.chart_creator import ChartCreator


class ChartsHTMLCreator:
    """Charts HTML creator class."""

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
        elements_specs = ChartCreator.get_elements_specs(chart_type, chart_specs)
        if chart_type == 'bar':
            base_html = '<a-box position="{pos}" width="{width}" height="{height}" depth="{depth}" color="{color}"></a-box>'
        elif chart_type == 'point':
            base_html = '<a-sphere position="{pos}" radius="{radius}" color="{color}"></a-sphere>'
        else:  # Should never enter here, should have raised error before
            raise RuntimeError('Something went wrong. Should never happen.')
        # Elements HTML
        for element in elements_specs:
            chart_html += base_html.format(**element) + '\n\t\t'  # Tabulate the lines (better visualization)

        # Axis HTML
        start, end_x, end_y, end_z = ChartCreator.get_axis_specs(chart_type, chart_specs)
        chart_html += AxisHTMLCreator.create_axis_html(start, end_x, end_y, end_z)

        chart_html.removesuffix('\n\t\t')  # Remove the last tabulation

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
