"""BabiaXR data types"""

import json


class Data:
    """
    Data class. See the example below to see the format.

    Examples
    --------
    >>> data_format = [{"a": 1, "b": 2}, {"a": 2, "b": 4}, ...]
    ...
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
    """URL data class."""

    def __init__(self, url: str):
        self.url = url