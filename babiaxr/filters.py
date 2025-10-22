"""BabiaXR filters"""

from abc import abstractmethod, ABC


class Filter(ABC):
    """Filter base class."""
    def __init__(self, field: str, predicate: float):
        self.field = field
        self.predicate = predicate

    @abstractmethod
    def equation(self):
        """Returns the equation of the filter."""

        pass  # Must be implemented by child class



class FieldEqualPredicate(Filter):
    """Equal predicate filter class."""

    def __init__(self, field: str, equal: float):
        super().__init__(field, equal)

    def equation(self):
        """Returns the equation of the filter."""

        return f'{self.field}={self.predicate}'
