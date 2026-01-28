import aframexr
import unittest


class TestAframexrError(unittest.TestCase):
    """General ERROR tests."""
    def test_from_dict_error_validate_type(self):
        """Verify that the error is raised when using from_dict with no dictionary."""
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            aframexr.Chart.from_dict('not_a_dict')
        assert str(error.exception) == f'Expected {dict.__name__}, got {str.__name__} instead.'

    def test_add_error_not_isinstance_TopLevelMixin(self):
        """Verify that the error is raised when adding one chart to other thing."""
        with self.assertRaises(TypeError) as error:
            one = aframexr.Chart(aframexr.URLData(''))
            other = 2
            one + other
        assert str(error.exception) == f"Cannot add {type(other).__name__} to {type(one).__name__}."
