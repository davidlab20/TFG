import aframexr
import unittest

from aframexr.utils.constants import ERROR_MESSAGES
from .constants import *


class TestConeOK(unittest.TestCase):
    """Tests for simple cone creation."""

    def test_simple(self):
        """Simple cone creation."""
        cone = aframexr.Cone()
        cone.to_html()

    def test_from_dict(self):
        """Cone creation using form_dict() method."""
        cone = aframexr.Cone.from_dict(aframexr.Cone().to_dict())
        cone.to_html()

    def test_from_json(self):
        """Cone creation using form_json() method."""
        cone = aframexr.Cone.from_json(aframexr.Cone().to_json())
        cone.to_html()

    def test_color(self):
        """Cone with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            cone = aframexr.Cone(color=c)
            cone.to_html()

    def test_height(self):
        """Cone with specific height creation."""
        for h in ALL_MARK_DEPTHS_HEIGHTS_WIDTHS:
            cone = aframexr.Cone(height=h)
            cone.to_html()

    def test_position(self):
        """Cone with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            cone = aframexr.Cone(position=p)
            cone.to_html()

    def test_radius_bottom(self):
        """Cone with specific bottom's radius creation."""
        for r in MARK_ARC_RADIUS:
            cone = aframexr.Cone(radius_bottom=r)
            cone.to_html()

    def test_radius_top(self):
        """Cone with specific top's radius creation."""
        for r in MARK_ARC_RADIUS:
            cone = aframexr.Cone(radius_top=r)
            cone.to_html()

    def test_all_parameters(self):
        """Cone creation with all parameters specified."""
        for c, h, p, rb, rt in zip(SIMPLE_ELEMENTS_COLORS, ALL_MARK_DEPTHS_HEIGHTS_WIDTHS, POSITIONS, MARK_ARC_RADIUS,
                                   MARK_ARC_RADIUS):
            cone = aframexr.Cone(color=c, height=h, position=p, radius_bottom=rb, radius_top=rt)
            cone.to_html()

    def test_concatenation(self):
        """Concatenation of simple cones."""
        concatenated_chart = aframexr.Cone(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Cone(position=p)
        concatenated_chart.to_html()


class TestConeERROR(unittest.TestCase):
    """Tests for cone creation errors."""

    def test_color_error(self):
        """Cone with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            cone = aframexr.Cone(color=not_an_string)
            cone.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_radius_bottom_error(self):
        """Cone with specific bottom's radius creation error."""
        for r in NOT_GREATER_THAN_0_MARK_ARC_RADIUS:
            with self.assertRaises(ValueError) as error:
                cone = aframexr.Cone(radius_bottom=r)
                cone.to_html()
            self.assertEqual(
                str(error.exception),
                ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius_bottom')
            )

    def test_radius_top_error(self):
        """Cone with specific top's radius creation error."""
        for r in NOT_GREATER_THAN_0_MARK_ARC_RADIUS:
            with self.assertRaises(ValueError) as error:
                cone = aframexr.Cone(radius_top=r)
                cone.to_html()
            self.assertEqual(
                str(error.exception),
                ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius_top')
            )
