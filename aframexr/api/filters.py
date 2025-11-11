"""AframeXR filters"""

class FilterTransform:
    """FilterTransform base class."""

    def __init__(self, field: str, operator: str, value: str):
        self.field = field
        self.operator = operator
        self.value = value

    # Exporting equation formats
    def equation_to_dict(self):
        """Returns a dictionary about the equation of the filter with the syntaxis of the JSON specifications."""

        return {'filter': f'datum.{self.field}{self.operator}{self.value}'}

    def equation_to_string(self):
        """Returns a string representation about the equation of the filter."""

        return f'{self.field}{self.operator}{self.value}'

    # Creating filters
    @staticmethod
    def from_string(equation: str) -> 'FilterTransform':
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

        Notes
        -----
        Suppose equation is a string for posterior calls of from_string of child filters.
        """

        if not isinstance(equation, str):
            raise TypeError(f'The equation must be a string, got {type(equation).__name__}')
        if equation.find('=') != -1:  # Equation is of type field=value
            return FieldEqualPredicate.from_string(equation)
        else:
            raise NotImplementedError(f'The filter for equation "{equation}" is not implemented yet.')

    # Filtering data
    def filter_data(self, raw_data: list[dict]) -> list[dict]:
        """Returns the filtered data."""

        if not isinstance(raw_data, list):
            raise TypeError(f'The raw_data must be a list[dict], got {type(raw_data).__name__}')
        if self.operator == '=':
            return FieldEqualPredicate.filter_data(FieldEqualPredicate(self.field, self.value), raw_data)
        else:
            raise NotImplementedError(f'The filter for equation "{self.equation_to_string()}" is not implemented yet.')


class FieldEqualPredicate(FilterTransform):
    """Equal predicate filter class."""

    def __init__(self, field: str, equal: str):
        operator = '='
        super().__init__(field, operator, equal)

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

        if len(equation.split('=')) != 2:  # The equation has more than 1 equal symbol
            raise SyntaxError('Incorrect syntax, must be datum.{field}={value}')
        field = equation.split('=')[0].strip()
        if field.find('datum.') == -1:  # The word 'datum.' is not in the field
            raise SyntaxError('Incorrect syntax, must be datum.{field}={value}')
        field = field.replace('datum.', '')  # Delete the 'datum.' part of the field
        equal = equation.split('=')[1].strip()
        return FieldEqualPredicate(field, equal)

    # Filtering data
    def filter_data(self, raw_data: list[dict]) -> list[dict]:
        """
        Returns the filtered data.

        Notes
        -----
        Supposing that raw_data is a dict (as it has been called from FilterTransform).
        """

        return [d for d in raw_data if d[self.field] == self.value]
