import aframexr
import unittest

from aframexr.api.filters import FilterTransform
from aframexr.utils.constants import AVAILABLE_ENVIRONMENTS, ERROR_MESSAGES
from tests.constants import *  # Constants used for testing


class TestMarkLineOK(unittest.TestCase):
    """Line chart OK tests."""
    def test_simple(self):
        """Simple line chart creation."""
        line_chart = aframexr.Chart(DATA).mark_line().encode(x='model', y='sales')
        line_chart.to_html()

    def test_simple_with_pandas_not_installed(self):
        """Simple line chart creation without having pandas installed."""
        import sys
        import importlib
        from unittest import mock

        sys.modules.pop('aframexr', None)
        sys.modules.pop('aframexr.api.components', None)

        with mock.patch.dict(sys.modules, {'pandas': None}):
            import aframexr
            importlib.reload(aframexr)

            line_chart = aframexr.Chart(DATA).mark_line().encode(x='model', y='sales')
            line_chart.to_html()

            import aframexr.api.components as components
            self.assertIsNone(components.pd)
            self.assertIs(components.DataFrame, object)

    def test_from_json(self):
        """Line chart using from_json() method creation."""
        json_string = aframexr.Chart(DATA).mark_line().encode(x='model', y='sales').to_json()
        line_chart = aframexr.Chart.from_json(json_string)
        line_chart.to_html()

        self.assertEqual(line_chart.to_json(), json_string)

    def test_data_format(self):
        """Line chart changing data format creation."""
        for d in DATA_FORMATS:
            line_chart = aframexr.Chart(d).mark_line().encode(x='model', y='sales')
            line_chart.to_html()

    def test_position(self):
        """Line chart changing position creation."""
        for p in POSITIONS:
            line_chart = aframexr.Chart(DATA, position=p).mark_line().encode(x='model', y='sales')
            line_chart.to_html()

    def test_position_format(self):
        """Line chart changing position format creation."""
        for p in POSITION_FORMATS:
            line_chart = aframexr.Chart(DATA, position=p).mark_line().encode(x='model', y='sales')
            line_chart.to_html()

    def test_rotation(self):
        """Line chart changing rotation creation."""
        for r in ROTATIONS:
            line_chart = aframexr.Chart(DATA, rotation=r).mark_line().encode(x='model', y='sales')
            line_chart.to_html()

    def test_rotation_format(self):
        """Line chart changing rotation format creation."""
        for r in ROTATION_FORMATS:
            line_chart = aframexr.Chart(DATA, rotation=r).mark_line().encode(x='model', y='sales')
            line_chart.to_html()

    def test_height(self):
        """Line chart changing height creation."""
        for h in MARK_BAR_POINT_HEIGHTS_WIDTHS:
            line_chart = aframexr.Chart(DATA, height=h).mark_line().encode(x='model', y='sales')
            line_chart.to_html()

    def test_width(self):
        """Line chart changing width creation."""
        for w in MARK_BAR_POINT_HEIGHTS_WIDTHS:
            line_chart = aframexr.Chart(DATA, width=w).mark_line().encode(x='model', y='sales')
            line_chart.to_html()

    def test_point_markers(self):
        """Line chart using point markers creation."""
        line_chart = aframexr.Chart(DATA).mark_line(point=True).encode(x='model', y='sales')
        line_chart.to_html()

    def test_encoding(self):
        """Line chart changing encoding creation."""
        for e in MARK_BAR_ENCODINGS:
            line_chart = aframexr.Chart(DATA).mark_line().encode(**e)
            line_chart.to_html()

    def test_encoding_with_no_Y_axis_displayed(self):
        """Line chart creation with no Y-axis displayed."""
        line_chart = aframexr.Chart(DATA).mark_line().encode(x='model', y=aframexr.Y('sales', axis=None))
        line_chart.to_html()

    def test_filter(self):
        """Line chart changing filter creation."""
        for eq in FILTER_EQUATIONS:
            for f in [eq, FilterTransform.from_equation(eq)]:  # Filter using equation and using FilterTransform object
                line_chart = aframexr.Chart(DATA).mark_line().encode(x='model', y='sales').transform_filter(f)
                line_chart.to_html()

    def test_several_filters(self):
        """Line chart with several filters' creation."""
        line_chart = (aframexr.Chart(DATA).mark_line().encode(x='model', y='sales')
                      .transform_filter(SEVERAL_FILTER_EQUATIONS[0]))
        for eq in SEVERAL_FILTER_EQUATIONS[1:]:
            line_chart.transform_filter(eq)

        line_chart.to_html()

    def test_aggregate(self):
        """Line chart changing aggregates creation."""
        for a in AGGREGATES:
            line_chart = (aframexr.Chart(DATA).mark_line().encode(x='model', y='new_field')
                          .transform_aggregate(new_field=f'{a}(sales)'))
            line_chart.to_html()

            line_chart_2 = aframexr.Chart(DATA).mark_line().encode(x='model', y=f'{a}(sales)')
            line_chart_2.to_html()

    def test_aggregate_position_rotation_size_height_width_filter(self):
        """Line chart changing position, rotation size, height, width and filter creation."""
        for a, p, r, po, h, w, f in zip(AGGREGATES, POSITIONS, ROTATIONS, (True, False),
                                       MARK_BAR_POINT_HEIGHTS_WIDTHS, MARK_BAR_POINT_HEIGHTS_WIDTHS,
                                       FILTER_EQUATIONS):
            line_chart = (aframexr.Chart(DATA, position=p, rotation=r, height=h, width=w).mark_line(point=po)
                          .encode(x='model', y='agg').transform_filter(f).transform_aggregate(agg=f'{a}(sales)'))
            line_chart.to_html()

    def test_concatenation(self):
        """Line chart concatenation creation."""
        concatenated_chart = (aframexr.Chart(DATA, position=CONCATENATION_POSITIONS[0]).mark_line()
                              .encode(x='model', y='sales'))
        for pos in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Chart(DATA, position=pos).mark_line().encode(x='model', y='sales')

        concatenated_chart.to_html()

    def test_environment(self):
        """Scene creation with personalized environment."""
        for e in AVAILABLE_ENVIRONMENTS:
            line_chart = aframexr.Chart(DATA).mark_line().encode(x='model', y='sales')
            line_chart.to_html(environment=e)

    def test_save(self):
        """Line chart saving."""
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_html_file_path = Path(tmpdir) / "test.html"
            temp_json_file_path = Path(tmpdir) / "test.json"

            line_chart = aframexr.Chart(DATA).mark_line().encode(x='model', y='sales')
            line_chart.save(str(temp_html_file_path))
            line_chart.save(str(temp_json_file_path))

            self.assertTrue(temp_html_file_path.exists())
            self.assertTrue(temp_json_file_path.exists())

    def test_properties(self):
        """Line chart properties definition."""
        line_chart = aframexr.Chart().mark_line().encode(x='model', y='sales')
        for p, r in zip(POSITIONS, ROTATIONS):
            line_chart_2 = line_chart.properties(data=DATA, position=p, rotation=r)
            line_chart_2.to_html()


