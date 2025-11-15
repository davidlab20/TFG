"""AframeXR charts HTML creator"""

from aframexr.utils.axis_html_creator import AxisHTMLCreator
from aframexr.utils.constants import CHART_TEMPLATES
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

        Suppose that the parameters are correct for method calls of ChartCreator and AxisHTMLCreator.
        """

        # Validate chart type
        chart_type = chart_specs['mark']['type']
        if chart_type not in CHART_TEMPLATES.keys():
            raise NotImplementedError('That chart type is not supported.')

        # Chart HTML
        chart_html = ''
        base_html = CHART_TEMPLATES[chart_type]
        elements_specs = ChartCreator.get_elements_specs(chart_type, chart_specs)
        for element in elements_specs:
            chart_html += base_html.format(**element) + '\n\t\t'  # Tabulate the lines (better visualization)

        # Axis HTML
        starts, ends = [], []
        starts.append(ChartCreator.get_x_axis_specs(chart_type, chart_specs)[0])  # X-axis start
        ends.append(ChartCreator.get_x_axis_specs(chart_type, chart_specs)[1])  # X-axis end
        starts.append(ChartCreator.get_y_axis_specs(chart_type, chart_specs)[0])  # Y-axis start
        ends.append(ChartCreator.get_y_axis_specs(chart_type, chart_specs)[1])  # Y-axis end
        for axis in range(len(starts)):  # Starts and ends has the same number of elements
            chart_html += AxisHTMLCreator.create_axis_html(starts[axis], ends[axis])
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
