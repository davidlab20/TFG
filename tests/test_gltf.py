import aframexr
import unittest

from tests.constants import *

URL = ('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/refs/heads/main/Models/AntiqueCamera/'
        'glTF/AntiqueCamera.gltf')


class TestMarkGLTFOK(unittest.TestCase):
    """Mark GLTF OK tests."""
    def test_simple(self):
        """Simple GLTF creation."""
        aframexr.GLTF(URL).to_html()

    def test_simple_with_pandas_not_installed(self):
        """Simple GLTF creation without having pandas installed."""
        import sys
        import importlib
        from unittest import mock

        sys.modules.pop('aframexr', None)
        sys.modules.pop('aframexr.api.components', None)

        with mock.patch.dict(sys.modules, {'pandas': None}):
            import aframexr
            importlib.reload(aframexr)

            aframexr.GLTF(URL).to_html()

            import aframexr.api.components as components
            self.assertIsNone(components.pd)
            self.assertIs(components.DataFrame, object)

    def test_from_json(self):
        """GLTF using from_json() method creation."""
        json_string = aframexr.GLTF(URL).to_json()
        gltf_chart = aframexr.Chart.from_json(json_string)
        gltf_chart.to_html()

        self.assertEqual(gltf_chart.to_json(), json_string)

    def test_position(self):
        """GLTF changing position creation."""
        for p in POSITIONS:
            aframexr.GLTF(URL, position=p).to_html()

    def test_position_format(self):
        """GLTF changing position format creation."""
        for p in POSITION_FORMATS:
            aframexr.GLTF(URL, position=p).to_html()

    def test_rotation(self):
        """GLTF changing rotation creation."""
        for r in ROTATIONS:
            aframexr.GLTF(URL, rotation=r).to_html()

    def test_rotation_format(self):
        """GLTF changing rotation format creation."""
        for r in ROTATION_FORMATS:
            aframexr.GLTF(URL, rotation=r).to_html()

    def test_scale(self):
        """GLTF changing scale creation."""
        for s in MARK_GLTF_SCALES:
            aframexr.GLTF(URL, scale=s).to_html()

    def test_position_rotation_scale(self):
        """GLTF changing position, rotation and scale creation."""
        for p, r, s in zip(POSITIONS, ROTATIONS, MARK_GLTF_SCALES):
            aframexr.GLTF(URL, position=p, rotation=r, scale=s).to_html()

    def test_concatenation(self):
        """GLTF concatenation creation."""
        concatenated_chart = aframexr.GLTF(URL, position=CONCATENATION_POSITIONS[0])
        for pos in CONCATENATION_POSITIONS[1:]:
            concatenated_chart += aframexr.GLTF(URL, position=pos)

        concatenated_chart.to_html()

    def test_save(self):
        """GLTF saving."""
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_html_file_path = Path(tmpdir) / "test.html"
            temp_json_file_path = Path(tmpdir) / "test.json"

            gltf = aframexr.GLTF(URL)
            gltf.save(str(temp_html_file_path))
            gltf.save(str(temp_json_file_path))

            assert temp_html_file_path.exists()
            assert temp_json_file_path.exists()
