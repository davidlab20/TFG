import aframexr
import math
import unittest

from bs4 import BeautifulSoup

from aframexr.api.filters import FilterTransform
from aframexr.utils.constants import DEFAULT_CHART_HEIGHT, ERROR_MESSAGES, PRECISION_DECIMALS
from tests.constants import *  # Constants used for testing


def _bars_bases_are_on_x_axis(bars_chart: aframexr.Chart) -> bool:
    """Verify that the bars are well-placed in the x-axis (the base of the bar is in the x-axis)."""
    soup = BeautifulSoup(bars_chart.to_html(), 'lxml')
    x_axis_y_pos = float(soup.select('a-entity[line]')[2]['line'].split(';')[0].split()[2])  # Y position of x-axis line

    bars = soup.find_all('a-box')
    for b in bars:
        bar_height = float(b['height'])  # Total height of the bar
        y_axis_midpoint = float(b['position'].split()[1])  # Y-axis coordinate

        y_id = float(b['info'].split(' : ')[1])
        if y_id >= 0:  # Bar represents positive value (above x-axis)
            if not math.isclose(x_axis_y_pos, y_axis_midpoint - 0.5 * bar_height, abs_tol=10 ** -PRECISION_DECIMALS):
                print(f'\nDEBUG: Positive bar\'s base is not on x-axis line.'
                      f'\n\t- X-axis line Y-coordinate: {x_axis_y_pos}'
                      f'\n\t- Y-axis bar coordinate: {y_axis_midpoint}'
                      f'\n\t- Bar\'s height: {bar_height}')
                return False  # Y-pos minus half its height must be the same as the x-axis y-coordinate
        else:  # Bar represents negative value (below x-axis)
            if not math.isclose(x_axis_y_pos, y_axis_midpoint + 0.5 * bar_height, abs_tol=10 ** -PRECISION_DECIMALS):
                print(f'\nDEBUG: Negative bar\'s base is not on x-axis line.'
                      f'\n\t- X-axis line Y-coordinate: {x_axis_y_pos}'
                      f'\n\t- Y-axis bar coordinate: {y_axis_midpoint}'
                      f'\n\t- Bar\'s height: {bar_height}')
                return False  # Y-pos plus half its height must be the same as the x-axis y-coordinate
    return True

def _bars_height_does_not_exceed_max_height(bars_chart: aframexr.Chart) -> bool:
    """Verify that every bar height does not exceed the maximum height."""
    max_height = float(bars_chart.to_dict().get('height', DEFAULT_CHART_HEIGHT))

    soup = BeautifulSoup(bars_chart.to_html(), 'lxml')
    bars = soup.find_all('a-box')
    for b in bars:
        bar_height = float(b['height'])  # Total height of the bar
        if bar_height > max_height:
            print(f'\nDEBUG: Bar\'s height exceed chart\'s height.'
                  f'\n\t- Bar\'s height: {bar_height}'
                  f'\n\t- Chart height: {max_height}')
            return False
    return True


