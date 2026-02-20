"""AframeXR entities HTML creator"""

import io
import json
import os
import polars as pl
import urllib.error, urllib.request
import warnings

from functools import lru_cache
from polars import DataFrame

from .axis_creator import AxisCreator
from .chart_creator import ChartCreator
from .element_creator import ElementCreator


@lru_cache  # Use come cache for increasing performance
def _get_data_from_url(url: str) -> DataFrame:
    """Loads the data from the URL (could be a local path) and returns it as a DataFrame."""
    if url.startswith(('http://', 'https://')):  # Data is stored in a URL
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                file_type = response.info().get_content_type()
                data = io.BytesIO(response.read())  # For polars
        except urllib.error.URLError:
            raise IOError(f'Could not load data from URL: {url}.')
    else:  # Data is stored in a local file
        path = os.path.normpath(url)
        if not os.path.exists(path):
            raise FileNotFoundError(f'Local file "{path}" was not found.')

        data = open(path, 'rb')
        _, file_type = os.path.splitext(path)
        file_type = file_type.lower()

    try:
        if 'csv' in file_type:  # Data is in CSV format
            df_data = pl.read_csv(data)
        elif 'json' in file_type:
            json_data = json.load(data)
            df_data = DataFrame(json_data)
        else:
            raise ValueError(f'Unsupported file type: {file_type}.')

        return df_data
    except ValueError:
        raise  # To raise previous ValueError
    except Exception as e:
        raise IOError(f'Error when processing data. Error: {e}.')

    finally:
        if data and not url.startswith(('http', 'https')):
            data.close()  # Close the file


def _get_raw_data_and_params(chart_specs: dict) -> tuple[DataFrame, set]:
    """
    Returns a tuple containing the raw data from the chart specifications (transformed if necessary),
    and a set containing the names for the params of the chart.
    """
    # Get the raw data of the chart
    data_field = chart_specs['data']
    if data_field.get('url'):  # Data is stored in a file
        raw_data = _get_data_from_url(data_field['url'])
    elif data_field.get('values'):  # Data is stored as the raw data
        json_data = data_field['values']
        raw_data = DataFrame(json_data)
    else:  # pragma: no cover (should never enter here, as chart_specs should have previously been validated)
        raise RuntimeError('Unreachable code: chart_specs should have been validated earlier')

    # Transform data (if necessary)
    from ..api.aggregate import AggregatedFieldDef  # To avoid circular import error
    from ..api.filters import FilterTransform

    transform_field = chart_specs.get('transform')
    params_names = set()
    if transform_field:

        for filter_transformation in transform_field:  # The first transformations are the filters
            if filter_transformation.get('filter'):
                filter_specs = filter_transformation['filter']
                if 'param' in filter_specs:
                    params_names.add(filter_specs['param'])
                else:  # Exclude params from filters
                    if isinstance(filter_specs, str):
                        filter_object = FilterTransform.from_equation(filter_specs)
                    elif isinstance(filter_specs, dict):
                        filter_object = FilterTransform.from_dict(filter_transformation['filter'])
                    else:  # pragma: no cover (should never enter here, as filter specs should have been validated)
                        raise RuntimeError('Unreachable code. Filter specifications should have been validated earlier')

                    raw_data = filter_object.get_filtered_data(raw_data)
                    if raw_data.is_empty():  # Data does not contain any value for the filter
                        warnings.warn(f'Data does not contain values for the filter: {filter_transformation["filter"]}')

        for non_filter_transf in transform_field:  # Non-filter transformations
            groupby = set(non_filter_transf.get('groupby')) if non_filter_transf.get('groupby') else set()
            if non_filter_transf.get('aggregate'):
                for aggregate in non_filter_transf.get('aggregate'):
                    aggregate_object = AggregatedFieldDef.from_dict(aggregate)

                    encoding_channels = {  # Using a set to have the possibility of getting differences
                        ch_spec['field'] for ch_spec in chart_specs['encoding'].values()  # Take the encoding channels
                        if ch_spec['field'] != aggregate_object.as_field  # Except the aggregate field channel
                    }

                    if groupby:
                        not_defined_channels = encoding_channels - set(groupby)  # Difference between sets
                        if not_defined_channels:  # There are channels in encoding_channels not defined in groupby
                            raise ValueError(
                                f'Encoding channel(s) "{not_defined_channels}" must be defined in aggregate groupby: '
                                f'{groupby}, otherwise that fields will disappear.'
                            )
                    else:
                        groupby = encoding_channels  # Use the encoding channels as groupby
                    raw_data = aggregate_object.get_aggregated_data(raw_data, list(groupby))

    # Aggregate in encoding
    encoding_channels_values = list(chart_specs['encoding'].values())
    groupby_fields = [ch['field'] for ch in encoding_channels_values if not ch.get('aggregate')]

    for ch in encoding_channels_values:
        aggregate_op = ch.get('aggregate')
        if aggregate_op is not None:
            aggregate_object = AggregatedFieldDef(aggregate_op, ch['field'])
            raw_data = aggregate_object.get_aggregated_data(raw_data, groupby_fields)

    return raw_data, params_names


