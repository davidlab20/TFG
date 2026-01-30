import aframexr
import unittest


class TestAframexrError(unittest.TestCase):
    """General ERROR tests."""
    def test_from_dict_error_validate_type(self):
        """Verify that the error is raised when using from_dict with no dictionary."""
        with self.assertRaises(TypeError) as error:
            # noinspection PyTypeChecker
            aframexr.Chart.from_dict('not_a_dict')
        self.assertEqual(str(error.exception), f'Expected {dict.__name__}, got {str.__name__} instead.')

    def test_data_has_not_field_data_url(self):
        """Verify that the error is raised when data has not field "data" or "url"."""
        with self.assertRaises(ValueError) as error:
            bad_data_specifications = {"data": {}, "mark": "bar", "encoding": {}}  # Same occurs with other marks
            aframexr.Chart.from_dict(bad_data_specifications).to_html()
        self.assertEqual(str(error.exception),
                         'Data specifications has no correct syntaxis, must have field "url" or "values".')

    def test_NULL_series(self):
        """Verify that the error is raised when having NULL series."""
        with self.assertRaises(ValueError) as error:
            data = [
                {"id": 1, "value": None},
                {"id": 2, "value": None},
                {"id": 3, "value": None}
            ]
            aframexr.Chart(aframexr.Data(data)).mark_bar().encode(x='id', y='value').to_html()
        self.assertEqual(str(error.exception), 'Unknown dtype: Null.')

    def test_add_error_not_isinstance_TopLevelMixin(self):
        """Verify that the error is raised when adding one chart to other thing."""
        with self.assertRaises(TypeError) as error:
            one = aframexr.Chart(aframexr.URLData(''))
            other = 2
            one + other
        self.assertEqual(str(error.exception), f"Cannot add {type(other).__name__} to {type(one).__name__}.")

    def test_invalid_chart_specifications_not_data_having_mark(self):
        """Verify that the error is raised when chart specifications do not have field "data" having mark type."""
        with self.assertRaises(ValueError) as error:
            aframexr.Chart.from_dict({'mark': ''}).to_html()
        self.assertEqual(str(error.exception), 'Invalid chart specifications. Must contain key "data".')

    def test_invalid_chart_specifications_not_mark_element(self):
        """Verify that the error is raised when chart specifications do not have field "mark" or "element"."""
        with self.assertRaises(ValueError) as error:
            aframexr.Chart.from_dict({'neither_mark_or_element': ''}).to_html()
        self.assertEqual(
            str(error.exception), f'Invalid chart specifications. Must contain key "mark" or "element".'
        )

    def test_invalid_chart_type(self):
        """Verify that the error is raised when the chart type is invalid."""
        with self.assertRaises(ValueError) as error:
            bad_chart_type = 'bad_mark'
            aframexr.Chart.from_dict({'data': '', 'mark': bad_chart_type, 'encoding': ''}).to_html()
        self.assertEqual(str(error.exception), f'Invalid chart type: {bad_chart_type}.')
