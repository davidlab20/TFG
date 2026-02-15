import aframexr
import unittest

from aframexr.utils.constants import AVAILABLE_ENVIRONMENTS, ERROR_MESSAGES
from .constants import *


class TestPlaneOK(unittest.TestCase):
    """Test for plane creation."""

    def test_simple(self):
        """Simple plane creation."""
        plane = aframexr.Plane()
        plane.to_html()

    def test_from_dict(self):
        """Plane creation using form_dict() method."""
        plane = aframexr.Plane.from_dict(aframexr.Plane().to_dict())
        plane.to_html()

    def test_from_json(self):
        """Plane creation using form_json() method."""
        plane = aframexr.Plane.from_json(aframexr.Plane().to_json())
        plane.to_html()

    def test_color(self):
        """Plane with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            plane = aframexr.Plane(color=c)
            plane.to_html()

    def test_height(self):
        """Plane with specific height creation."""
        for h in ALL_MARK_DEPTHS_HEIGHTS_WIDTHS:
            plane = aframexr.Plane(height=h)
            plane.to_html()

    def test_position(self):
        """Plane with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            plane = aframexr.Plane(position=p)
            plane.to_html()

    def test_rotation(self):
        """Plane with specific rotation creation."""
        for r in ROTATIONS + ROTATION_FORMATS:
            plane = aframexr.Plane(rotation=r)
            plane.to_html()

    def test_width(self):
        """Plane with specific width creation."""
        for w in ALL_MARK_DEPTHS_HEIGHTS_WIDTHS:
            plane = aframexr.Plane(width=w)
            plane.to_html()

    def test_all_parameters(self):
        """Plane creation with all parameters specified."""
        for c, h, p, r, w in zip(SIMPLE_ELEMENTS_COLORS, ALL_MARK_DEPTHS_HEIGHTS_WIDTHS, POSITIONS, ROTATIONS,
                                 ALL_MARK_DEPTHS_HEIGHTS_WIDTHS):
            plane = aframexr.Plane(color=c, height=h, position=p, rotation=r, width=w)
            plane.to_html()

    def test_concatenation(self):
        """Concatenation of simple planes."""
        concatenated_chart = aframexr.Plane(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Plane(position=p)
        concatenated_chart.to_html()

    def test_environment(self):
        """Scene creation with personalized environment."""
        for e in AVAILABLE_ENVIRONMENTS:
            aframexr.Plane().to_html(environment=e)


class TestPlaneERROR(unittest.TestCase):
    """Tests for plane creation error."""

    def test_color_error(self):
        """Plane with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            plane = aframexr.Plane(color=not_an_string)
            plane.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_environment_error(self):
        """Scene creation with invalid personalized environment."""
        environment = 'bad_environment'
        plane = aframexr.Plane()
        with self.assertRaises(ValueError) as error:
            # noinspection PyTypeChecker
            plane.to_html(environment=environment)
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENVIRONMENT'].format(environment=environment))
