import aframexr
import unittest

from aframexr.utils.constants import ERROR_MESSAGES
from .constants import *


class TestCylinderOK(unittest.TestCase):
    """Tests for simple cylinder creation."""

    def test_simple(self):
        """Simple cylinder creation."""
        cylinder = aframexr.Cylinder()
        cylinder.to_html()

    def test_from_dict(self):
        """Cylinder creation using form_dict() method."""
        cylinder = aframexr.Cylinder.from_dict(aframexr.Cylinder().to_dict())
        cylinder.to_html()

    def test_from_json(self):
        """Cylinder creation using form_json() method."""
        cylinder = aframexr.Cylinder.from_json(aframexr.Cylinder().to_json())
        cylinder.to_html()

    def test_color(self):
        """Cylinder with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            cylinder = aframexr.Cylinder(color=c)
            cylinder.to_html()

    def test_height(self):
        """Cylinder with specific height creation."""
        for h in ALL_MARK_DEPTHS_HEIGHTS_WIDTHS:
            cylinder = aframexr.Cylinder(height=h)
            cylinder.to_html()

    def test_position(self):
        """Cylinder with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            cylinder = aframexr.Cylinder(position=p)
            cylinder.to_html()

    def test_radius(self):
        """Cylinder with specific radius creation."""
        for r in MARK_ARC_RADIUS:
            cylinder = aframexr.Cylinder(radius=r)
            cylinder.to_html()

    def test_rotation(self):
        """Cylinder with specific rotation creation."""
        for r in ROTATIONS + ROTATION_FORMATS:
            cylinder = aframexr.Cylinder(rotation=r)
            cylinder.to_html()

    def test_all_parameters(self):
        """Cylinder creation with all parameters specified."""
        for c, h, p, ra, ro in zip(SIMPLE_ELEMENTS_COLORS, ALL_MARK_DEPTHS_HEIGHTS_WIDTHS, POSITIONS, MARK_ARC_RADIUS,
                                   ROTATIONS):
            cylinder = aframexr.Cylinder(color=c, height=h, position=p, radius=ra, rotation=ro)
            cylinder.to_html()

    def test_concatenation(self):
        """Concatenation of simple cylinders."""
        concatenated_chart = aframexr.Cylinder(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Cylinder(position=p)
        concatenated_chart.to_html()


class TestCylinderERROR(unittest.TestCase):
    """Tests for cylinder creation error."""

    def test_color_error(self):
        """Cylinder with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            cylinder = aframexr.Cylinder(color=not_an_string)
            cylinder.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_radius_error(self):
        """Cylinder with specific radius creation error."""
        for r in NOT_GREATER_THAN_0_RADIUS:
            with self.assertRaises(ValueError) as error:
                cylinder = aframexr.Cylinder(radius=r)
                cylinder.to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius'))
