import aframexr
import unittest

from aframexr.utils.constants import ERROR_MESSAGES
from .constants import *


class TestDodecahedronOK(unittest.TestCase):
    """Tests for simple dodecahedron creation."""

    def test_simple(self):
        """Simple dodecahedron creation."""
        dodecahedron = aframexr.Dodecahedron()
        dodecahedron.to_html()

    def test_from_dict(self):
        """Dodecahedron creation using form_dict() method."""
        dodecahedron = aframexr.Dodecahedron.from_dict(aframexr.Dodecahedron().to_dict())
        dodecahedron.to_html()

    def test_from_json(self):
        """Dodecahedron creation using form_json() method."""
        dodecahedron = aframexr.Dodecahedron.from_json(aframexr.Dodecahedron().to_json())
        dodecahedron.to_html()

    def test_color(self):
        """Dodecahedron with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            dodecahedron = aframexr.Dodecahedron(color=c)
            dodecahedron.to_html()

    def test_position(self):
        """Dodecahedron with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            dodecahedron = aframexr.Dodecahedron(position=p)
            dodecahedron.to_html()

    def test_radius(self):
        """Dodecahedron with specific radius creation."""
        for r in MARK_ARC_RADIUS:
            dodecahedron = aframexr.Dodecahedron(radius=r)
            dodecahedron.to_html()

    def test_all_parameters(self):
        """Dodecahedron creation with all parameters specified."""
        for c, p, r in zip(SIMPLE_ELEMENTS_COLORS, POSITIONS, MARK_ARC_RADIUS):
            dodecahedron = aframexr.Dodecahedron(color=c, position=p, radius=r)
            dodecahedron.to_html()

    def test_concatenation(self):
        """Concatenation of simple dodecahedron."""
        concatenated_chart = aframexr.Dodecahedron(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Dodecahedron(position=p)
        concatenated_chart.to_html()


class TestDodecahedronERROR(unittest.TestCase):
    """Tests for dodecahedron creation error."""

    def test_color_error(self):
        """Dodecahedron with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            dodecahedron = aframexr.Dodecahedron(color=not_an_string)
            dodecahedron.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_radius_error(self):
        """Dodecahedron with specific radius creation error."""
        for r in NOT_GREATER_THAN_0_RADIUS:
            with self.assertRaises(ValueError) as error:
                dodecahedron = aframexr.Dodecahedron(radius=r)
                dodecahedron.to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius'))
