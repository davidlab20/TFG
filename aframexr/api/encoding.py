"""AframeXR encoding classes"""

from aframexr.utils.constants import AVAILABLE_ENCODING_TYPES
from aframexr.utils.validators import AframeXRValidator


class Encoding:
    """Encoding base class."""
    def __init__(self, field: str | None = None, aggregate: str | None = None, axis: bool = True,
                 encoding_type: str | None = None, groupby: list | None = None):
        from aframexr import AframeXRValidator  # To avoid circular import

        AframeXRValidator.validate_type(field, (str, type(None)))
        AframeXRValidator.validate_type(aggregate, (str, type(None)))
        AframeXRValidator.validate_type(axis, (bool, type(None)))
        AframeXRValidator.validate_type(encoding_type, (str, type(None)))
        AframeXRValidator.validate_type(groupby, (list, type(None)))

        self._field = field
        self._aggregate = aggregate
        self._axis = axis
        self._encoding_type = encoding_type
        self._groupby = groupby

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
    pass  # Using Encode __init__() method


class Y(Encoding):
    pass  # Using Encode __init__() method


class Z(Encoding):
    pass  # Using Encode __init__() method
