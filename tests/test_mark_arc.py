import aframexr
import math
import unittest

from bs4 import BeautifulSoup

from aframexr.api.filters import FilterTransform
from tests.constants import *  # Constants used for testing


def _all_theta_sum_is_360_degrees(pie_chart: aframexr.Chart) -> bool:
    """Verify that the sum for the theta length of every slice is 360 degrees."""

    total_theta_length = 0

    soup = BeautifulSoup(pie_chart.to_html(), 'html.parser')
    slices = soup.find_all('a-cylinder')
    for s in slices:
        total_theta_length += float(s['theta-length'])
    if not math.isclose(total_theta_length, 360):
        return False
    return True

def _slices_are_well_placed(pie_chart: aframexr.Chart) -> bool:
    """Verify that the slices are well-placed in the pie chart (relative position has to be the same for all)."""

    soup = BeautifulSoup(pie_chart.to_html(), 'html.parser')
    slices = soup.find_all('a-cylinder')
    position = slices[0]['position']
    for s in slices:
        if s['position'] != position:
            return False
    return True


class TestMarkArcOK(unittest.TestCase):
    """Pie chart OK tests."""

    def test_simple(self):
        """Simple pie chart creation."""

        pie_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales')
        pie_chart.show()
        assert _all_theta_sum_is_360_degrees(pie_chart)
        assert _slices_are_well_placed(pie_chart)

    def test_data_format(self):
        """Pie chart changing data format creation."""

        for d in DATA_FORMATS:
            pie_chart = aframexr.Chart(d).mark_arc().encode(color='model', theta='sales')
            pie_chart.show()
            assert _all_theta_sum_is_360_degrees(pie_chart)
            assert _slices_are_well_placed(pie_chart)

    def test_position(self):
        """Pie chart changing position creation."""

        for p in POSITIONS:
            pie_chart = aframexr.Chart(DATA, position=p).mark_arc().encode(color='model', theta='sales')
            pie_chart.show()
            assert _all_theta_sum_is_360_degrees(pie_chart)
            assert _slices_are_well_placed(pie_chart)

    def test_position_format(self):
        """Pie chart changing position format creation."""

        for p in POSITION_FORMATS:
            pie_chart = aframexr.Chart(DATA, position=p).mark_arc().encode(color='model', theta='sales')
            pie_chart.show()
            assert _all_theta_sum_is_360_degrees(pie_chart)
            assert _slices_are_well_placed(pie_chart)

    def test_rotation(self):
        """Pie chart changing rotation creation."""

        for r in ROTATIONS:
            pie_chart = aframexr.Chart(DATA, rotation=r).mark_arc().encode(color='model', theta='sales')
            pie_chart.show()
            assert _all_theta_sum_is_360_degrees(pie_chart)
            assert _slices_are_well_placed(pie_chart)

    def test_rotation_format(self):
        """Pie chart changing rotation format creation."""

        for r in ROTATION_FORMATS:
            pie_chart = aframexr.Chart(DATA, rotation=r).mark_arc().encode(color='model', theta='sales')
            pie_chart.show()
            assert _all_theta_sum_is_360_degrees(pie_chart)
            assert _slices_are_well_placed(pie_chart)

    def test_radius(self):
        """Pie chart changing radius creation."""

        for r in MARK_ARC_RADIUS:
            pie_chart = aframexr.Chart(DATA).mark_arc(radius=r).encode(color='model', theta='sales')
            pie_chart.show()
            assert _all_theta_sum_is_360_degrees(pie_chart)
            assert _slices_are_well_placed(pie_chart)

    def test_filter(self):
        """Pie chart changing filter creation."""

        for eq in FILTER_EQUATIONS:
            for f in [eq, FilterTransform.from_string(eq)]:  # Filter using equation and using FilterTransform object
                pie_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales').transform_filter(f)
                pie_chart.show()
                assert _all_theta_sum_is_360_degrees(pie_chart)
                assert _slices_are_well_placed(pie_chart)

    def test_aggregate(self):
        """Pie chart changing aggregates creation."""

        for a in AGGREGATES:
            pie_chart = (aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales')
                         .transform_aggregate(new_field=f'{a}(sales)'))
            pie_chart.show()
            assert _all_theta_sum_is_360_degrees(pie_chart)
            assert _slices_are_well_placed(pie_chart)

    def test_aggregate_position_rotation_radius_filter(self):
        """Pie chart changing position, rotation, radius and filter creation."""

        for agg, pos, rot, rad, fil in zip(AGGREGATES, POSITIONS, ROTATIONS, MARK_ARC_RADIUS, FILTER_EQUATIONS):
            pie_chart = (aframexr.Chart(DATA, position=pos, rotation=rot).mark_arc(radius=rad)
                         .encode(color='model',theta='sales').transform_filter(fil)
                         .transform_aggregate(agg=f'{agg}(sales)'))
            pie_chart.show()
            assert _all_theta_sum_is_360_degrees(pie_chart)
            assert _slices_are_well_placed(pie_chart)


class TestMarkArcError(unittest.TestCase):
    """Pie chart error tests."""

    def test_position_error(self):
        """Pie chart position error."""

        for p in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_arc().encode(color='model', theta='sales')
            assert str(error.exception) == f'The position: {p} is not correct. Must be "x y z".'

        for p in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_arc().encode(color='model', theta='sales')
            assert str(error.exception) == 'The position values must be numeric.'

    def test_rotation_error(self):
        """Pie chart rotation error."""

        for r in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_arc().encode(color='model', theta='sales')
            assert str(error.exception) == f'The rotation: {r} is not correct. Must be "x y z".'

        for r in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_arc().encode(color='model', theta='sales')
            assert str(error.exception) == 'The rotation values must be numeric.'

    def test_radius_error(self):
        """Pie chart radius error."""

        for r in NOT_GREATER_THAN_0_MARK_ARC_RADIUS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_arc(radius=r).encode(color='model', theta='sales')
            assert str(error.exception) == 'The radius must be greater than 0.'

    def test_encoding_error(self):
        """Pie chart encoding error."""

        for e in NON_EXISTING_MARK_ARC_ENCODINGS:
            with self.assertRaises(KeyError) as error:
                pie_chart = aframexr.Chart(DATA).mark_arc().encode(**e)
                pie_chart.show()
            assert 'Data has no field ' in str(error.exception)

        for e in NOT_VALID_MARK_ARC_ENCODINGS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_arc().encode(**e)
            assert str(error.exception) in ['Parameter theta must be specified in arc chart.',
                                            'Parameter color must be specified in arc chart.']

    def test_filter_warning(self):
        """Pie chart filter warning."""

        for f in WARNING_FILTER_EQUATIONS:
            with self.assertWarns(UserWarning) as warning:
                filt_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales').transform_filter(f)
                filt_chart.show()
            assert str(warning.warning) == f'Data does not contain values for the filter: {f}.'

    def test_filter_error(self):
        """Pie chart filter error."""

        for f in ERROR_FILTER_EQUATIONS:
            with self.assertRaises(SyntaxError) as error:
                filt_chart = aframexr.Chart(DATA).mark_arc().encode(color='model', theta='sales').transform_filter(f)
                filt_chart.show()
            assert str(error.exception) in ['Incorrect syntax, must be datum.{field} == {value}',
                                            'Incorrect syntax, must be datum.{field} > {value}',
                                            'Incorrect syntax, must be datum.{field} < {value}']
