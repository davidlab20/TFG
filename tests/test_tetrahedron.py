import aframexr
import unittest

from aframexr.utils.constants import ERROR_MESSAGES
from .constants import *


class TestTetrahedronOK(unittest.TestCase):
    """Tests for simple tetrahedron creation."""

    def test_simple(self):
        """Simple tetrahedron creation."""
        tetrahedron = aframexr.Tetrahedron()
        tetrahedron.to_html()

    def test_from_dict(self):
        """Tetrahedron creation using form_dict() method."""
        tetrahedron = aframexr.Tetrahedron.from_dict(aframexr.Tetrahedron().to_dict())
        tetrahedron.to_html()

    def test_from_json(self):
        """Tetrahedron creation using form_json() method."""
        tetrahedron = aframexr.Tetrahedron.from_json(aframexr.Tetrahedron().to_json())
        tetrahedron.to_html()

    def test_color(self):
        """Tetrahedron with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            tetrahedron = aframexr.Tetrahedron(color=c)
            tetrahedron.to_html()

    def test_position(self):
        """Tetrahedron with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            tetrahedron = aframexr.Tetrahedron(position=p)
            tetrahedron.to_html()

    def test_radius(self):
        """Tetrahedron with specific radius creation."""
        for r in RADIUS:
            tetrahedron = aframexr.Tetrahedron(radius=r)
            tetrahedron.to_html()

    def test_all_parameters(self):
        """Tetrahedron creation with all parameters specified."""
        for c, p, r in zip(SIMPLE_ELEMENTS_COLORS, POSITIONS, RADIUS):
            tetrahedron = aframexr.Tetrahedron(color=c, position=p, radius=r)
            tetrahedron.to_html()

    def test_concatenation(self):
        """Concatenation of simple tetrahedron."""
        concatenated_chart = aframexr.Tetrahedron(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Tetrahedron(position=p)
        concatenated_chart.to_html()


class TestTetrahedronERROR(unittest.TestCase):
    """Tests for tetrahedron creation error."""

    def test_color_error(self):
        """Tetrahedron with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            tetrahedron = aframexr.Tetrahedron(color=not_an_string)
            tetrahedron.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_radius_error(self):
        """Tetrahedron with specific radius creation error."""
        for r in NOT_GREATER_THAN_0_RADIUS:
            with self.assertRaises(ValueError) as error:
                tetrahedron = aframexr.Tetrahedron(radius=r)
                tetrahedron.to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius'))
