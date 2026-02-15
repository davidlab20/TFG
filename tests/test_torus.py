import aframexr
import unittest

from aframexr.utils.constants import AVAILABLE_ENVIRONMENTS, ERROR_MESSAGES
from .constants import *


class TestTorusOK(unittest.TestCase):
    """Tests for torus creation."""

    def test_simple(self):
        """Simple torus creation."""
        torus = aframexr.Torus()
        torus.to_html()

    def test_from_dict(self):
        """Torus creation using form_dict() method."""
        torus = aframexr.Torus.from_dict(aframexr.Torus().to_dict())
        torus.to_html()

    def test_from_json(self):
        """Torus creation using form_json() method."""
        torus = aframexr.Torus.from_json(aframexr.Torus().to_json())
        torus.to_html()

    def test_color(self):
        """Torus with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            torus = aframexr.Torus(color=c)
            torus.to_html()

    def test_position(self):
        """Torus with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            torus = aframexr.Torus(position=p)
            torus.to_html()

    def test_radius(self):
        """Torus with specific radius creation."""
        for r in RADIUS:
            torus = aframexr.Torus(radius=r)
            torus.to_html()

    def test_radius_tubular(self):
        """Torus with specific radius tubular creation."""
        for r in RADIUS:
            torus = aframexr.Torus(radius_tubular=r)
            torus.to_html()

    def test_rotation(self):
        """Torus with specific rotation creation."""
        for r in ROTATIONS + ROTATION_FORMATS:
            torus = aframexr.Torus(rotation=r)
            torus.to_html()

    def test_all_parameters(self):
        """Torus creation with all parameters specified."""
        for c, p, rad, rt, rot in zip(SIMPLE_ELEMENTS_COLORS, POSITIONS, RADIUS, RADIUS, ROTATIONS):
            torus = aframexr.Torus(color=c, position=p, radius=rad, radius_tubular=rt, rotation=rot)
            torus.to_html()

    def test_concatenation(self):
        """Concatenation of simple tetrahedron."""
        concatenated_chart = aframexr.Torus(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Torus(position=p)
        concatenated_chart.to_html()

    def test_environment(self):
        """Scene creation with personalized environment."""
        for e in AVAILABLE_ENVIRONMENTS:
            aframexr.Torus().to_html(environment=e)


class TestTorusERROR(unittest.TestCase):
    """Tests for torus creation error."""

    def test_color_error(self):
        """Torus with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            torus = aframexr.Torus(color=not_an_string)
            torus.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_radius_error(self):
        """Torus with specific radius creation error."""
        for r in NOT_GREATER_THAN_0_RADIUS:
            with self.assertRaises(ValueError) as error:
                torus = aframexr.Torus(radius=r)
                torus.to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius'))

    def test_radius_tubular_error(self):
        """Torus with specific radius tubular creation error."""
        for r in NOT_GREATER_THAN_0_RADIUS:
            with self.assertRaises(ValueError) as error:
                torus = aframexr.Torus(radius_tubular=r)
                torus.to_html()
            self.assertEqual(
                str(error.exception),
                ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius_tubular')
            )

    def test_environment_error(self):
        """Scene creation with invalid personalized environment."""
        environment = 'bad_environment'
        torus = aframexr.Torus()
        with self.assertRaises(ValueError) as error:
            # noinspection PyTypeChecker
            torus.to_html(environment=environment)
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENVIRONMENT'].format(environment=environment))
