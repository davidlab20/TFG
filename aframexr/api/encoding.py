"""AframeXR encoding clases"""

from abc import ABC, abstractmethod


class Encoding(ABC):
    """Encoding base class."""

    # Import
    @staticmethod
    @abstractmethod
    def from_dict(spec_dict: dict):
        pass  # Must be implemented by child classes

    # Export
    @abstractmethod
    def to_dict(self):
        pass  # Must be implemented by child classes


class X(Encoding):
    """
    X-axis encoding class.

    Parameters
    ----------
    shorthand : str
        The data field of the axis.
    axis : bool | None (optional)
        If the axis line is visible or not. Default is True (visible).
    """

    def __init__(self, shorthand: str, axis: bool | None = True):
        if not isinstance(shorthand, str):
            raise TypeError(f'Expected str, got {type(shorthand).__name__} instead.')
        self.shorthand = shorthand
        if not isinstance(axis, bool | None):
            raise TypeError(f'Expected bool | None, got {type(axis).__name__} instead.')
        self.axis = axis

    # Import
    @staticmethod
    def from_dict(spec_dict: dict):
        """Returns the X object from the specification dictionary."""

        if not isinstance(spec_dict, dict):
            raise TypeError(f'Expected dict, got {type(spec_dict).__name__} instead.')
        field = spec_dict['x'].get('field')
        axis = spec_dict['x'].get('axis')
        return X(field, axis)

    # Export
    def to_dict(self):
        """Returns the dictionary specifications expression."""

        spec_dict = {'x': {}}
        if self.shorthand:
            spec_dict['x']['field'] = self.shorthand
        if not self.axis:  # Add if it is not True (as True is the default)
            spec_dict['x']['axis'] = self.axis
        return spec_dict


class Y(Encoding):
    """
    Y-axis encoding class.

    Parameters
    ----------
    shorthand : str
        The data field of the axis.
    axis : bool | None (optional)
        If the axis line is visible or not. Default is True (visible).
    """

    def __init__(self, shorthand: str, axis: bool | None = True):
        if not isinstance(shorthand, str):
            raise TypeError(f'Expected str, got {type(shorthand).__name__} instead.')
        self.shorthand = shorthand
        if not isinstance(axis, bool | None):
            raise TypeError(f'Expected bool | None, got {type(axis).__name__} instead.')
        self.axis = axis

    # Import
    @staticmethod
    def from_dict(spec_dict: dict):
        """Returns the Y object from the specification dictionary."""

        if not isinstance(spec_dict, dict):
            raise TypeError(f'Expected dict, got {type(spec_dict).__name__} instead.')
        field = spec_dict['y'].get('field')
        axis = spec_dict['y'].get('axis')
        return Y(field, axis)

    # Export
    def to_dict(self):
        """Returns the dictionary specifications expression."""

        spec_dict = {'y': {}}
        if self.shorthand:
            spec_dict['y']['field'] = self.shorthand
        if not self.axis:  # Add if it is not True (as True is the default)
            spec_dict['y']['axis'] = self.axis
        return spec_dict
