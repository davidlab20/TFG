import aframexr
import math
import unittest

from bs4 import BeautifulSoup

from aframexr import ERROR_MESSAGES
from aframexr.api.filters import FilterTransform
from tests.constants import *  # Constants used for testing


def _all_theta_sum_is_360_degrees(pie_chart: aframexr.Chart) -> bool:
    """Verify that the sum for the theta length of every slice is 360 degrees."""
    total_theta_length = 0

    soup = BeautifulSoup(pie_chart.to_html(), 'lxml')
    slices = soup.find_all('a-cylinder')
    for s in slices:
        total_theta_length += float(s['theta-length'])
    if not math.isclose(total_theta_length, 360):
        print(f'\nDEBUG: total theta length must be 360 degrees.\n\t- Total theta length: {total_theta_length}.')
        return False
    return True

def _slices_are_well_placed(pie_chart: aframexr.Chart) -> bool:
    """Verify that the slices are well-placed in the pie chart (relative position has to be the same for all)."""
    soup = BeautifulSoup(pie_chart.to_html(), 'lxml')
    slices = soup.find_all('a-cylinder')
    for s in slices:
        if s['position'] != '0 0 0':
            print(f'\nDEBUG: one slice does not have position "0 0 0".\n\t- Position: {s['position']}.')
            return False
    return True


class TestMarkArcOK(unittest.TestCase):
    """Pie chart OK tests."""
    def test_simple(self):
        """Simple pie chart creation."""
        pie_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales')
        pie_chart.to_html()
        self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
        self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_simple_with_pandas_not_installed(self):
        """Simple pie chart creation without having pandas installed."""
        import sys
        import importlib
        from unittest import mock

        sys.modules.pop('aframexr', None)
        sys.modules.pop('aframexr.api.components', None)

        with mock.patch.dict(sys.modules, {'pandas': None}):
            import aframexr
            importlib.reload(aframexr)

            pie_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales')
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

            import aframexr.api.components as components
            self.assertIsNone(components.pd)
            self.assertIs(components.DataFrame, object)

    def test_from_json(self):
        """Pie chart using from_json() method creation."""
        json_string = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales').to_json()
        pie_chart = aframexr.Chart.from_json(json_string)
        pie_chart.to_html()
        # noinspection PyTypeChecker
        self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
        # noinspection PyTypeChecker
        self.assertTrue(_slices_are_well_placed(pie_chart))
        self.assertEqual(pie_chart.to_json(), json_string)

    def test_data_format(self):
        """Pie chart changing data format creation."""
        for d in DATA_FORMATS:
            pie_chart = aframexr.Chart(d).mark_arc().encode(color='model', theta='sales')
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_depth(self):
        """Pie chart changing depth creation."""
        for d in ALL_MARK_DEPTHS_HEIGHTS_WIDTHS:
            pie_chart = aframexr.Chart(DATA, depth=d).mark_arc().encode(color='model', theta='sales')
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_position(self):
        """Pie chart changing position creation."""
        for p in POSITIONS:
            pie_chart = aframexr.Chart(DATA, position=p).mark_arc().encode(color='model', theta='sales')
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_position_format(self):
        """Pie chart changing position format creation."""
        for p in POSITION_FORMATS:
            pie_chart = aframexr.Chart(DATA, position=p).mark_arc().encode(color='model', theta='sales')
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_rotation(self):
        """Pie chart changing rotation creation."""
        for r in ROTATIONS:
            pie_chart = aframexr.Chart(DATA, rotation=r).mark_arc().encode(color='model', theta='sales')
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_rotation_format(self):
        """Pie chart changing rotation format creation."""
        for r in ROTATION_FORMATS:
            pie_chart = aframexr.Chart(DATA, rotation=r).mark_arc().encode(color='model', theta='sales')
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_radius(self):
        """Pie chart changing radius creation."""
        for r in MARK_ARC_RADIUS:
            pie_chart = aframexr.Chart(DATA).mark_arc(radius=r).encode(color='model', theta='sales')
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_filter(self):
        """Pie chart changing filter creation."""
        for eq in FILTER_EQUATIONS:
            for f in [eq, FilterTransform.from_string(eq)]:  # Filter using equation and using FilterTransform object
                pie_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales').transform_filter(f)
                pie_chart.to_html()
                self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
                self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_several_filters(self):
        """Pie chart with several filters' creation."""
        pie_chart = (aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales')
                     .transform_filter(SEVERAL_FILTER_EQUATIONS[0]))
        for eq in SEVERAL_FILTER_EQUATIONS[1:]:
            pie_chart.transform_filter(eq).to_html()

        self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
        self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_aggregate(self):
        """Pie chart changing aggregates creation."""
        for a in AGGREGATES:
            pie_chart = (aframexr.Chart(DATA).mark_arc().encode(color='model', theta='new_field')
                         .transform_aggregate(new_field=f'{a}(sales)'))
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

            pie_chart_2 = aframexr.Chart(DATA).mark_arc().encode(color='model', theta=f'{a}(sales)')
            pie_chart_2.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart_2))
            self.assertTrue(_slices_are_well_placed(pie_chart_2))

    def test_aggregate_position_rotation_radius_filter(self):
        """Pie chart changing position, rotation, radius and filter creation."""
        for agg, pos, rot, rad, fil in zip(AGGREGATES, POSITIONS, ROTATIONS, MARK_ARC_RADIUS, FILTER_EQUATIONS):
            pie_chart = (aframexr.Chart(DATA, position=pos, rotation=rot).mark_arc(radius=rad)
                         .encode(color='model',theta='agg').transform_filter(fil)
                         .transform_aggregate(agg=f'{agg}(sales)'))
            pie_chart.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart))
            self.assertTrue(_slices_are_well_placed(pie_chart))

    def test_concatenation(self):
        """Pie chart concatenation creation."""
        concatenated_chart = (aframexr.Chart(DATA, position=CONCATENATION_POSITIONS[0]).mark_arc()
                              .encode(color='model', theta='sales'))
        for pos in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Chart(DATA, position=pos).mark_arc().encode(color='model', theta='sales')

        concatenated_chart.to_html()
        self.assertTrue(_slices_are_well_placed(concatenated_chart))

    def test_save(self):
        """Pie chart saving."""
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_html_file_path = Path(tmpdir) / "test.html"
            temp_json_file_path = Path(tmpdir) / "test.json"

            pie_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales')
            pie_chart.save(str(temp_html_file_path))
            pie_chart.save(str(temp_json_file_path))

            self.assertTrue(temp_html_file_path.exists())
            self.assertTrue(temp_json_file_path.exists())

    def test_properties(self):
        """Pie chart properties definition."""
        pie_chart = aframexr.Chart().mark_arc().encode(color='model', theta='sales')
        for p, r in zip(POSITIONS, ROTATIONS):
            pie_chart_2 = pie_chart.properties(data=DATA, position=p, rotation=r)
            pie_chart_2.to_html()
            self.assertTrue(_all_theta_sum_is_360_degrees(pie_chart_2))
            self.assertTrue(_slices_are_well_placed(pie_chart_2))


