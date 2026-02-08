import aframexr
import unittest

from aframexr.utils.constants import ERROR_MESSAGES
from .constants import *


class TestSphereOK(unittest.TestCase):
    """Tests for simple sphere creation."""

    def test_simple(self):
        """Simple sphere creation."""
        sphere = aframexr.Sphere()
        sphere.to_html()

    def test_from_dict(self):
        """Sphere creation using form_dict() method."""
        sphere = aframexr.Sphere.from_dict(aframexr.Sphere().to_dict())
        sphere.to_html()

    def test_from_json(self):
        """Sphere creation using form_json() method."""
        sphere = aframexr.Sphere.from_json(aframexr.Sphere().to_json())
        sphere.to_html()

    def test_color(self):
        """Sphere with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            sphere = aframexr.Sphere(color=c)
            sphere.to_html()

    def test_position(self):
        """Sphere with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            sphere = aframexr.Sphere(position=p)
            sphere.to_html()

    def test_radius(self):
        """Sphere with specific radius creation."""
        for r in MARK_ARC_RADIUS:
            sphere = aframexr.Sphere(radius=r)
            sphere.to_html()

    def test_all_parameters(self):
        """Sphere creation with all parameters specified."""
        for c, p, r in zip(SIMPLE_ELEMENTS_COLORS, POSITIONS, MARK_ARC_RADIUS):
            sphere = aframexr.Sphere(color=c, position=p, radius=r)
            sphere.to_html()

    def test_concatenation(self):
        """Concatenation of simple spheres."""
        concatenated_chart = aframexr.Sphere(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Sphere(position=p)
        concatenated_chart.to_html()


class TestSphereERROR(unittest.TestCase):
    """Tests for sphere creation error."""

    def test_color_error(self):
        """Sphere with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            sphere = aframexr.Sphere(color=not_an_string)
            sphere.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_radius_error(self):
        """Sphere with specific radius creation error."""
        for r in NOT_GREATER_THAN_0_MARK_ARC_RADIUS:
            with self.assertRaises(ValueError) as error:
                sphere = aframexr.Sphere(radius=r)
                sphere.to_html()
            self.assertEqual(str(error.exception), ERROR_MESSAGES['POSITIVE_NUMBER'].format(param_name='specs.radius'))
