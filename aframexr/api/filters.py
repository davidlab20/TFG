"""AframeXR filters"""

class FilterTransform:
    """FilterTransform base class."""

    def __init__(self, field: str, operator: str, value: str | float):
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

        Notes
        -----
        Suppose equation is a string for posterior calls of from_string of child filters.
        """

        if not isinstance(equation, str):
            raise TypeError(f'The equation must be a string, got {type(equation).__name__}')
        if '=' in equation:  # Equation is of type field=value
            return FieldEqualPredicate.from_string(equation)
        if '>' in equation:  # Equation is of type field>value
            return FieldGTPredicate.from_string(equation)
        if '<' in equation:  # Equation is of type field<value
            return FieldLTPredicate.from_string(equation)
        else:
            raise NotImplementedError(f'The filter for equation "{equation}" is not implemented yet.')


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

        if len(equation.split('=')) != 2:
            raise SyntaxError('Incorrect syntax, must be datum.{field}={value}')
        field = equation.split('=')[0].strip()

        if not 'datum.' in field:  # The word 'datum.' is not in the field
            raise SyntaxError('Incorrect syntax, must be datum.{field}={value}')
        field = field.replace('datum.', '')  # Delete the 'datum.' part of the field
        value = equation.split('=')[1].strip()

        return FieldEqualPredicate(field, value)

    # Filtering data
    def get_filtered_data(self, raw_data: list[dict]) -> list[dict]:
        """
        Returns the filtered data.

        Notes
        -----
        Supposing that raw_data is a dict (as it has been called from FilterTransform).
        """

        return [d for d in raw_data if d[self.field] == self.value]


class FieldGTPredicate(FilterTransform):
    """Greater than predicate filter class."""

    def __init__(self, field: str, gt: float):
        operator = '>'
        super().__init__(field, operator, gt)

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
            raise SyntaxError('Incorrect syntax, must be datum.{field}>{value}')
        field = equation.split('>')[0].strip()

        if not 'datum.' in field:  # The word 'datum.' is not in the field
            raise SyntaxError('Incorrect syntax, must be datum.{field}>{value}')
        field = field.replace('datum.', '')  # Delete the 'datum.' part of the field
        value = float(equation.split('>')[1].strip())

        return FieldGTPredicate(field, value)

    # Filtering data
    def get_filtered_data(self, raw_data: list[dict]) -> list[dict]:
        """
        Returns the filtered data.

        Notes
        -----
        Supposing that raw_data is a dict (as it has been called from FilterTransform).
        """

        return [d for d in raw_data if d[self.field] > self.value]


class FieldLTPredicate(FilterTransform):
    """Lower than predicate filter class."""

    def __init__(self, field: str, lt: float):
        operator = '<'
        super().__init__(field, operator, lt)

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
            raise SyntaxError('Incorrect syntax, must be datum.{field}<{value}')
        field = equation.split('<')[0].strip()

        if not 'datum.' in field:  # The word 'datum.' is not in the field
            raise SyntaxError('Incorrect syntax, must be datum.{field}<{value}')
        field = field.replace('datum.', '')  # Delete the 'datum.' part of the field
        value = float(equation.split('<')[1].strip())

        return FieldLTPredicate(field, value)

    # Filtering data
    def get_filtered_data(self, raw_data: list[dict]) -> list[dict]:
        """
        Returns the filtered data.

        Notes
        -----
        Supposing that raw_data is a dict (as it has been called from FilterTransform).
        """

        return [d for d in raw_data if d[self.field] < self.value]
