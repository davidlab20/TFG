import aframexr
import unittest
from typing import Literal, get_args

from aframexr.utils.constants import AVAILABLE_ENVIRONMENTS, ERROR_MESSAGES
from .constants import *


ALIGNS = Literal['center', 'left', 'right']
TEXT_CONTENT = 'aframexr'


class TestTextOK(unittest.TestCase):
    """Tests for text creation."""

    def test_simple(self):
        """Simple text creation."""
        text = aframexr.Text(value=TEXT_CONTENT)
        text.to_html()

    def test_from_dict(self):
        """Text creation using form_dict() method."""
        text = aframexr.Text.from_dict(aframexr.Text(value=TEXT_CONTENT).to_dict())
        text.to_html()

    def test_from_json(self):
        """Text creation using form_json() method."""
        text = aframexr.Text.from_json(aframexr.Text(value=TEXT_CONTENT).to_json())
        text.to_html()

    def test_align(self):
        """Text with specific align creation."""
        for a in get_args(ALIGNS):
            text = aframexr.Text(value=TEXT_CONTENT, align=a)
            text.to_html()

    def test_color(self):
        """Text with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            text = aframexr.Text(value=TEXT_CONTENT, color=c)
            text.to_html()

    def test_position(self):
        """Text with specific position creation."""
        for p in POSITIONS + POSITION_FORMATS:
            text = aframexr.Text(value=TEXT_CONTENT, position=p)
            text.to_html()

    def test_rotation(self):
        """Text with specific rotation creation."""
        for r in ROTATIONS + ROTATION_FORMATS:
            text = aframexr.Text(value=TEXT_CONTENT, rotation=r)
            text.to_html()

    def test_scale(self):
        """Text with specific scale creation."""
        for s in MARK_GLTF_SCALES:
            text = aframexr.Text(value=TEXT_CONTENT, scale=s)
            text.to_html()

    def test_all_parameters(self):
        """Text creation with all parameters specified."""
        for a, c, p, r, s in zip(get_args(ALIGNS), SIMPLE_ELEMENTS_COLORS, POSITIONS, ROTATIONS, MARK_GLTF_SCALES):
            text = aframexr.Text(value=TEXT_CONTENT, align=a, color=c, position=p, rotation=r, scale=s)
            text.to_html()

    def test_concatenation(self):
        """Concatenation of simple texts."""
        concatenated_chart = aframexr.Text(value=TEXT_CONTENT, position=CONCATENATION_POSITIONS[0])
        for p in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Text(value=TEXT_CONTENT, position=p)
        concatenated_chart.to_html()

    def test_environment(self):
        """Scene creation with personalized environment."""
        for e in AVAILABLE_ENVIRONMENTS:
            aframexr.Text(value=TEXT_CONTENT).to_html(environment=e)


class TestTextERROR(unittest.TestCase):
    """Tests for text creation error."""

    def test_align_error(self):
        """Text with specific align creation error."""
        incorrect_align = 'not_correct'
        with self.assertRaises(ValueError) as error:
            # noinspection PyTypeChecker
            text = aframexr.Text(value=TEXT_CONTENT, align=incorrect_align)
            text.to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ALIGN'].format(align=incorrect_align))

    def test_color_error(self):
        """Text with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            text = aframexr.Text(value=TEXT_CONTENT, color=not_an_string)
            text.to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_scale_error(self):
        """Text with specific scale creation error."""
        for s in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                text = aframexr.Text(value=TEXT_CONTENT, scale=s)
                text.to_html()
            self.assertEqual(
                str(error.exception),
                ERROR_MESSAGES['NOT_3_AXES_POSITION_OR_ROTATION'].format(
                    pos_or_rot='specs.scale', pos_or_rot_value=s
                )
            )

    def test_environment_error(self):
        """Scene creation with invalid personalized environment."""
        environment = 'bad_environment'
        text = aframexr.Text(value=TEXT_CONTENT)
        with self.assertRaises(ValueError) as error:
            # noinspection PyTypeChecker
            text.to_html(environment=environment)
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENVIRONMENT'].format(environment=environment))
