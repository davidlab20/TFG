import aframexr
import unittest

from bs4 import BeautifulSoup

from aframexr.api.filters import FilterTransform
from aframexr.utils.constants import DEFAULT_POINT_RADIUS
from tests.constants import *  # Constants used for testing


def _every_radius_does_not_exceed_max_radius(point_chart: aframexr.Chart) -> bool:
    """Verify that every point radius does not exceed the maximum radius."""

    max_radius = point_chart.to_dict()['mark'].get('max_radius', DEFAULT_POINT_RADIUS)

    soup = BeautifulSoup(point_chart.to_html(), 'html.parser')
    points = soup.find_all('a-sphere')
    for p in points:
        point_radius = float(p['radius'])  # Radius of the sphere
        if point_radius > max_radius:
            return False
    return True


class TestMarkPointOK(unittest.TestCase):
    """Mark point OK tests."""

    def test_simple(self):
        """Simple mark point creation."""

        point_chart = aframexr.Chart(DATA).mark_point().encode(x='model', y='sales')
        point_chart.show()
        assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_data_format(self):
        """Mark point changing data format creation."""

        for d in DATA_FORMATS:
            point_chart = aframexr.Chart(d).mark_point().encode(x='model', y='sales')
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_position(self):
        """Mark point changing position creation."""

        for p in POSITIONS:
            point_chart = aframexr.Chart(DATA, position=p).mark_point().encode(x='model', y='sales')
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_position_format(self):
        """Mark point changing position format creation."""

        for p in POSITION_FORMATS:
            point_chart = aframexr.Chart(DATA, position=p).mark_point().encode(x='model', y='sales')
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_rotation(self):
        """Mark point changing rotation creation."""

        for r in ROTATIONS:
            point_chart = aframexr.Chart(DATA, rotation=r).mark_point().encode(x='model', y='sales')
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_rotation_format(self):
        """Mark point changing rotation format creation."""

        for r in ROTATION_FORMATS:
            point_chart = aframexr.Chart(DATA, rotation=r).mark_point().encode(x='model', y='sales')
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_size(self):
        """Mark point changing size creation."""

        for s in MARK_BAR_POINT_SIZES:
            point_chart = aframexr.Chart(DATA).mark_point(size=s).encode(x='model', y='sales')
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_height(self):
        """Mark point changing height creation."""

        for h in MARK_BAR_POINT_HEIGHTS:
            point_chart = aframexr.Chart(DATA, height=h).mark_point().encode(x='model', y='sales')
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_encoding(self):
        """Mark point changing encoding creation."""

        for e in MARK_POINT_ENCODINGS:
            point_chart = aframexr.Chart(DATA).mark_point().encode(**e)
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_filter(self):
        """Mark point changing filter creation."""

        for eq in FILTER_EQUATIONS:
            for f in [eq, FilterTransform.from_string(eq)]:  # Filter using equation and using FilterTransform object
                point_chart = aframexr.Chart(DATA).mark_point().encode(x='model', y='sales').transform_filter(f)
                point_chart.show()
                assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_aggregate(self):
        """Mark point changing aggregate creation."""

        for a in AGGREGATES:
            point_chart = (aframexr.Chart(DATA).mark_point().encode(x='model', y='sales')
                         .transform_aggregate(new_field=f'{a}(sales)'))
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_aggregate_position_rotation_size_height_encoding_filter(self):
        """Mark point changing position, rotation size, height, encoding and filter creation."""

        for a, p, r, s, h, e, f in zip(AGGREGATES, POSITIONS, ROTATIONS, MARK_BAR_POINT_SIZES, MARK_BAR_POINT_HEIGHTS,
                                       MARK_POINT_ENCODINGS, FILTER_EQUATIONS):
            point_chart = (aframexr.Chart(DATA, position=p, rotation=r, height=h).mark_point(size=s).encode(**e)
                           .transform_filter(f).transform_aggregate(agg=f'{a}(sales)'))
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)

    def test_concatenating_charts(self):
        """Mark point concatenating charts creation."""

        for p, r, s, h, e, f in zip(POSITIONS, ROTATIONS, MARK_BAR_POINT_SIZES, MARK_BAR_POINT_HEIGHTS,
                                    MARK_POINT_ENCODINGS, FILTER_EQUATIONS):
            point_chart = (aframexr.Chart(DATA, position=p, rotation=r, height=h).mark_point(size=s).encode(**e)
                           .transform_filter(f))
            point_chart.show()
            assert _every_radius_does_not_exceed_max_radius(point_chart)


class TestMarkPointError(unittest.TestCase):
    """Mark point error tests."""

    def test_position_error(self):
        """Mark point position error."""

        for p in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_point().encode(x='model', y='sales')
            assert str(error.exception) == f'The position: {p} is not correct. Must be "x y z".'

        for p in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_point().encode(x='model', y='sales')
            assert str(error.exception) == 'The position values must be numeric.'

    def test_rotation_error(self):
        """Mark point rotation error."""

        for r in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_point().encode(x='model', y='sales')
            assert str(error.exception) == f'The rotation: {r} is not correct. Must be "x y z".'

        for r in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_point().encode(x='model', y='sales')
            assert str(error.exception) == 'The rotation values must be numeric.'

    def test_size_error(self):
        """Mark point size error."""

        for s in NOT_GREATER_THAN_0_MARK_BAR_POINT_SIZES_HEIGHTS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_point(size=s).encode(x='model', y='sales')
            assert str(error.exception) == 'The size must be greater than 0.'

    def test_height_error(self):
        """Mark point height error."""

        for h in NOT_GREATER_THAN_0_MARK_BAR_POINT_SIZES_HEIGHTS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, height=h).mark_point().encode(x='model', y='sales')
            assert str(error.exception) == 'The height must be greater than 0.'

    def test_encoding_error(self):
        """Mark point encoding error."""

        for e in NON_EXISTING_MARK_BAR_POINT_ENCODINGS:
            with self.assertRaises(KeyError) as error:
                point_chart = aframexr.Chart(DATA).mark_point().encode(**e)
                point_chart.show()
            assert 'Data has no field ' in str(error.exception)

        for e in NOT_VALID_MARK_BAR_POINT_ENCODINGS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_point().encode(**e)
            assert str(error.exception) == 'At least 2 of (x, y, z) must be specified.'

    def test_filter_warning(self):
        """Mark point filter warning."""

        for f in WARNING_FILTER_EQUATIONS:
            with self.assertWarns(UserWarning) as warning:
                filt_chart = aframexr.Chart(DATA).mark_point().encode(x='model', y='sales').transform_filter(f)
                filt_chart.show()
            assert str(warning.warning) == f'Data does not contain values for the filter: {f}.'

    def test_filter_error(self):
        """Mark point filter error."""

        for f in ERROR_FILTER_EQUATIONS:
            with self.assertRaises(SyntaxError) as error:
                filt_chart = aframexr.Chart(DATA).mark_point().encode(x='model', y='sales').transform_filter(f)
                filt_chart.show()
            assert str(error.exception) in ['Incorrect syntax, must be datum.{field} == {value}',
                                            'Incorrect syntax, must be datum.{field} > {value}',
                                            'Incorrect syntax, must be datum.{field} < {value}']
