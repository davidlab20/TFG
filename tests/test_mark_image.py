import aframexr
import unittest

from tests.constants import *

DATA = aframexr.URLData('https://davidlab20.github.io/TFG/imgs/logo.png')


class TestMarkImageOK(unittest.TestCase):
    """Mark image OK tests."""

    def test_simple(self):
        """Simple image creation."""

        aframexr.Chart(DATA).mark_image().show()

    def test_position(self):
        """Image changing position creation."""

        for p in POSITIONS:
            aframexr.Chart(DATA, position=p).mark_image().show()

    def test_position_format(self):
        """Image changing position format creation."""

        for p in POSITION_FORMATS:
            aframexr.Chart(DATA, position=p).mark_image().show()

    def test_rotation(self):
        """Image changing rotation creation."""

        for r in ROTATIONS:
            aframexr.Chart(DATA, rotation=r).mark_image().show()

    def test_rotation_format(self):
        """Image changing rotation format creation."""

        for r in ROTATION_FORMATS:
            aframexr.Chart(DATA, rotation=r).mark_image().show()

    def test_width(self):
        """Image changing width creation."""

        for w in MARK_IMAGE_WIDTHS_HEIGHTS:
            aframexr.Chart(DATA).mark_image(width=w).show()

    def test_height(self):
        """Image changing height creation."""

        for h in MARK_IMAGE_WIDTHS_HEIGHTS:
            aframexr.Chart(DATA).mark_image(height=h).show()

    def test_position_rotation_width_height(self):
        """Image changing position, rotation, width and height creation."""

        for p, r, w, h in zip(POSITIONS, ROTATIONS, MARK_IMAGE_WIDTHS_HEIGHTS, MARK_IMAGE_WIDTHS_HEIGHTS):
            aframexr.Chart(DATA, position=p, rotation=r).mark_image(width=w, height=h).show()


class TestMarkImageError(unittest.TestCase):
    """Mark image error tests."""

    def test_position_error(self):
        """Mark image position error."""

        for p in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_image()
            assert str(error.exception) == f'The position: {p} is not correct. Must be "x y z".'

        for p in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, position=p).mark_image()
            assert str(error.exception) == 'The position values must be numeric.'

    def test_rotation_error(self):
        """Mark image rotation error."""

        for r in NOT_3AXIS_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_image()
            assert str(error.exception) == f'The rotation: {r} is not correct. Must be "x y z".'

        for r in NOT_NUMERIC_POSITIONS_ROTATIONS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA, rotation=r).mark_image()
            assert str(error.exception) == 'The rotation values must be numeric.'

    def test_width_error(self):
        """Mark image width error."""

        for w in NOT_GREATER_THAN_0_MARK_IMAGE_WIDTHS_HEIGHTS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_image(width=w)
            assert str(error.exception) == 'The width must be greater than 0.'

    def test_height_error(self):
        """Mark image height error."""

        for h in NOT_GREATER_THAN_0_MARK_IMAGE_WIDTHS_HEIGHTS:
            with self.assertRaises(ValueError) as error:
                aframexr.Chart(DATA).mark_image(height=h)
            assert str(error.exception) == 'The height must be greater than 0.'
