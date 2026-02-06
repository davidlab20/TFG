import aframexr
import unittest

from aframexr.utils.validators import ERROR_MESSAGES


class TestAframexrError(unittest.TestCase):
    """General ERROR tests."""
    def test_from_dict_error_validate_type(self):
        """Verify that the error is raised when using from_dict with no dictionary."""
        with self.assertRaises(TypeError) as error:
            invalid_specs = 'not_a_dict'
            # noinspection PyTypeChecker
            aframexr.Chart.from_dict(specs=invalid_specs)
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='specs', expected_type=dict.__name__, current_type=type(invalid_specs).__name__
            )
        )

    def test_data_has_not_field_data_url(self):
        """Verify that the error is raised when data has not field "data" or "url"."""
        with self.assertRaises(ValueError) as error:
            bad_data_specifications = {"data": {}, "mark": "bar", "encoding": {}}  # Same occurs with other marks
            aframexr.Chart.from_dict(bad_data_specifications).to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['DATA_AND_URL_NOT_IN_SPECS'])

    def test_data_of_invalid_type(self):
        """Verify that the error is raised when data has invalid type."""
        with self.assertRaises(TypeError) as error:
            err_data = 'invalid data type'
            aframexr.Chart(err_data)
        self.assertEqual(
            str(error.exception),
            ERROR_MESSAGES['TYPE'].format(
                param_name='data', expected_type='Data or URLData or DataFrame', current_type=type(err_data).__name__
            )
        )

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

    def test_there_is_no_filter_for_equation(self):
        """Verify that the error is raised when there is no filter for given equation."""
        invalid_equation = 'invalid_equation'
        with self.assertRaises(ValueError) as error:
            aframexr.Chart().transform_filter(invalid_equation)
        self.assertEqual(str(error.exception), f'There is no filter for equation: {invalid_equation}')

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
            aframexr.Chart.from_dict({'mark': ''}).show()  # Using show() to cover this method
        self.assertEqual(str(error.exception), ERROR_MESSAGES['DATA_NOT_IN_SPECS'])

    def test_invalid_chart_specifications_not_mark_element(self):
        """Verify that the error is raised when chart specifications do not have field "mark" or "element"."""
        with self.assertRaises(ValueError) as error:
            aframexr.Chart.from_dict({'neither_mark_or_element': ''}).to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['MARK_AND_ELEMENT_NOT_IN_SPECS'])

    def test_invalid_chart_type(self):
        """Verify that the error is raised when the chart type is invalid."""
        with self.assertRaises(ValueError) as error:
            bad_chart_type = 'bad_mark'
            aframexr.Chart.from_dict({'data': {'url': ''}, 'mark': bad_chart_type, 'encoding': ''}).to_html()
        self.assertEqual(str(error.exception), ERROR_MESSAGES['MARK_TYPE'].format(mark_type=bad_chart_type))

    def test_save_invalid_type_format(self):
        """Verify that the error is raised when the save type is invalid."""
        with self.assertRaises(ValueError) as error:
            bad_file_format = 'good_file.bad_format'
            aframexr.Chart().save(bad_file_format)
        self.assertEqual(str(error.exception), 'Invalid file format')