class TestMarkBarOK(unittest.TestCase):
    """Bars chart OK tests."""
    def test_simple(self):
        """Simple bars chart creation."""
        bars_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales')
        bars_chart.to_html()
        self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
        self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_simple_with_pandas_not_installed(self):
        """Simple bars chart creation without having pandas installed."""
        import sys
        import importlib
        from unittest import mock

        sys.modules.pop('aframexr', None)
        sys.modules.pop('aframexr.api.components', None)

        with mock.patch.dict(sys.modules, {'pandas': None}):
            import aframexr
            importlib.reload(aframexr)

            bars_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

            import aframexr.api.components as components
            self.assertIsNone(components.pd)
            self.assertIs(components.DataFrame, object)

    def test_from_json(self):
        """Bars chart using from_json() method creation."""
        json_string = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales').to_json()
        bars_chart = aframexr.Chart.from_json(json_string)
        bars_chart.to_html()
        # noinspection PyTypeChecker
        self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
        # noinspection PyTypeChecker
        self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))
        self.assertEqual(bars_chart.to_json(), json_string)

    def test_data_format(self):
        """Bars chart changing data format creation."""
        for d in DATA_FORMATS:
            bars_chart = aframexr.Chart(d).mark_bar().encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_position(self):
        """Bars chart changing position creation."""
        for p in POSITIONS:
            bars_chart = aframexr.Chart(DATA, position=p).mark_bar().encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_position_format(self):
        """Bars chart changing position format creation."""
        for p in POSITION_FORMATS:
            bars_chart = aframexr.Chart(DATA, position=p).mark_bar().encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_rotation(self):
        """Bars chart changing rotation creation."""
        for r in ROTATIONS:
            bars_chart = aframexr.Chart(DATA, rotation=r).mark_bar().encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_rotation_format(self):
        """Bars chart changing rotation format creation."""
        for r in ROTATION_FORMATS:
            bars_chart = aframexr.Chart(DATA, rotation=r).mark_bar().encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_depth(self):
        """Bars chart changing depth creation."""
        for d in ALL_MARK_DEPTHS_HEIGHTS_WIDTHS:
            bars_chart = aframexr.Chart(DATA, depth=d).mark_bar().encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_height(self):
        """Bars chart changing height creation."""
        for h in MARK_BAR_POINT_HEIGHTS_WIDTHS:
            bars_chart = aframexr.Chart(DATA, height=h).mark_bar().encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_width(self):
        """Bars chart changing width creation."""
        for w in MARK_BAR_POINT_HEIGHTS_WIDTHS:
            bars_chart = aframexr.Chart(DATA, width=w).mark_bar().encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_size(self):
        """Bars chart changing size creation."""
        for s in MARK_BAR_POINT_SIZES:
            bars_chart = aframexr.Chart(DATA).mark_bar(size=s).encode(x='model', y='sales')
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_encoding(self):
        """Bars chart changing encoding creation."""
        for e in MARK_BAR_ENCODINGS:
            bars_chart = aframexr.Chart(DATA).mark_bar().encode(**e)
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_encoding_with_no_Y_axis_displayed(self):
        """Bars chart creation with no Y-axis displayed."""
        bars_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y=aframexr.Y('sales', axis=None))
        bars_chart.to_html()
        self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
        self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_filter(self):
        """Bars chart changing filter creation."""
        for eq in FILTER_EQUATIONS:
            for f in [eq, FilterTransform.from_equation(eq)]:  # Filter using equation and using FilterTransform object
                bars_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales').transform_filter(f)
                bars_chart.to_html()
                self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
                self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_several_filters(self):
        """Bars chart with several filters' creation."""
        bars_chart = (aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales')
                      .transform_filter(SEVERAL_FILTER_EQUATIONS[0]))
        for eq in SEVERAL_FILTER_EQUATIONS[1:]:
            bars_chart.transform_filter(eq).to_html()

        self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
        self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_aggregate(self):
        """Bar chart changing aggregates creation."""
        for a in AGGREGATES:
            bars_chart = (aframexr.Chart(DATA).mark_bar().encode(x='model', y='new_field')
                         .transform_aggregate(new_field=f'{a}(sales)'))
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

            bars_chart_2 = aframexr.Chart(DATA).mark_bar().encode(x='model', y=f'{a}(sales)')
            bars_chart_2.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart_2))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart_2))

    def test_aggregate_position_rotation_size_height_width_filter(self):
        """Bars chart changing position, rotation size, height, width and filter creation."""
        for a, p, r, s, h, w, f in zip(AGGREGATES, POSITIONS, ROTATIONS, MARK_BAR_POINT_SIZES,
                                          MARK_BAR_POINT_HEIGHTS_WIDTHS, MARK_BAR_POINT_HEIGHTS_WIDTHS,
                                          FILTER_EQUATIONS):
            bars_chart = (aframexr.Chart(DATA, position=p, rotation=r, height=h, width=w).mark_bar(size=s)
                          .encode(x='model', y='agg').transform_filter(f).transform_aggregate(agg=f'{a}(sales)'))
            bars_chart.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart))

    def test_concatenation(self):
        """Bars chart concatenation creation."""
        concatenated_chart = (aframexr.Chart(DATA, position=CONCATENATION_POSITIONS[0]).mark_bar()
                              .encode(x='model', y='sales'))
        for pos in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Chart(DATA, position=pos).mark_bar().encode(x='model', y='sales')

        concatenated_chart.to_html()
        self.assertTrue(_bars_bases_are_on_x_axis(concatenated_chart))
        self.assertTrue(_bars_height_does_not_exceed_max_height(concatenated_chart))

    def test_save(self):
        """Bars chart saving."""
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_html_file_path = Path(tmpdir) / "test.html"
            temp_json_file_path = Path(tmpdir) / "test.json"

            bars_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales')
            bars_chart.save(str(temp_html_file_path))
            bars_chart.save(str(temp_json_file_path))

            self.assertTrue(temp_html_file_path.exists())
            self.assertTrue(temp_json_file_path.exists())

    def test_properties(self):
        """Bars chart properties definition."""
        bars_chart = aframexr.Chart().mark_bar().encode(x='model', y='sales')
        for p, r in zip(POSITIONS, ROTATIONS):
            bars_chart_2 = bars_chart.properties(data=DATA, position=p, rotation=r)
            bars_chart_2.to_html()
            self.assertTrue(_bars_bases_are_on_x_axis(bars_chart_2))
            self.assertTrue(_bars_height_does_not_exceed_max_height(bars_chart_2))


