"""AframeXR entities HTML creator"""

from .axis_creator import AxisCreator
from .chart_creator import ChartCreator
from .element_creator import ElementCreator


class ChartsHTMLCreator:
    """Charts HTML creator class."""

    @staticmethod
    def _create_chart_html(chart_specs: dict) -> str:
        chart_type = chart_specs['mark']['type'] if isinstance(chart_specs['mark'], dict) else chart_specs['mark']

        # Chart HTML
        chart_object = ChartCreator.create_object(chart_type, chart_specs)  # Create the chart object

        group_specs = chart_object.get_group_specs()  # Get the base specifications of the group of elements
        chart_html = '<a-entity{attributes}>'.format(
            attributes=''.join(f' {key.replace("_", "-")}="{value}"' for key, value in group_specs.items())
        ) + "  <!-- Chart's box (modify this values if you want to change position or rotation) -->\n"
        chart_html += f'\t\t\t<a-entity position="{chart_object.get_relative_bottom_left_corner_position()}">\n'
        elements = chart_object.get_elements()  # Get the specifications for each element of the chart
        for element in elements:
            chart_html += '\t\t\t\t' + element.get_element_html() + '\n'  # Tabulate the lines (better visualization)

        # Axis HTML
        axes_specs = chart_object.get_axes_specs()

        for ax, ax_specs in axes_specs.items():
            chart_html += f'\n\t\t\t\t<!-- {ax.upper()}-axis -->\n'  # Added HTML comment for better visualization
            chart_html += '\t\t\t\t' + AxisCreator.create_axis_html(ax_specs['start'], ax_specs['end']) + '\n'
            for label_pos, label_value in zip(ax_specs['labels_pos'], ax_specs['labels_values']):
                label_rotation = ax_specs['labels_rotation']
                label_align = ax_specs['labels_align']
                chart_html += '\t\t\t\t' + AxisCreator.create_label_html(
                    label_pos, label_rotation, label_value, label_align
                ) + '\n'

        # Close the groups
        chart_html += '\t\t\t</a-entity>\n'
        chart_html += '\t\t</a-entity>\n\t\t'
        return chart_html

    @staticmethod
    def _create_element_html(element_specs: dict) -> str:
        element_type = element_specs['element']
        element_object = ElementCreator.create_object(element_type, element_specs)
        return element_object.get_element_html()

    @staticmethod
    def _create_entity_html(chart_specs: dict) -> str:
        """
        Returns the HTML of the elements that compose the entity.

        Parameters
        ----------
        chart_specs : dict
            Chart specifications.

        Notes
        -----
        Supposing that chart_specs is a dictionary (at this method has been called from self.create_charts_html).

        Suppose that the parameters are correct for method calls of ChartCreator and AxisCreator.
        """
        if 'mark' in chart_specs:
            html = ChartsHTMLCreator._create_chart_html(chart_specs)
        elif 'element' in chart_specs:
            html = ChartsHTMLCreator._create_element_html(chart_specs)
        else:  # pragma: no cover (should never enter here, as chart_specs should have previously been validated)
            raise RuntimeError('Unreachable code: chart_specs should have been validated earlier')

        return html

    @staticmethod
    def create_charts_html(specs: dict) -> str:
        """
        Returns the HTML of the charts that compose the scene.

        Parameters
        ----------
        specs : dict
            Specifications of all the charts composing the scene.

        Notes
        -----
        Supposing that specs is a dictionary, at this method has been called from SceneCreator.create_scene().

        Suppose that chart_specs is a dictionary for self._create_entity_html(chart_specs).
        """
        charts_html = ''

        charts_list = specs.get('concat')
        if charts_list:  # The scene has more than one chart
            for chart in charts_list:
                charts_html += ChartsHTMLCreator._create_entity_html(chart) + '\n\t\t'  # Tabulate (visualization)
        else:  # The scene has only one chart
            charts_html = ChartsHTMLCreator._create_entity_html(specs)
        charts_html = charts_html.removesuffix('\n\t\t')  # Delete the last tabulation
        return charts_html
