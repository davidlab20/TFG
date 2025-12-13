"""AframeXR filters"""

import polars as pl
from polars import DataFrame

from aframexr.utils.validators import AframeXRValidator


class FilterTransform:
    """FilterTransform base class."""

    def __init__(self, field: str, operator: str, value: str | float):
        self.field = field
        self.operator = operator
        self.value = value
        self._magic_method: str = ''  # Will be filled by child classes with its method (e.g. __eq__)

    # Exporting equation formats
    def equation_to_dict(self):
        """Returns a dictionary about the equation of the filter with the syntaxis of the JSON specifications."""

        return {'filter': f'datum.{self.field} {self.operator} {self.value}'}

    def equation_to_string(self):
        """Returns a string representation about the equation of the filter."""

        return f'{self.field} {self.operator} {self.value}'

    # Creating filters
    @staticmethod
    def from_string(equation: str):
        """
        Creates a child filter object from the given equation.

        Parameters
        ----------
        equation : str
            Equation to parse.

        Raises
        ------
        TypeError
            If equation is not a string.
        ValueError
            If the equation of the filter is not correct.

        Notes
        -----
        Suppose equation is a string for posterior calls of from_string of child filters.
        """

        AframeXRValidator.validate_type(equation, str)
        if '==' in equation:  # Equation is of type field == value
            return FieldEqualPredicate.from_string(equation)
        if '>' in equation:  # Equation is of type field > value
            return FieldGTPredicate.from_string(equation)
        if '<' in equation:  # Equation is of type field < value
            return FieldLTPredicate.from_string(equation)
        else:
            raise ValueError(f'There is no filter for equation: {equation}.')

    # Filter data
    def get_filtered_data(self, data: DataFrame) -> DataFrame:
        """Filters and returns the data."""

        if not self._magic_method:  # Should never enter here
            raise RuntimeError('Magic method was not defined.')

        try:
            condition = getattr(pl.col(self.field), self._magic_method)(self.value)
            filtered_data = data.filter(condition)
        except pl.exceptions.ColumnNotFoundError:
            raise KeyError(f'Data has no field "{self.field}".')
        return filtered_data


class FieldEqualPredicate(FilterTransform):
    """Equal predicate filter class."""

    def __init__(self, field: str, equal: str | float):
        operator = '=='
        super().__init__(field, operator, equal)
        self._magic_method = '__eq__'  # Magic method

    @staticmethod
    def from_string(equation: str):
        """
        Creates a FieldEqualPredicate from the equation string receiving.

        Parameters
        ----------
        equation : str
            Equation to parse.

        Raises
        ------
        SyntaxError
            If equation has an incorrect syntax.

        Notes
        -----
        Should receive equation as a string (as it has been called from FilterTransform).
        """

        if len(equation.split('==')) != 2:
            raise SyntaxError('Incorrect syntax, must be datum.{field} == {value}')
        field = equation.split('==')[0].strip()

        if not 'datum.' in field:  # The word 'datum.' is not in the field
            raise SyntaxError('Incorrect syntax, must be datum.{field} == {value}')
        field = field.replace('datum.', '')  # Delete the 'datum.' part of the field
        value = equation.split('==')[1].strip()
        try:
            value = int(value) if int(value) == float(value) else float(value)  # Try to convert value into a number
        except ValueError:
            pass  # Remain value as string

        return FieldEqualPredicate(field, value)


class FieldGTPredicate(FilterTransform):
    """Greater than predicate filter class."""

    def __init__(self, field: str, gt: float):
        operator = '>'
        super().__init__(field, operator, gt)
        self._magic_method = '__gt__'  # Magic method

    @staticmethod
    def from_string(equation: str):
        """
        Creates a FieldGTPredicate from the equation string receiving.

        Parameters
        ----------
        equation : str
            Equation to parse.

        Raises
        ------
        SyntaxError
            If equation has an incorrect syntax.

        Notes
        -----
        Should receive equation as a string (as it has been called from FilterTransform).
        """

        if len(equation.split('>')) != 2:
            raise SyntaxError('Incorrect syntax, must be datum.{field} > {value}')
        field = equation.split('>')[0].strip()

        if not 'datum.' in field:  # The word 'datum.' is not in the field
            raise SyntaxError('Incorrect syntax, must be datum.{field} > {value}')
        field = field.replace('datum.', '')  # Delete the 'datum.' part of the field
        value = float(equation.split('>')[1].strip())
        if int(value) == float(value):
            value = int(value)

        return FieldGTPredicate(field, value)


class FieldLTPredicate(FilterTransform):
    """Lower than predicate filter class."""

    def __init__(self, field: str, lt: float):
        operator = '<'
        super().__init__(field, operator, lt)
        self._magic_method = '__lt__'  # Magic method

    @staticmethod
    def from_string(equation: str):
        """
        Creates a FieldLTPredicate from the equation string receiving.

        Parameters
        ----------
        equation : str
            Equation to parse.

        Raises
        ------
        SyntaxError
            If equation has an incorrect syntax.

        Notes
        -----
        Should receive equation as a string (as it has been called from FilterTransform).
        """

        if len(equation.split('<')) != 2:
            raise SyntaxError('Incorrect syntax, must be datum.{field} < {value}')
        field = equation.split('<')[0].strip()

        if not 'datum.' in field:  # The word 'datum.' is not in the field
            raise SyntaxError('Incorrect syntax, must be datum.{field} < {value}')
        field = field.replace('datum.', '')  # Delete the 'datum.' part of the field
        value = float(equation.split('<')[1].strip())
        if int(value) == float(value):
            value = int(value)

        return FieldLTPredicate(field, value)
