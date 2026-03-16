import aframexr
import unittest

from aframexr.utils.constants import AVAILABLE_ENVIRONMENTS, ERROR_MESSAGES
from .constants import *

START_END = {'start': '0 0 0', 'end': '1 1 1'}


class TestLineOK(unittest.TestCase):
    """Tests for simple line creation."""

    def test_simple(self):
        """Simple line creation."""
        line = aframexr.Line(**START_END)
        line.to_html()

    def test_from_dict(self):
        """Line creation using form_dict() method."""
        line = aframexr.Line.from_dict(aframexr.Line(**START_END).to_dict())
        line.to_html()

    def test_from_json(self):
        """Line creation using form_json() method."""
        line = aframexr.Line.from_json(aframexr.Line(**START_END).to_json())
        line.to_html()

    def test_color(self):
        """Line with specific color creation."""
        for c in SIMPLE_ELEMENTS_COLORS:
            line = aframexr.Line(**START_END, color=c)
            line.to_html()

    def test_concatenation(self):
        """Concatenation of simple lines."""
        concatenated_chart = aframexr.Line(**START_END) + aframexr.Line(**START_END)
        concatenated_chart.to_html()

    def test_environment(self):
        """Scene creation with personalized environment."""
        for e in AVAILABLE_ENVIRONMENTS:
            aframexr.Line(**START_END).to_html(environment=e)


class TestLineERROR(unittest.TestCase):
    """Tests for line creation errors."""

    def test_color_error(self):
        """Line with specific color creation error."""
        not_an_string = ['not a color']
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            aframexr.Line(**START_END, color=not_an_string).to_html()
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs.color', expected_type=str.__name__, current_type=type(not_an_string).__name__
            )
        )

    def test_environment_error(self):
        """Scene creation with invalid personalized environment."""
        environment = 'bad_environment'
        line = aframexr.Line(**START_END)
        with self.assertRaises(ValueError) as error:
            # noinspection PyTypeChecker
            line.to_html(environment=environment)
        self.assertEqual(str(error.exception), ERROR_MESSAGES['ENVIRONMENT'].format(environment=environment))
