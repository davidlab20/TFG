"""AframeXR axis HTML creator"""


class AxisHTMLCreator:
    """Axis HTML creator class."""

    @staticmethod
    def create_axis_html(start: str | None, end: str | None) -> str:
        """
        Create a line for the axis and returns its HTML.

        Parameters
        ----------
        start : str | None
            The base position of each axis. If None, no axis is displayed.
        end : str | None
            The end position of the axis. If None, no axis is displayed.
        """

        if start and end:
            return f'<a-entity line="start: {start}; end: {end}; color: black"></a-entity>'
        return ''

    @staticmethod
    def create_label_html(pos: str, rotation: str, value: str) -> str:
        """
        Create a text with the value of the label in the correct position and returns its HTML.

        Parameters
        ----------
        pos : str
            The position of the label.
        rotation : str
            The rotation of the label (for better visualization).
        value : str
            The value of the label.
        """

        return f'<a-text position="{pos}" rotation="{rotation}" value="{value}" scale="3 3 3"></a-text>'
