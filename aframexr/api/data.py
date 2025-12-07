"""AframeXR data types"""

import json

from aframexr.utils.validators import AframeXRValidator


class Data:
    """
    Data class. See the example below to see the format.

    Examples
    --------
    # To instantiate Data using Data(data_format_as_list)

    >>> import aframexr
    >>> data_format_as_list = [{"a": 1, "b": 2}, {"a": 2, "b": 4}]
    >>> data = aframexr.Data(data_format_as_list)

    # To instantiate Data using Data.from_json(data_format_as_string)

    >>> import aframexr
    >>> data_format_as_string = '[{"a": 1, "b": 2}, {"a": 2, "b": 4}]'
    >>> data = aframexr.Data.from_json(data_format_as_string)
    """

    def __init__(self, values: list[dict]):
        AframeXRValidator.validate_type(values, list)
        self.values = values



    # Import data
    @staticmethod
    def from_json(data: str):
        """Create a Data object from JSON string."""

        AframeXRValidator.validate_type(data, str)
        data = json.loads(data)
        return Data(data)

    # Export data
    def to_json(self) -> str:
        """Return a JSON string representation of the data."""

        return json.dumps(self.values)


class URLData:
    """
    URLData class.

    Examples
    --------
    >>> import aframexr
    >>> url = '...'  # The URL of the file storing the data
    >>> data = aframexr.URLData(url)
    """

    def __init__(self, url: str):
        AframeXRValidator.validate_type(url, str)
        self.url = url