class TestMarkArcError(unittest.TestCase):
    """Pie chart error tests."""
    def test_load_data_url_error(self):
        """Pie chart load data url error."""
        with self.assertRaises(IOError) as error:
            aframexr.Chart(NON_EXISTING_URL_DATA).mark_arc().encode(color='model', theta='sales').to_html()

        self.assertEqual(str(error.exception), f"Could not load data from URL: {NON_EXISTING_URL_DATA.url}.")

    def test_local_file_does_not_exist(self):
        """Pie chart error when local file does not exist."""
        with self.assertRaises(IOError) as error:
            aframexr.Chart(NON_EXISTING_LOCAL_PATH).mark_arc().encode(color='model', theta='sales').to_html()

        self.assertRegex(str(error.exception), r'Local file .* was not found')

    def test_bad_file_format(self):
        """Pie chart error when file format is incorrect."""
        with open(BAD_FILE_FORMAT.url, 'w'):
            pass  # Create a bad format temporal file

        try:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(BAD_FILE_FORMAT).mark_arc().encode(color='model', theta='sales').to_html()

            self.assertIn('Unsupported file type: ', str(error.exception))

        finally:
            from pathlib import Path
            Path(BAD_FILE_FORMAT.url).unlink()  # Remove the temporal file

    def test_file_is_empty(self):
        """Pie chart error when file is empty."""
        with open(EMPTY_FILE.url, 'w'):
            pass  # Create an empty temporal file

        try:
            with self.assertRaises(IOError) as error:
                aframexr.Chart(EMPTY_FILE).mark_arc().encode(color='model', theta='sales').to_html()

            self.assertIn('Error when processing data. Error: ', str(error.exception))

        finally:
            from pathlib import Path
            Path(EMPTY_FILE.url).unlink()  # Remove the temporal file

    def test_depth_error(self):
        """Pie chart error when depth is incorrect."""
        for d in NOT_GREATER_THAN_0_NUMBERS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, depth=d).mark_arc().encode(color='model', theta='sales').to_html()
            self.assertEqual(
                str(error.exception),
                ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='depth')
            )

    def test_position_error(self):
        """Pie chart position error."""
        for p in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_arc().encode(color='model', theta='sales').to_html()
            self.assertEqual(
                str(error.exception),
                ERROR_MESSAGES['NOT_3_AXES_POSITION_OR_ROTATION'].format(pos_or_rot='position', pos_or_rot_value=p)
            )

        for p in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_arc().encode(color='model', theta='sales').to_html()
            self.assertEqual(str(error.exception), 'The position values must be numeric.')

    def test_rotation_error(self):
        """Pie chart rotation error."""
        for r in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_arc().encode(color='model', theta='sales').to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['NOT_3_AXES_POSITION_OR_ROTATION'].format(
                pos_or_rot='rotation', pos_or_rot_value=r
            ))

        for r in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_arc().encode(color='model', theta='sales').to_html()
            self.assertEqual(str(error.exception), 'The rotation values must be numeric.')

    def test_radius_error(self):
        """Pie chart radius error."""
        for r in NOT_GREATER_THAN_0_MARK_ARC_RADIUS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_arc(radius=r).encode(color='model', theta='sales')
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='radius'))

    def test_encoding_error(self):
        """Pie chart encoding error."""
        for e in NON_EXISTING_MARK_ARC_ENCODINGS:
            with self.assertRaises(KeyError) as error:
                pie_chart = aframexr.Chart(DATA).mark_arc().encode(**e)
                pie_chart.to_html()
            self.assertIn('Data has no field ', str(error.exception))

        for e in NOT_VALID_MARK_ARC_ENCODINGS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_arc().encode(**e).to_html()
            self.assertIn(
                str(error.exception),
                [
                    ERROR_MESSAGES['PARAM_NOT_SPECIFIED_IN_MARK_ARC'].format(param='color'),
                    ERROR_MESSAGES['PARAM_NOT_SPECIFIED_IN_MARK_ARC'].format(param='theta')
                ]
            )

    def test_encoding_error_invalid_encoding_type(self):
        """Pie chart encoding error with invalid encoding type."""
        with self.assertRaises(ValueError) as error:
            bad_encoding_type = 'BAD_ENCODING'
            aframexr.Chart(DATA).mark_arc().encode(color=f'model:{bad_encoding_type}', theta='sales').to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENCODING_TYPE'].format(encoding_type=bad_encoding_type))

    def test_encoding_error_not_encoded(self):
        """Pie chart encoding error. Encoding not in specifications."""
        with self.assertRaises(ValueError) as error:
            pie_chart = aframexr.Chart(DATA).mark_arc()
            pie_chart.to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENCODING_NOT_IN_SPECS'])

    def test_filter_warning(self):
        """Pie chart filter warning."""
        for f in WARNING_FILTER_EQUATIONS:
            with self.assertWarns(UserWarning) as warning:
                filt_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales').transform_filter(f)
                filt_chart.to_html()
            self.assertEqual(str(warning.warning), f'Data does not contain values for the filter: {f}.')

    def test_filter_error(self):
        """Pie chart filter error."""
        for f in SYNTAX_ERROR_FILTER_EQUATIONS:
            with self.assertRaises(SyntaxError) as error:
                filt_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales').transform_filter(f)
                filt_chart.to_html()
            self.assertIn(str(error.exception), ['Incorrect syntax, must be datum.{field} == {value}',
                                            'Incorrect syntax, must be datum.{field} > {value}',
                                            'Incorrect syntax, must be datum.{field} < {value}'])

    def test_aggregate_error(self):
        """Pie chart aggregate error."""
        for a in NOT_VALID_AGGREGATES:
            with self.assertRaises(ValueError) as error:
                agg_chart = (aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales')
                             .transform_aggregate(new_field=f'{a}(sales)'))
                agg_chart.to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['AGGREGATE_OPERATION'].format(operation=a))

    def test_aggregate_error_not_defined_encoding_channels(self):
        """Pie chart aggregate error raised when encoding channels are not defined in aggregation."""
        with self.assertRaises(ValueError) as error:
            agg_chart = (aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales')
                         .transform_aggregate(mean_sales='mean(sales)', groupby=['model']))
            agg_chart.to_html()

        self.assertRegex(str(error.exception), r'Encoding channel\(s\) .* must be defined in aggregate .*'
                                               r', otherwise that fields will disappear.')
