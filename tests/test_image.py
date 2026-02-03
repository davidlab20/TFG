import aframexr
import unittest

from tests.constants import *

URL = 'https://davidlab20.github.io/TFG/imgs/logo.png'


class TestMarkImageOK(unittest.TestCase):
    """Mark image OK tests."""
    def test_simple(self):
        """Simple image creation."""
        aframexr.Image(URL).to_html()

    def test_simple_with_pandas_not_installed(self):
        """Simple image creation without having pandas installed."""
        import sys
        import importlib
        from unittest import mock

        sys.modules.pop('aframexr', None)
        sys.modules.pop('aframexr.api.components', None)

        with mock.patch.dict(sys.modules, {'pandas': None}):
            import aframexr
            importlib.reload(aframexr)

            aframexr.Image(URL).to_html()

            import aframexr.api.components as components
            self.assertIsNone(components.pd)
            self.assertIs(components.DataFrame, object)

    def test_from_json(self):
        """Image using from_json() method creation."""
        json_string = aframexr.Image(URL).to_json()
        image_chart = aframexr.Chart.from_json(json_string)
        image_chart.to_html()

        self.assertTrue(image_chart.to_json() == json_string)

    def test_position(self):
        """Image changing position creation."""
        for p in POSITIONS:
            aframexr.Image(URL, position=p).to_html()

    def test_position_format(self):
        """Image changing position format creation."""
        for p in POSITION_FORMATS:
            aframexr.Image(URL, position=p).to_html()

    def test_rotation(self):
        """Image changing rotation creation."""
        for r in ROTATIONS:
            aframexr.Image(URL, rotation=r).to_html()

    def test_rotation_format(self):
        """Image changing rotation format creation."""
        for r in ROTATION_FORMATS:
            aframexr.Image(URL, rotation=r).to_html()

    def test_width(self):
        """Image changing width creation."""
        for w in MARK_IMAGE_WIDTHS_HEIGHTS:
            aframexr.Image(URL, width=w).to_html()

    def test_height(self):
        """Image changing height creation."""
        for h in MARK_IMAGE_WIDTHS_HEIGHTS:
            aframexr.Image(URL, height=h).to_html()

    def test_position_rotation_width_height(self):
        """Image changing position, rotation, width and height creation."""
        for p, r, w, h in zip(POSITIONS, ROTATIONS, MARK_IMAGE_WIDTHS_HEIGHTS, MARK_IMAGE_WIDTHS_HEIGHTS):
            aframexr.Image(URL, position=p, rotation=r, width=w, height=h).to_html()

    def test_concatenation(self):
        """Image concatenation creation."""
        concatenated_chart = aframexr.Image(URL, position=CONCATENATION_POSITIONS[0])
        for pos in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.Image(URL, position=pos)

        concatenated_chart.to_html()
