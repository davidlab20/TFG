"""BabiaXR Vega-Altair library"""


import marimo


class Chart:
    """Simple chart class."""

    def __init__(self, data: str | list[dict]):
        """Init sample class.

        Args:
            data: string like JSON format or list of dictionaries with the data.
        """

        if type(data) == str:
            self.data = data
        else:  # Type of tada is list[dict]
            self.data = str(data)[1:-1]  # Take the data as string and delete the brackets
            self.data = self.data.replace("'", '"')  # Replace the character ' to " (sintaxis of charts)
        self.chart = ''  # Chart HTML (will be filled with the necessary HTML to view the chart)
        self.html = ''  # Scene HTML (will be filled when encode() is called)

    # Types of charts
    def mark_arc(self, inner_radius=0):
        """Pie chart (default) and doughnut chart."""

        chartType = 'pie'
        if inner_radius > 0:  # The inner_radius must be positive
            chartType = 'doughnut'
        self.chart = f"""
            <a-entity babia-{chartType}""""""='legend: true; palette: blues; key: {key}; size: {size}; data:[{data}]'
                position="0 5 -5" rotation="90 0 0">
            </a-entity>"""
        return self

    def mark_bar(self):
        """Bars chart."""

        self.chart = """
            <a-entity babia-bars='legend: true; palette: ubuntu; x_axis: {x}; height: {y}; data:[{data}]'
                position="-{centerPoint} 0.5 -10" rotation="0 0 0">
            </a-entity>"""
        return self

    # Parameters of the chart
    def encode(self, theta='', color='', x='', y=''):
        """Completes and returns the necessary HTML to view the chart."""

        centerPoint = self.data.count(x) / 2  # Value to center the chart
        chartParameters = {'data': self.data, 'key': theta, 'size': color, 'x': x, 'y': y, 'centerPoint': centerPoint}
        self.html = f"""
            <!DOCTYPE html>
            <html class="a-html" lang="en">
                <head>
                    <script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script>
                    <script src="https://unpkg.com/aframe-environment-component@1.5.x/dist/aframe-environment-component.min.js"></script>
                    <script src="https://unpkg.com/aframe-babia-components/dist/aframe-babia-components.min.js"></script>
                    <script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v7.2.0/dist/aframe-extras.min.js"></script>
                </head>  
                <body class="a-body">
                    <a-scene>
                        <!-- Environment -->
                        <a-entity environment="preset: forest"></a-entity>
                        
                        <!-- Chart -->
                        {self.chart.format(**chartParameters)}
                        
                        <!-- Light -->
                        <a-light type="point" intensity="1" position="-10 20 30"></a-light>
                        
                        <!-- Camera -->
                        <a-entity movement-controls="fly: true" position="0 0 0">
                            <a-entity camera position="0 5 0" look-controls></a-entity>
                            <a-entity cursor="rayOrigin:mouse"></a-entity>
                            <a-entity laser-controls="hand: right"></a-entity>
                        </a-entity>
                    </a-scene>
                </body>
            </html>
            """
        return self

    # Saving the chart
    def save(self, filename):
        """Saves the chart into an HTML file."""

        with open(filename, 'w') as file:
            file.write(self.html)
            file.close()

    # Showing the chart
    def show(self):
        """Shows the chart in the marimo notebook."""

        return marimo.iframe(self.html)
