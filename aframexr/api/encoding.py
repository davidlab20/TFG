"""AframeXR encoding classes"""

from abc import ABC, abstractmethod
from typing import Union

from aframexr.utils.constants import AVAILABLE_ENCODING_TYPES
from aframexr.utils.validators import AframeXRValidator


class Encoding(ABC):
    """Encoding base class."""

    # Export
    @abstractmethod
    def to_dict(self):
        pass  # Must be implemented by child classes

    # Utils
    @staticmethod
    def split_field_and_encoding(param: str) -> tuple[str, str | None]:
        """
        Splits and returns the field and the encoding data type of the parameter.

        Raises
        ------
        TypeError
            If the encoding type is incorrect.

        Notes
        -----
        Supposing that param is a string, as it has been called from encode() method.
        """

        param_parts = param.split(':')  # Split parameter in field:encoding_type
        if len(param_parts) == 1:  # No encoding data type is specified
            return param, None
        if len(param_parts) == 2:
            field = param_parts[0]
            encoding_type = param_parts[1].upper()  # Convert to upper case (to accept lower case also)
            AframeXRValidator.validate_encoding_type(encoding_type)
            return field, AVAILABLE_ENCODING_TYPES[encoding_type]
        else:
            raise ValueError(f'Invalid encoding type: {param}.')


class X(Encoding):
    """
    X-axis encoding class.

    Parameters
    ----------
    field : str
        The data field of the axis.
    aggregate : bool | None (optional)
        Type of transformation in the field data.
    axis : bool | None (optional)
        If the axis line is visible or not. Default is True (visible).
    encoding_type : str | None (optional)
        The encoding type.
    group_by : str | None (optional)
        The grouping key to use for the encoding.
    """

    def __init__(self, field: str, aggregate: str | None = None, axis: bool | None = True,
                 encoding_type: str | None = None, group_by: str | None = None):
        AframeXRValidator.validate_type(field, str)
        self.field = field

        AframeXRValidator.validate_type(aggregate, Union[str | None])
        AframeXRValidator.validate_aggregate_operation(aggregate)
        self.aggregate = aggregate

        AframeXRValidator.validate_type(axis, Union[bool | None])
        self.axis = axis

        AframeXRValidator.validate_type(encoding_type, Union[str | None])
        AframeXRValidator.validate_encoding_type(encoding_type)
        self.encoding_type = encoding_type

        AframeXRValidator.validate_type(group_by, str)
        self.group_by = group_by

    # Export
    def to_dict(self):
        """Returns the dictionary specifications expression."""

        spec_dict = {'x': {}}
        if self.field:
            spec_dict['x']['field'] = self.field
        if self.aggregate:
            spec_dict['x']['aggregate'] = self.aggregate
        if not self.axis:  # Add if it is not True (as True is the default)
            spec_dict['x']['axis'] = self.axis
        if self.encoding_type:
            spec_dict['x']['encoding_type'] = self.encoding_type
        if self.group_by:
            spec_dict['x']['group_by'] = self.group_by
        return spec_dict


class Y(Encoding):
    """
    Y-axis encoding class.

    Parameters
    ----------
    field : str
        The data field of the axis.
    aggregate : bool | None (optional)
        Type of transformation in the field data.
    axis : bool | None (optional)
        If the axis line is visible or not. Default is True (visible).
    encoding_type : str | None (optional)
        The encoding type.
    group_by : str | None (optional)
        The grouping key to use for the encoding.
    """

    def __init__(self, field: str, aggregate: str | None = None, axis: bool | None = True,
                 encoding_type: str | None = None, group_by: str | None = None):
        AframeXRValidator.validate_type(field, str)
        self.field = field

        AframeXRValidator.validate_type(aggregate, Union[str | None])
        AframeXRValidator.validate_aggregate_operation(aggregate)
        self.aggregate = aggregate

        AframeXRValidator.validate_type(axis, Union[bool | None])
        self.axis = axis

        AframeXRValidator.validate_type(encoding_type, Union[str | None])
        AframeXRValidator.validate_encoding_type(encoding_type)
        self.encoding_type = encoding_type

        AframeXRValidator.validate_type(group_by, str)
        self.group_by = group_by

    # Export
    def to_dict(self):
        """Returns the dictionary specifications expression."""

        spec_dict = {'y': {}}
        if self.field:
            spec_dict['y']['field'] = self.field
        if self.aggregate:
            spec_dict['y']['aggregate'] = self.aggregate
        if not self.axis:  # Add if it is not True (as True is the default)
            spec_dict['y']['axis'] = self.axis
        if self.encoding_type:
            spec_dict['y']['encoding_type'] = self.encoding_type
        if self.group_by:
            spec_dict['y']['group_by'] = self.group_by
        return spec_dict


class Z(Encoding):
    """
    Z-axis encoding class.

    Parameters
    ----------
    field : str
        The data field of the axis.
    aggregate : bool | None (optional)
        Type of transformation in the field data.
    axis : bool | None (optional)
        If the axis line is visible or not. Default is True (visible).
    encoding_type : str | None (optional)
        The encoding type.
    group_by : str | None (optional)
        The grouping key to use for the encoding.
    """

    def __init__(self, field: str, aggregate: str | None = None, axis: bool | None = True,
                 encoding_type: str | None = None, group_by: str | None = None):
        AframeXRValidator.validate_type(field, str)
        self.field = field

        AframeXRValidator.validate_type(aggregate, Union[str | None])
        AframeXRValidator.validate_aggregate_operation(aggregate)
        self.aggregate = aggregate

        AframeXRValidator.validate_type(axis, Union[bool | None])
        self.axis = axis

        AframeXRValidator.validate_type(encoding_type, Union[str | None])
        AframeXRValidator.validate_encoding_type(encoding_type)
        self.encoding_type = encoding_type

        AframeXRValidator.validate_type(group_by, str)
        self.group_by = group_by

    # Export
    def to_dict(self):
        """Returns the dictionary specifications expression."""

        spec_dict = {'z': {}}
        if self.field:
            spec_dict['z']['field'] = self.field
        if self.aggregate:
            spec_dict['z']['aggregate'] = self.aggregate
        if not self.axis:  # Add if it is not True (as True is the default)
            spec_dict['z']['axis'] = self.axis
        if self.encoding_type:
            spec_dict['z']['encoding_type'] = self.encoding_type
        return spec_dict
