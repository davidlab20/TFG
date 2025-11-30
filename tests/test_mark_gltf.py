import aframexr
import unittest

from tests.constants import *

DATA = aframexr.URLData('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/refs/heads/main/Models/'
                        'AntiqueCamera/glTF/AntiqueCamera.gltf')


class TestMarkGLTFOK(unittest.TestCase):
    """Mark GLTF OK tests."""

    def test_simple(self):
        """Simple GLTF creation."""

        aframexr.Chart(DATA).mark_gltf().show()

    def test_position(self):
        """GLTF changing position creation."""

        for p in POSITIONS:
            aframexr.Chart(DATA, position=p).mark_gltf().show()

    def test_position_format(self):
        """GLTF changing position format creation."""

        for p in POSITION_FORMATS:
            aframexr.Chart(DATA, position=p).mark_gltf().show()

    def test_rotation(self):
        """GLTF changing rotation creation."""

        for r in ROTATIONS:
            aframexr.Chart(DATA, rotation=r).mark_gltf().show()

    def test_rotation_format(self):
        """GLTF changing rotation format creation."""

        for r in ROTATION_FORMATS:
            aframexr.Chart(DATA, rotation=r).mark_gltf().show()

    def test_scale(self):
        """GLTF changing scale creation."""

        for s in MARK_GLTF_SCALES:
            aframexr.Chart(DATA).mark_gltf(scale=s).show()

    def test_position_rotation_scale(self):
        """GLTF changing position, rotation and scale creation."""

        for p, r, s in zip(POSITIONS, ROTATIONS, MARK_GLTF_SCALES):
            aframexr.Chart(DATA, position=p, rotation=r).mark_gltf(scale=s).show()


class TestMarkGLTFError(unittest.TestCase):
    """Mark GLTF error tests."""

    def test_position_error(self):
        """Mark GLTF position error."""

        for p in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_gltf()
            assert str(error.exception) == f'The position: {p} is not correct. Must be "x y z".'

        for p in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_gltf()
            assert str(error.exception) == 'The position values must be numeric.'

    def test_rotation_error(self):
        """Mark GLTF rotation error."""

        for r in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_gltf()
            assert str(error.exception) == f'The rotation: {r} is not correct. Must be "x y z".'

        for r in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_gltf()
            assert str(error.exception) == 'The rotation values must be numeric.'
