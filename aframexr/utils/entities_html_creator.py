"""AframeXR entities HTML creator"""

from aframexr.utils.axis_creator import AxisCreator
from aframexr.utils.constants import ALL_TEMPLATES
from aframexr.utils.entity_creator import ChartCreator
from aframexr.utils.validators import AframeXRValidator


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

        Suppose that the parameters are correct for method calls of ChartCreator and AxisCreator.
        """

        # Validate chart type
        chart_type = chart_specs['mark']['type'] if isinstance(chart_specs['mark'], dict) else chart_specs['mark']
        AframeXRValidator.validate_chart_type(chart_type)

        # Chart HTML
        chart_html = ''
        base_html = ALL_TEMPLATES[chart_type]
        chart_object = ChartCreator.create_object(chart_type, chart_specs)  # Create the chart object

        group_specs = chart_object.get_group_specs()  # Get the base specifications of the group of elements
        chart_html += '<a-entity position="{pos}" rotation="{rotation}">\n'.format(**group_specs)
        elements_specs = chart_object.get_elements_specs()  # Get the specifications for each element of the chart
        for element in elements_specs:
            chart_html += '\t\t\t' + base_html.format(**element) + '\n'  # Tabulate the lines (better visualization)

        # Axis HTML
        axis_specs = chart_object.get_axis_specs()

        for ax in axis_specs:
            if axis_specs[ax]['start'] is None:
                continue  # If the axis is not displayed, continue with the next
            chart_html += f'\n\t\t\t<!-- {ax.upper()}-axis -->\n'  # Added HTML comment for better visualization
            chart_html += '\t\t\t' + AxisCreator.create_axis_html(axis_specs[ax]['start'], axis_specs[ax]['end']) + '\n'
            for label in range(len(axis_specs[ax]['labels_pos'])):
                label_pos = axis_specs[ax]['labels_pos'][label]
                label_rotation = axis_specs[ax]['labels_rotation']
                label_value = axis_specs[ax]['labels_values'][label]
                label_align = axis_specs[ax]['labels_align']
                chart_html += '\t\t\t' + AxisCreator.create_label_html(
                    label_pos, label_rotation, label_value, label_align
                ) + '\n'

        # Close the group
        chart_html += '\t\t</a-entity>\n\t\t'
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

        charts_list = specs.get('concat') or specs.get('layer')  # Charts could be concatenated using layer
        if charts_list:  # The scene has more than one chart
            for chart in charts_list:
                charts_html += ChartsHTMLCreator._create_simple_chart_html(chart) + '\n\t\t'  # Tabulate (visualization)
        else:  # The scene has only one chart
            charts_html = ChartsHTMLCreator._create_simple_chart_html(specs)
        charts_html = charts_html.removesuffix('\n\t\t')  # Delete the last tabulation
        return charts_html
