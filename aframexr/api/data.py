"""AframeXR data types"""

import json


class Data:
    """
    Data class. See the example below to see the format.

    Examples
    --------
    # To instantiate Data using Data(data_format_as_list)

    >>> data_format_as_list = [{"a": 1, "b": 2}, {"a": 2, "b": 4}]
    >>> data = Data(data_format_as_list)

    # To instantiate Data using Data.from_json(data_format_as_string)

    >>> data_format_as_string = '[{"a": 1, "b": 2}, {"a": 2, "b": 4}]'
    >>> data = Data.from_json(data_format_as_string)
    """

    def __init__(self, values: list[dict]):
        if not isinstance(values, list):
            raise TypeError(f'Expected list[dict], got {type(values).__name__} instead. See documentation.')
        self.values = values



    # Import data
    @staticmethod
    def from_json(data: str):
        """Create a Data object from JSON string."""

        if not isinstance(data, str):
            raise TypeError(f'Expected dict, got {type(data).__name__} instead.')
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
    >>> url = '...'  # The URL of the file storing the data
    >>> data = URLData(url)
    """

    def __init__(self, url: str):
        if not isinstance(url, str):
            raise TypeError(f'Expected str, got {type(url).__name__} instead.')
        self.url = url