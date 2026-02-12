"""AframeXR filters"""

import polars as pl
from abc import ABC, abstractmethod
from polars import DataFrame

from ..utils.validators import AframeXRValidator


OPERATOR_MAP: dict[str, type['FilterTransform']] = {}  # Operator map, classes are added at the end of this file


class FilterTransform(ABC):
    """FilterTransform base class."""
    _operator: str = ''
    _magic_method: str = ''  # Must be defined by child classes with its method (e.g. __eq__)

    @abstractmethod
    def __init__(self, field: str, value: str | float):
        self.field = field
        self.value = value

    # Exporting equation formats
    @abstractmethod
    def to_dict(self):
        """Returns a dictionary about the equation of the filter with the syntaxis of the JSON specifications."""

    # Creating filters
    @staticmethod
    def from_equation(equation: str):
        AframeXRValidator.validate_type('equation', equation, str)

        parts = equation.split()
        if len(parts) != 3:
            raise SyntaxError('Incorrect syntax, must be datum.{field} {operator} {value}')

        field, op, value = parts

        try:
            value = float(value)
        except ValueError:
            pass

        if op in OPERATOR_MAP:
            if not field.startswith('datum.'):
                raise SyntaxError('Incorrect syntax, must be datum.{field} {operator} {value}')
            return OPERATOR_MAP[op](field.removeprefix('datum.'), value)
        else:
            raise ValueError(f'There is no filter for equation: {equation}')

    @staticmethod
    def from_dict(filter_specs: dict):
        """
        Creates a child filter object from the given filter's specifications.

        Parameters
        ----------
        filter_specs : dict
            Filter specifications.

        Raises
        ------
        TypeError
            If equation is not a dictionary.
        ValueError
            If the specifications of the filter is not correct.

        Notes
        -----
        Suppose equation is a string for posterior calls of from_string of child filters.
        """
        AframeXRValidator.validate_type('equation', filter_specs, dict)

        if 'equal' in filter_specs:  # Equation is of type field == value
            return FieldEqualPredicate(filter_specs['field'], filter_specs['equal'])
        if 'gt' in filter_specs:  # Equation is of type field > value
            return FieldGTPredicate(filter_specs['field'], filter_specs['gt'])
        if 'lt' in filter_specs:  # Equation is of type field < value
            return FieldLTPredicate(filter_specs['field'], filter_specs['lt'])
        else:
            raise ValueError(f'There is no filter for specifications: {filter_specs}')

    # Filter data
    def get_filtered_data(self, data: DataFrame) -> DataFrame:
        """Filters and returns the data."""
        if not self._magic_method:  # pragma: no cover
            raise RuntimeError(f'Unreachable code. Magic method was not defined in {self.__class__.__name__} class')

        try:
            condition = getattr(pl.col(self.field), self._magic_method)(self.value)
            filtered_data = data.filter(condition)
        except pl.exceptions.ColumnNotFoundError:
            raise KeyError(f'Data has no field "{self.field}".')
        return filtered_data


class FieldEqualPredicate(FilterTransform):
    """Equal predicate filter class."""

    def __init__(self, field: str, equal: str | float):
        self._operator = '=='
        self._magic_method = '__eq__'  # Magic method
        super().__init__(field, equal)

    def to_dict(self):
        return {'field': self.field, 'equal': self.value}


class FieldGTPredicate(FilterTransform):
    """Greater than predicate filter class."""

    def __init__(self, field: str, gt: float):
        self._operator = '>'
        self._magic_method = '__gt__'  # Magic method
        super().__init__(field, gt)

    def to_dict(self):
        return {'field': self.field, 'gt': self.value}


class FieldLTPredicate(FilterTransform):
    """Lower than predicate filter class."""

    def __init__(self, field: str, lt: float):
        self._operator = '<'
        self._magic_method = '__lt__'  # Magic method
        super().__init__(field, lt)

    def to_dict(self):
        return {'field': self.field, 'lt': self.value}


# Add classes to OPERATOR_MAP
OPERATOR_MAP.update({
    '==': FieldEqualPredicate,
    '>': FieldGTPredicate,
    '<': FieldLTPredicate,
})
