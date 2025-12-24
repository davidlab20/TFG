import aframexr
import math
import unittest

from bs4 import BeautifulSoup

from aframexr.api.filters import FilterTransform
from aframexr.utils.constants import DEFAULT_CHART_HEIGHT
from tests.constants import *  # Constants used for testing


def _bars_bases_are_on_x_axis(bars_chart: aframexr.Chart) -> bool:
    """Verify that the bars are well-placed in the x-axis (the base of the bar is in the x-axis)."""

    soup = BeautifulSoup(bars_chart.to_html(), 'html.parser')
    bars = soup.find_all('a-box')
    for b in bars:
        bar_height = float(b['height'])  # Total height of the bar
        y_axis_midpoint = float(b['position'].split()[1])  # Y-axis coordinate
        if not math.isclose(bar_height, 2 * y_axis_midpoint):
            return False  # The height of the bar must be twice the value of its y-axis midpoint
    return True

def _bars_height_does_not_exceed_max_height(bars_chart: aframexr.Chart) -> bool:
    """Verify that every bar height does not exceed the maximum height."""

    max_height = float(bars_chart.to_dict().get('height', DEFAULT_CHART_HEIGHT))

    soup = BeautifulSoup(bars_chart.to_html(), 'html.parser')
    bars = soup.find_all('a-box')
    for b in bars:
        bar_height = float(b['height'])  # Total height of the bar
        if bar_height > max_height:
            return False
    return True


class TestMarkBarOK(unittest.TestCase):
    """Bars chart OK tests."""

    def test_simple(self):
        """Simple bars chart creation."""

        bars_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales')
        bars_chart.show()
        assert _bars_bases_are_on_x_axis(bars_chart)
        assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_data_format(self):
        """Bars chart changing data format creation."""

        for d in DATA_FORMATS:
            bars_chart = aframexr.Chart(d).mark_bar().encode(x='model', y='sales')
            bars_chart.show()
            assert _bars_bases_are_on_x_axis(bars_chart)
            assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_position(self):
        """Bars chart changing position creation."""

        for p in POSITIONS:
            bars_chart = aframexr.Chart(DATA, position=p).mark_bar().encode(x='model', y='sales')
            bars_chart.show()
            assert _bars_bases_are_on_x_axis(bars_chart)
            assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_position_format(self):
        """Bars chart changing position format creation."""

        for p in POSITION_FORMATS:
            bars_chart = aframexr.Chart(DATA, position=p).mark_bar().encode(x='model', y='sales')
            bars_chart.show()
            assert _bars_bases_are_on_x_axis(bars_chart)
            assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_rotation(self):
        """Bars chart changing rotation creation."""

        for r in ROTATIONS:
            bars_chart = aframexr.Chart(DATA, rotation=r).mark_bar().encode(x='model', y='sales')
            bars_chart.show()
            assert _bars_bases_are_on_x_axis(bars_chart)
            assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_rotation_format(self):
        """Bars chart changing rotation format creation."""

        for r in ROTATION_FORMATS:
            bars_chart = aframexr.Chart(DATA, rotation=r).mark_bar().encode(x='model', y='sales')
            bars_chart.show()
            assert _bars_bases_are_on_x_axis(bars_chart)
            assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_size(self):
        """Bars chart changing size creation."""

        for s in MARK_BAR_POINT_SIZES:
            bars_chart = aframexr.Chart(DATA).mark_bar(size=s).encode(x='model', y='sales')
            bars_chart.show()
            assert _bars_bases_are_on_x_axis(bars_chart)
            assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_height(self):
        """Bars chart changing height creation."""

        for h in MARK_BAR_POINT_HEIGHTS:
            bars_chart = aframexr.Chart(DATA, height=h).mark_bar().encode(x='model', y='sales')
            bars_chart.show()
            assert _bars_bases_are_on_x_axis(bars_chart)
            assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_encoding(self):
        """Bars chart changing encoding creation."""

        for e in MARK_BAR_ENCODINGS:
            bars_chart = aframexr.Chart(DATA).mark_bar().encode(**e)
            bars_chart.show()
            assert _bars_bases_are_on_x_axis(bars_chart)
            assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_filter(self):
        """Bars chart changing filter creation."""

        for eq in FILTER_EQUATIONS:
            for f in [eq, FilterTransform.from_string(eq)]:  # Filter using equation and using FilterTransform object
                bars_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales').transform_filter(f)
                bars_chart.show()
                assert _bars_bases_are_on_x_axis(bars_chart)
                assert _bars_height_does_not_exceed_max_height(bars_chart)

    def test_aggregate(self):
        """Bar chart changing aggregates creation."""

        for a in AGGREGATES:
            bar_chart = (aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales')
                         .transform_aggregate(new_field=f'{a}(sales)'))
            bar_chart.show()
            assert _bars_bases_are_on_x_axis(bar_chart)
            assert _bars_height_does_not_exceed_max_height(bar_chart)

    def test_aggregate_position_rotation_size_height_encoding_filter(self):
        """Bars chart changing position, rotation size, height, encoding and filter creation."""

        for a, p, r, s, h, e, f in zip(AGGREGATES, POSITIONS, ROTATIONS, MARK_BAR_POINT_SIZES, MARK_BAR_POINT_HEIGHTS,
                                       MARK_BAR_ENCODINGS, FILTER_EQUATIONS):
            bars_chart = (aframexr.Chart(DATA, position=p, rotation=r, height=h).mark_bar(size=s).encode(**e)
                          .transform_filter(f).transform_aggregate(agg=f'{a}(sales)'))
            bars_chart.show()
            assert _bars_bases_are_on_x_axis(bars_chart)
            assert _bars_height_does_not_exceed_max_height(bars_chart)


