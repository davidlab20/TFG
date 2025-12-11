"""AframeXR encoding classes"""

from typing import Union

from aframexr.utils.constants import AVAILABLE_ENCODING_TYPES
from aframexr.utils.validators import AframeXRValidator


class Encoding:
    """
    Encoding base class.

    Parameters
    ----------
    field: str
        The name of the data field to encode.
    aggregate: str | None (optional)
        The aggregate operation.
    axis: bool | None (optional)
        If the axis is displayed or not, default is set to True (show axis).
    encoding_type: str | None (optional)
        The encoding type.
    groupby: list | None (optional)
        The fields of the aggrupation.
    """

    _encoding_channel_name = ''  # Will be filled by child classes when calling to to_dict() method

    def __init__(self, field: str, aggregate: str | None = None, axis: bool | None = True,
                 encoding_type: str | None = None, groupby: list | None = None):
        AframeXRValidator.validate_type(field, str)
        self.field = field

        AframeXRValidator.validate_type(aggregate, Union[str | None])
        if aggregate: AframeXRValidator.validate_aggregate_operation(aggregate)  # Only validate if it is not None
        self.aggregate = aggregate

        AframeXRValidator.validate_type(axis, Union[bool | None])
        self.axis = axis

        AframeXRValidator.validate_type(encoding_type, Union[str | None])
        if encoding_type: AframeXRValidator.validate_encoding_type(encoding_type)  # Only validate if it is not None
        self.encoding_type = encoding_type

        AframeXRValidator.validate_type(groupby, Union[list | None])
        self.groupby = groupby

    # Export
    def to_dict(self):
        """Returns the dictionary specifications expression."""

        if not self._encoding_channel_name:  # Should never happen
            raise RuntimeError(f'Encoding channel was not defined, must have be done by: {self.__class__.__name__}.')

        spec_dict = {}
        if self.field:
            spec_dict.update({'field': self.field})
        if self.aggregate:
            spec_dict.update({'aggregate': self.aggregate})
        if not self.axis:  # Add if it is not True (as True is the default)
            spec_dict.update({'axis': self.axis})
        if self.encoding_type:
            spec_dict.update({'encoding_type': self.encoding_type})
        if self.groupby:
            spec_dict.update({'group_by': self.groupby})

        return {self._encoding_channel_name: spec_dict}

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
    _encoding_channel_name = 'x'  # Define the encoding channel name


class Y(Encoding):
    _encoding_channel_name = 'y'  # Define the encoding channel name


class Z(Encoding):
    _encoding_channel_name = 'z'  # Define the encoding channel name