def _get_param_combinations(data: DataFrame, param_specs: dict | None) -> list[dict]:
    """Returns a list containing the combinations in data for param specifications."""
    combinations = []

    if param_specs is None:
        return combinations

    select_type = param_specs['select']['type']
    if select_type == 'point':
        combinations = data.select(param_specs['select']['fields']).unique().to_dicts()

    return combinations


class ChartsHTMLCreator:
    """Charts HTML creator class."""

    @staticmethod
    def _create_chart_html(chart_specs: dict, param_name: str = None, param_values: dict = None) -> str:
        chart_type = chart_specs['mark']['type'] if isinstance(chart_specs['mark'], dict) else chart_specs['mark']

        # Chart HTML
        chart_object = ChartCreator.create_object(chart_type, chart_specs)  # Create the chart object
        group_specs = chart_object.get_group_specs()  # Get the base specifications of the group of elements

        filtered_by_params = False
        attributes = ''.join(f' {key.replace("_", "-")}="{value}"' for key, value in group_specs.items())
        if param_name is not None and param_values is not None:
            filtered_by_params = True
            param_values_str = '__'.join(f'{value}' for value in param_values.values())
            attributes += f' param-name="{param_name}__{param_values_str}" visible="false"'
        chart_html = ('<a-entity{attributes}>'.format(attributes=attributes) +
                      "  <!-- Chart's box (modify this values if you want to change position or rotation) -->\n")

        chart_html += f'\t\t\t<a-entity position="{chart_object.get_relative_bottom_left_corner_position()}">\n'
        elements = chart_object.get_elements(filtered_by_params=filtered_by_params)  # Specifications for each element
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
    def _create_entity_html(chart_specs: dict, scene_params_map: dict) -> str:
        """
        Returns the HTML of the elements that compose the entity.

        Parameters
        ----------
        chart_specs : dict
            Chart specifications.
        scene_params_map : dict
            Parameters of the scene.

        Notes
        -----
        Supposing that chart_specs is a dictionary (at this method has been called from self.create_charts_html).

        Suppose that the parameters are correct for method calls of ChartCreator and AxisCreator.
        """
        if 'mark' in chart_specs:  # Chart
            raw_data, chart_params_names = _get_raw_data_and_params(chart_specs)

            if chart_params_names:  # Chart is filtered using params
                html = ''
                for param_name in chart_params_names:
                    param_specs = scene_params_map.get(param_name)

                    if param_specs is None:
                        warnings.warn(
                            f'Parameter {param_name} not found in scene\'s specifications, charts transformed by '
                            f'that param will not be displayed. Make sure the name is correct'
                        )

                    # Create one chart per combination
                    charts_html = []
                    param_combinations = _get_param_combinations(raw_data, param_specs)
                    if not param_combinations:
                        chart_specs['data'] = {'values': raw_data.to_dicts()}
                        charts_html.append(ChartsHTMLCreator._create_chart_html(chart_specs))
                    else:
                        for combination in param_combinations:
                            new_data = raw_data
                            for key, value in combination.items():
                                new_data = new_data.filter(pl.col(key) == value)

                            charts_html.append(
                                ChartsHTMLCreator._create_chart_html(
                                    {**chart_specs, 'data': {'values': new_data.to_dicts()}},
                                    param_name=param_name, param_values=combination
                                )
                            )

                    html = '\n\t\t'.join(charts_html)

            else:
                chart_specs['data'] = {'values': raw_data.to_dicts()}
                html = ChartsHTMLCreator._create_chart_html(chart_specs)

        elif 'element' in chart_specs:  # Single element
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
        scene_params = list(specs.get('params', []))
        for chart in specs.get('concat', []):
            scene_params.extend(chart.get('params', []))
        scene_params_map = {p['name']: p for p in scene_params}

        charts_list = specs.get('concat')
        if charts_list:
            return '\n\t\t'.join(
                ChartsHTMLCreator._create_entity_html(chart, scene_params_map) for chart in charts_list
            )

        return ChartsHTMLCreator._create_entity_html(specs, scene_params_map)

