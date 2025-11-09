"""AframeXR axis HTML creator"""


class AxisHTMLCreator:
    """Axis HTML creator class."""

    @staticmethod
    def create_axis_html(start: str, end_x: float, end_y: float, end_z: float):
        """
        Create a line for each axis and returns the HTML of the axis.

        Parameters
        ----------
        start : str
            The base position of each axis.
        end_x : float
            The end position of x-axis.
        end_y : float
            The end position of y-axis.
        end_z : float
            The end position of z-axis.
        """

        html = ''
        base_x, base_y, base_z = start.split()
        base_x, base_y, base_z = float(base_x), float(base_y), float(base_z)  # Convert into float

        # X-axis
        html += f'<a-entity line="start: {start}; end: {end_x} {base_y} {base_z}; color: black"></a-entity>\n\t\t'

        # Y-axis
        html += f'<a-entity line="start: {start}; end: {base_x} {end_y} {base_z}; color: black"></a-entity>\n\t\t'

        # Z-axis
        html += f'<a-entity line="start: {start}; end: {base_x} {base_y} {end_z}; color: black"></a-entity>\n\t\t'

        return html