class TestMarkLineError(unittest.TestCase):
    """Line chart error tests."""

    def test_load_data_url_error(self):
        """Line chart load data url error."""
        with self.assertRaises(IOError) as error:
            aframexr.Chart(NON_EXISTING_URL_DATA).mark_line().encode(x='model', y='sales').to_html()

        self.assertEqual(str(error.exception), f"Could not load data from URL: {NON_EXISTING_URL_DATA.url}.")

    def test_local_file_does_not_exist(self):
        """Line chart error when local file does not exist."""
        with self.assertRaises(IOError) as error:
            aframexr.Chart(NON_EXISTING_LOCAL_PATH).mark_line().encode(x='model', y='sales').to_html()

        self.assertRegex(str(error.exception), r'Local file .* was not found')

    def test_bad_file_format(self):
        """Line chart error when file format is incorrect."""
        with open(BAD_FILE_FORMAT.url, 'w'):
            pass  # Create a bad format temporal file

        try:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(BAD_FILE_FORMAT).mark_line().encode(x='model', y='sales').to_html()

            self.assertIn(f'Unsupported file type: ', str(error.exception))

        finally:
            from pathlib import Path
            Path(BAD_FILE_FORMAT.url).unlink()  # Remove the temporal file

    def test_file_is_empty(self):
        """Line chart error when file is empty."""
        with open(EMPTY_FILE.url, 'w'):
            pass  # Create an empty temporal file

        try:
            with self.assertRaises(IOError) as error:
                aframexr.Chart(EMPTY_FILE).mark_line().encode(x='model', y='sales').to_html()

            self.assertIn('Error when processing data. Error: ', str(error.exception))

        finally:
            from pathlib import Path
            Path(EMPTY_FILE.url).unlink()  # Remove the temporal file

    def test_position_error(self):
        """Line chart position error."""
        for p in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_line().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['NOT_3_AXES_POSITION_OR_ROTATION'].format(
                pos_or_rot='position', pos_or_rot_value=p
            ))

        for p in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_line().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), 'The position values must be numeric.')

    def test_rotation_error(self):
        """Line chart rotation error."""
        for r in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_line().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['NOT_3_AXES_POSITION_OR_ROTATION'].format(
                pos_or_rot='rotation', pos_or_rot_value=r
            ))

        for r in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_line().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), 'The rotation values must be numeric.')

    def test_height_error(self):
        """Line chart height error."""
        for h in NOT_GREATER_THAN_0_NUMBERS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, height=h).mark_line().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='height'))

    def test_width_error(self):
        """Line chart width error."""
        for w in NOT_GREATER_THAN_0_NUMBERS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, width=w).mark_line().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='width'))

    def test_encoding_error(self):
        """Line chart encoding error."""
        for e in NON_EXISTING_MARK_BAR_POINT_ENCODINGS:
            with self.assertRaises(KeyError) as error:
                aframexr.Chart(DATA).mark_line().encode(**e).to_html()
            self.assertIn('Data has no field ', str(error.exception))

    def test_encoding_error_invalid_encoding_type(self):
        """Line chart encoding error with invalid encoding type."""
        with self.assertRaises(ValueError) as error:
            bad_encoding_type = 'BAD_ENCODING'
            aframexr.Chart(DATA).mark_line().encode(x=f'model:{bad_encoding_type}', y='sales').to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENCODING_TYPE'].format(encoding_type=bad_encoding_type))

    def test_encoding_error_not_encoded(self):
        """Line chart encoding error. Encoding not in specifications."""
        with self.assertRaises(ValueError) as error:
            aframexr.Chart(DATA).mark_line().to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENCODING_NOT_IN_SPECS'])

    def test_filter_warning(self):
        """Line chart filter warning."""
        for f in WARNING_FILTER_EQUATIONS:
            with self.assertWarns(UserWarning) as warning:
                aframexr.Chart(DATA).mark_line().encode(x='model', y='sales').transform_filter(f).to_html()
            self.assertEqual(
                str(warning.warning),
                f'Data does not contain values for the filter: {FilterTransform.from_equation(f).to_dict()}'
            )

    def test_filter_error(self):
        """Line chart filter error."""
        for f in SYNTAX_ERROR_FILTER_EQUATIONS:
            with self.assertRaises(SyntaxError) as error:
                aframexr.Chart(DATA).mark_line().encode(x='model', y='sales').transform_filter(f).to_html()
            self.assertEqual(str(error.exception), 'Incorrect syntax, must be datum.{field} {operator} {value}')

    def test_aggregate_error(self):
        """Line chart aggregate error."""
        for a in NOT_VALID_AGGREGATES:
            with self.assertRaises(ValueError) as error:
                (aframexr.Chart(DATA).mark_line().encode(x='model', y='sales')
                 .transform_aggregate(new_field=f'{a}(sales)').to_html())
            self.assertEqual(str(error.exception), ERROR_MESSAGES['AGGREGATE_OPERATION'].format(operation=a))

    def test_aggregate_error_not_defined_encoding_channels(self):
        """Line chart aggregate error raised when encoding channels are not defined in aggregation."""
        with self.assertRaises(ValueError) as error:
            (aframexr.Chart(DATA).mark_line().encode(x='model', y='sales')
             .transform_aggregate(mean_sales='mean(sales)', groupby=['model'])).to_html()

        self.assertRegex(str(error.exception), r'Encoding channel\(s\) .* must be defined in aggregate .*'
                                               r', otherwise that fields will disappear.')

    def test_environment_error(self):
        """Scene creation with invalid personalized environment."""
        environment = 'bad_environment'
        line_chart = aframexr.Chart(DATA).mark_line().encode(x='model', y='sales')
        with self.assertRaises(ValueError) as error:
            # noinspection PyTypeChecker
            line_chart.to_html(environment=environment)
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENVIRONMENT'].format(environment=environment))
