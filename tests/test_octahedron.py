import aframexr
import unittest

from aframexr.utils.constants import AVAILABLE_ENVIRONMENTS, ERROR_MESSAGES
from .constants import *


class TestOctahedronOK(unittest.TestCase):
    """Tests for simple octahedron creation."""

    def test_simple(self):
        """Simple octahedron creation."""
        octahedron = aframexr.Octahedron()
        octahedron.to_html()

    def test_from_dict(self):
        """Octahedron creation using form_dict() method."""
        octahedron = aframexr.Octahedron.from_dict(aframexr.Octahedron().to_dict())
        octahedron.to_html()

    def test_from_json(self):
        """Octahedron creation using form_json() method."""
        octahedron = aframexr.Octahedron.from_json(aframexr.Octahedron().to_json())
        octahedron.to_html()

    def test_color(self):
        """Octahedron with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            octahedron = aframexr.Octahedron(color=c)
            octahedron.to_html()

    def test_position(self):
        """Octahedron with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            octahedron = aframexr.Octahedron(position=p)
            octahedron.to_html()

    def test_radius(self):
        """Octahedron with specific radius creation."""
        for r in RADIUS:
            octahedron = aframexr.Octahedron(radius=r)
            octahedron.to_html()

    def test_all_parameters(self):
        """Octahedron creation with all parameters specified."""
        for c, p, r in zip(SIMPLE_ELEMENTS_COLORS, POSITIONS, RADIUS):
            octahedron = aframexr.Octahedron(color=c, position=p, radius=r)
            octahedron.to_html()

    def test_concatenation(self):
        """Concatenation of simple octahedron."""
        concatenated_chart = aframexr.Octahedron(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Octahedron(position=p)
        concatenated_chart.to_html()

    def test_environment(self):
        """Scene creation with personalized environment."""
        for e in AVAILABLE_ENVIRONMENTS:
            aframexr.Octahedron().to_html(environment=e)


class TestOctahedronERROR(unittest.TestCase):
    """Tests for octahedron creation error."""

    def test_color_error(self):
        """Octahedron with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            octahedron = aframexr.Octahedron(color=not_an_string)
            octahedron.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_radius_error(self):
        """Octahedron with specific radius creation error."""
        for r in NOT_GREATER_THAN_0_RADIUS:
            with self.assertRaises(ValueError) as error:
                octahedron = aframexr.Octahedron(radius=r)
                octahedron.to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius'))

    def test_environment_error(self):
        """Scene creation with invalid personalized environment."""
        environment = 'bad_environment'
        octahedron = aframexr.Octahedron()
        with self.assertRaises(ValueError) as error:
            # noinspection PyTypeChecker
            octahedron.to_html(environment=environment)
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENVIRONMENT'].format(environment=environment))
