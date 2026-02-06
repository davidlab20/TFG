import aframexr
import unittest


class TestBoxOK(unittest.TestCase):
    """Tests for simple box creation."""

    def test_simple(self):
        """Simple box creation."""
        box = aframexr.Box()
        box.to_html()

    def test_from_json(self):
        """Box creation using form_json() method."""
        box = aframexr.Box.from_json(aframexr.Box().to_json())
        box.to_html()

    def test_color(self):
        """Box with specific color creation."""
        box = aframexr.Box(color='red')
        box.to_html()
