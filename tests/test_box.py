import aframexr
import unittest

from aframexr.utils.constants import AVAILABLE_ENVIRONMENTS, ERROR_MESSAGES
from .constants import *


class TestBoxOK(unittest.TestCase):
    """Tests for simple box creation."""

    def test_simple(self):
        """Simple box creation."""
        box = aframexr.Box()
        box.to_html()

    def test_from_dict(self):
        """Box creation using form_dict() method."""
        box = aframexr.Box.from_dict(aframexr.Box().to_dict())
        box.to_html()

    def test_from_json(self):
        """Box creation using form_json() method."""
        box = aframexr.Box.from_json(aframexr.Box().to_json())
        box.to_html()

    def test_color(self):
        """Box with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            box = aframexr.Box(color=c)
            box.to_html()

    def test_depth(self):
        """Box with specific depth creation."""
        for d in ALL_MARK_DEPTHS_HEIGHTS_WIDTHS:
            box = aframexr.Box(depth=d)
            box.to_html()

    def test_height(self):
        """Box with specific height creation."""
        for h in ALL_MARK_DEPTHS_HEIGHTS_WIDTHS:
            box = aframexr.Box(height=h)
            box.to_html()

    def test_position(self):
        """Box with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            box = aframexr.Box(position=p)
            box.to_html()

    def test_rotation(self):
        """Box with specific rotation creation."""
        for r in ROTATIONS + ROTATION_FORMATS:
            box = aframexr.Box(rotation=r)
            box.to_html()

    def test_width(self):
        """Box with specific width creation."""
        for w in ALL_MARK_DEPTHS_HEIGHTS_WIDTHS:
            box = aframexr.Box(width=w)
            box.to_html()

    def test_all_parameters(self):
        """Box creation with all parameters specified."""
        for c, d, h, p, r, w in zip(SIMPLE_ELEMENTS_COLORS, ALL_MARK_DEPTHS_HEIGHTS_WIDTHS,
                                    ALL_MARK_DEPTHS_HEIGHTS_WIDTHS, POSITIONS, ROTATIONS,
                                    ALL_MARK_DEPTHS_HEIGHTS_WIDTHS):
            box = aframexr.Box(color=c, depth=d, height=h, position=p, rotation=r, width=w)
            box.to_html()

    def test_concatenation(self):
        """Concatenation of simple boxes."""
        concatenated_chart = aframexr.Box(position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Box(position=p)
        concatenated_chart.to_html()

    def test_environment(self):
        """Scene creation with personalized environment."""
        for e in AVAILABLE_ENVIRONMENTS:
            aframexr.Box().to_html(environment=e)


class TestBoxERROR(unittest.TestCase):
    """Tests for box creation errors."""

    def test_color_error(self):
        """Box with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            box = aframexr.Box(color=not_an_string)
            box.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_environment_error(self):
        """Scene creation with invalid personalized environment."""
        environment = 'bad_environment'
        box = aframexr.Box()
        with self.assertRaises(ValueError) as error:
            # noinspection PyTypeChecker
            box.to_html(environment=environment)
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENVIRONMENT'].format(environment=environment))