class TestMarkBarError(unittest.TestCase):
    """Bars chart error tests."""

    def test_position_error(self):
        """Bars chart position error."""

        for p in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_bar().encode(x='model', y='sales')
            assert str(error.exception) == f'The position: {p} is not correct. Must be "x y z".'

        for p in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_bar().encode(x='model', y='sales')
            assert str(error.exception) == 'The position values must be numeric.'

    def test_rotation_error(self):
        """Bars chart rotation error."""

        for r in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_bar().encode(x='model', y='sales')
            assert str(error.exception) == f'The rotation: {r} is not correct. Must be "x y z".'

        for r in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_bar().encode(x='model', y='sales')
            assert str(error.exception) == 'The rotation values must be numeric.'

    def test_size_error(self):
        """Bars chart size error."""

        for s in NOT_GREATER_THAN_0_MARK_BAR_POINT_SIZES_HEIGHTS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_bar(size=s).encode(x='model', y='sales')
            assert str(error.exception) == 'The size must be greater than 0.'

    def test_height_error(self):
        """Bars chart height error."""

        for h in NOT_GREATER_THAN_0_MARK_BAR_POINT_SIZES_HEIGHTS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, height=h).mark_bar().encode(x='model', y='sales')
            assert str(error.exception) == 'The height must be greater than 0.'

    def test_encoding_error(self):
        """Bars chart encoding error."""

        for e in NON_EXISTING_MARK_BAR_POINT_ENCODINGS:
            with self.assertRaises(KeyError) as error:
                bars_chart = aframexr.Chart(DATA).mark_bar().encode(**e)
                bars_chart.show()
            assert 'Data has no field ' in str(error.exception)

        for e in NOT_VALID_MARK_BAR_POINT_ENCODINGS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_bar().encode(**e)
            assert str(error.exception) == 'At least 2 of (x, y, z) must be specified.'

    def test_filter_warning(self):
        """Bars chart filter warning."""

        for f in WARNING_FILTER_EQUATIONS:
            with self.assertWarns(UserWarning) as warning:
                filt_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales').transform_filter(f)
                filt_chart.show()
            assert str(warning.warning) == f'Data does not contain values for the filter: {f}.'

    def test_filter_error(self):
        """Bars chart filter error."""

        for f in ERROR_FILTER_EQUATIONS:
            with self.assertRaises(SyntaxError) as error:
                filt_chart = aframexr.Chart(DATA).mark_bar().encode(x='model', y='sales').transform_filter(f)
                filt_chart.show()
            assert str(error.exception) in ['Incorrect syntax, must be datum.{field} == {value}',
                                            'Incorrect syntax, must be datum.{field} > {value}',
                                            'Incorrect syntax, must be datum.{field} < {value}']