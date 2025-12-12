"""AframeXR encoding classes"""

from typing import Union

from aframexr.utils.constants import AVAILABLE_ENCODING_TYPES
from aframexr.utils.validators import AframeXRValidator


class Encoding:
    """Encoding base class."""

    _field: str = None
    _aggregate: str | None = None
    _axis: bool | None = True
    _encoding_type: str | None = None
    _groupby: list | None = None

    def __init__(self):
        AframeXRValidator.validate_type(self._field, str)

        AframeXRValidator.validate_type(self._aggregate, Union[str | None])
        if self._aggregate: AframeXRValidator.validate_aggregate_operation(self._aggregate)  # Validate if defined

        AframeXRValidator.validate_type(self._axis, Union[bool | None])

        AframeXRValidator.validate_type(self._encoding_type, Union[str | None])
        if self._encoding_type: AframeXRValidator.validate_encoding_type(self._encoding_type)  # Validate if defined

        AframeXRValidator.validate_type(self._groupby, Union[list | None])

    # Export
    def to_dict(self):
        """Returns the dictionary specifications expression."""

        spec_dict = {}
        if self._field:
            spec_dict.update({'field': self._field})
        if self._aggregate:
            spec_dict.update({'aggregate': self._aggregate})
        if not self._axis:  # Add if it is not True (as True is the default)
            spec_dict.update({'axis': self._axis})
        if self._encoding_type:
            spec_dict.update({'encoding_type': self._encoding_type})
        if self._groupby:
            spec_dict.update({'group_by': self._groupby})

        return {f'{self.__class__.__name__.lower()}': spec_dict}

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
    X channel encoding class.

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

    def __init__(self, field: str, aggregate: str | None = None, axis: bool | None = True,
                 encoding_type: str | None = None, groupby: list | None = None):
        self._field = field
        self._aggregate = aggregate
        self._axis = axis
        self._encoding_type = encoding_type
        self._groupby = groupby

        super().__init__()


class Y(Encoding):
    """
    Y channel encoding class.

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

    def __init__(self, field: str, aggregate: str | None = None, axis: bool | None = True,
                 encoding_type: str | None = None, groupby: list | None = None):
        self._field = field
        self._aggregate = aggregate
        self._axis = axis
        self._encoding_type = encoding_type
        self._groupby = groupby

        super().__init__()


class Z(Encoding):
    """
    Z channel encoding class.

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

    def __init__(self, field: str, aggregate: str | None = None, axis: bool | None = True,
                 encoding_type: str | None = None, groupby: list | None = None):
        self._field = field
        self._aggregate = aggregate
        self._axis = axis
        self._encoding_type = encoding_type
        self._groupby = groupby

        super().__init__()