class TestMarkBarError(unittest.TestCase):
    """Bars chart error tests."""
    def test_load_data_url_error(self):
        """Bars chart load data url error."""
        with self.assertRaises(IOError) as error:
            aframexr.Chart(NON_EXISTING_URL_DATA).mark_bar().encode(x='model', y='sales').to_html()

        self.assertEqual(str(error.exception), f"Could not load data from URL: {NON_EXISTING_URL_DATA.url}.")

    def test_local_file_does_not_exist(self):
        """Bars chart error when local file does not exist."""
        with self.assertRaises(IOError) as error:
            aframexr.Chart(NON_EXISTING_LOCAL_PATH).mark_bar().encode(x='model', y='sales').to_html()

        self.assertRegex(str(error.exception), r'Local file .* was not found')

    def test_bad_file_format(self):
        """Bars chart error when file format is incorrect."""
        with open(BAD_FILE_FORMAT.url, 'w'):
            pass  # Create a bad format temporal file

        try:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(BAD_FILE_FORMAT).mark_bar().encode(x='model', y='sales').to_html()

            self.assertIn(f'Unsupported file type: ', str(error.exception))

        finally:
            from pathlib import Path
            Path(BAD_FILE_FORMAT.url).unlink()  # Remove the temporal file

    def test_file_is_empty(self):
        """Bars chart error when file is empty."""
        with open(EMPTY_FILE.url, 'w'):
            pass  # Create an empty temporal file

        try:
            with self.assertRaises(IOError) as error:
                aframexr.Chart(EMPTY_FILE).mark_bar().encode(x='model', y='sales').to_html()

            self.assertIn('Error when processing data. Error: ', str(error.exception))

        finally:
            from pathlib import Path
            Path(EMPTY_FILE.url).unlink()  # Remove the temporal file

    def test_position_error(self):
        """Bars chart position error."""
        for p in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_bar().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['NOT_3_AXES_POSITION_OR_ROTATION'].format(
                pos_or_rot='position', pos_or_rot_value=p
            ))

        for p in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_bar().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), 'The position values must be numeric.')

    def test_rotation_error(self):
        """Bars chart rotation error."""
        for r in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_bar().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['NOT_3_AXES_POSITION_OR_ROTATION'].format(
                pos_or_rot='rotation', pos_or_rot_value=r
            ))

        for r in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_bar().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), 'The rotation values must be numeric.')

    def test_size_error(self):
        """Bars chart size error."""
        for s in NOT_GREATER_THAN_0_NUMBERS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_bar(size=s).encode(x='model', y='sales')
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='size'))

    def test_depth_error(self):
        """Bars chart error when depth is incorrect."""
        for d in NOT_GREATER_THAN_0_NUMBERS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, depth=d).mark_bar().encode(x='model', y='sales').to_html()
            self.assertEqual(
                str(error.exception),
                ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='depth')
            )

    def test_height_error(self):
        """Bars chart height error."""
        for h in NOT_GREATER_THAN_0_NUMBERS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, height=h).mark_bar().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='height'))

    def test_width_error(self):
        """Bars chart width error."""
        for w in NOT_GREATER_THAN_0_NUMBERS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, width=w).mark_bar().encode(x='model', y='sales').to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='width'))

    def test_encoding_error(self):
        """Bars chart encoding error."""
        for e in NON_EXISTING_MARK_BAR_POINT_ENCODINGS:
            with self.assertRaises(KeyError) as error:
                bars_chart = aframexr.Chart(DATA).mark_bar().encode(**e)
                bars_chart.to_html()
            self.assertIn('Data has no field ', str(error.exception))

        for e in NOT_VALID_MARK_BAR_POINT_ENCODINGS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_bar().encode(**e).to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['LESS_THAN_2_XYZ_ENCODING'])

    def test_encoding_error_invalid_encoding_type(self):
        """Bars chart encoding error with invalid encoding type."""
        with self.assertRaises(ValueError) as error:
            bad_encoding_type = 'BAD_ENCODING'
            aframexr.Chart(DATA).mark_bar().encode(x=f'model:{bad_encoding_type}', y='sales').to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENCODING_TYPE'].format(encoding_type=bad_encoding_type))

    def test_encoding_error_not_encoded(self):
        """Bars chart encoding error. Encoding not in specifications."""
        with self.assertRaises(ValueError) as error:
            bars_chart = aframexr.Chart(DATA).mark_bar()
            bars_chart.to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENCODING_NOT_IN_SPECS'])

    def test_filter_warning(self):
        """Bars chart filter warning."""
        for f in WARNING_FILTER_EQUATIONS:
            with self.assertWarns(UserWarning) as warning:
                filt_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales').transform_filter(f)
                filt_chart.to_html()
            self.assertEqual(
                str(warning.warning),
                f'Data does not contain values for the filter: {FilterTransform.from_equation(f).to_dict()}'
            )

    def test_filter_error(self):
        """Bars chart filter error."""
        for f in SYNTAX_ERROR_FILTER_EQUATIONS:
            with self.assertRaises(SyntaxError) as error:
                filt_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales').transform_filter(f)
                filt_chart.to_html()
            self.assertEqual(str(error.exception), 'Incorrect syntax, must be datum.{field} {operator} {value}')

    def test_aggregate_error(self):
        """Bars chart aggregate error."""
        for a in NOT_VALID_AGGREGATES:
            with self.assertRaises(ValueError) as error:
                agg_chart = (aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales')
                             .transform_aggregate(new_field=f'{a}(sales)'))
                agg_chart.to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['AGGREGATE_OPERATION'].format(operation=a))

    def test_aggregate_error_not_defined_encoding_channels(self):
        """Bars chart aggregate error raised when encoding channels are not defined in aggregation."""
        with self.assertRaises(ValueError) as error:
            agg_chart = (aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales')
                         .transform_aggregate(mean_sales='mean(sales)', groupby=['model']))
            agg_chart.to_html()

        self.assertRegex(str(error.exception), r'Encoding channel\(s\) .* must be defined in aggregate .*'
                                               r', otherwise that fields will disappear.')