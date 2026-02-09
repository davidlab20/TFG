import aframexr
import unittest

from aframexr.utils.constants import ERROR_MESSAGES
from .constants import *


class TestIcosahedronOK(unittest.TestCase):
    """Tests for simple icosahedron creation."""

    def test_simple(self):
        """Simple icosahedron creation."""
        icosahedron = aframexr.Icosahedron()
        icosahedron.to_html()

    def test_from_dict(self):
        """Icosahedron creation using form_dict() method."""
        icosahedron = aframexr.Icosahedron.from_dict(aframexr.Icosahedron().to_dict())
        icosahedron.to_html()

    def test_from_json(self):
        """Icosahedron creation using form_json() method."""
        icosahedron = aframexr.Icosahedron.from_json(aframexr.Icosahedron().to_json())
        icosahedron.to_html()

    def test_color(self):
        """Icosahedron with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            icosahedron = aframexr.Icosahedron(color=c)
            icosahedron.to_html()

    def test_position(self):
        """Icosahedron with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            icosahedron = aframexr.Icosahedron(position=p)
            icosahedron.to_html()

    def test_radius(self):
        """Icosahedron with specific radius creation."""
        for r in MARK_ARC_RADIUS:
            icosahedron = aframexr.Icosahedron(radius=r)
            icosahedron.to_html()

    def test_all_parameters(self):
        """Icosahedron creation with all parameters specified."""
        for c, p, r in zip(SIMPLE_ELEMENTS_COLORS, POSITIONS, MARK_ARC_RADIUS):
            icosahedron = aframexr.Icosahedron(color=c, position=p, radius=r)
            icosahedron.to_html()

    def test_concatenation(self):
        """Concatenation of simple icosahedron."""
        concatenated_chart = aframexr.Icosahedron(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Icosahedron(position=p)
        concatenated_chart.to_html()


class TestIcosahedronERROR(unittest.TestCase):
    """Tests for icosahedron creation error."""

    def test_color_error(self):
        """Icosahedron with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            icosahedron = aframexr.Icosahedron(color=not_an_string)
            icosahedron.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_radius_error(self):
        """Icosahedron with specific radius creation error."""
        for r in NOT_GREATER_THAN_0_MARK_ARC_RADIUS:
            with self.assertRaises(ValueError) as error:
                icosahedron = aframexr.Icosahedron(radius=r)
                icosahedron.to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius'))
