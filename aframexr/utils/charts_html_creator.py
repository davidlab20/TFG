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
        chart_object = ChartCreator.create_object(chart_type, chart_specs)  # Create the chart object
        elements_specs = chart_object.get_elements_specs()  # Get the specifications for each element of the chart
        for element in elements_specs:
            chart_html += base_html.format(**element) + '\n\t\t'  # Tabulate the lines (better visualization)

        # X-axis HTML
        axis_specs = chart_object.get_axis_specs()
        chart_html += AxisHTMLCreator.create_axis_html(axis_specs['x']['start'], axis_specs['x']['end']) + '\n\t\t'
        for label in range(len(axis_specs['x']['labels_pos'])):
            label_pos = axis_specs['x']['labels_pos'][label]
            label_rotation = '-90 0 -90'
            label_value = axis_specs['x']['labels_values'][label]
            chart_html += AxisHTMLCreator.create_label_html(label_pos, label_rotation, label_value) + '\n\t\t'

        # Y-axis HTML
        chart_html += AxisHTMLCreator.create_axis_html(axis_specs['y']['start'], axis_specs['y']['end']) + '\n\t\t'
        for label in range(len(axis_specs['y']['labels_pos'])):
            label_pos = axis_specs['y']['labels_pos'][label]
            label_rotation = '0 0 0'
            label_value = axis_specs['y']['labels_values'][label]
            chart_html += AxisHTMLCreator.create_label_html(label_pos, label_rotation, label_value) + '\n\t\t'

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
