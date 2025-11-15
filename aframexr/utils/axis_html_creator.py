"""AframeXR axis HTML creator"""


class AxisHTMLCreator:
    """Axis HTML creator class."""

    @staticmethod
    def create_axis_html(start: str | None, end: str | None) -> str:
        """
        Create a line for each axis and returns the HTML of the axis.

        Parameters
        ----------
        start : str | None
            The base position of each axis. If None, no axis is displayed.
        end : str | None
            The end position of the axis. If None, no axis is displayed.
        """

        if start and end:
            return f'<a-entity line="start: {start}; end: {end}; color: black"></a-entity>\n\t\t'
        return ''
