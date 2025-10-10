"""BabiaXR Vega-Altair library"""


import copy
import marimo


class TopLevelMixin :
    """Top level chart class."""

    def __init__(self):
        self.charts = []
        self.sceneHtml = ''  # Scene HTML will be filled when saving or showing the chart automatically.

    # Creating the scene
    def __createHtmlScene(self):
        """Creates the HTML scene needed to visualize the chart (will be called automatically when necessary)."""

        chartsHtml = ''
        for chart in self.charts:
            chartsHtml += chart.toHtml()
        self.sceneHtml = f"""
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
                        
                        <!-- Charts -->
                        {chartsHtml}
                        
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

    # Saving the chart
    def save(self, filename):
        """Saves the chart into an HTML file."""

        self.__createHtmlScene()
        with open(filename, 'w') as file:
            file.write(self.sceneHtml)
            file.close()

    # Showing the chart
    def show(self):
        """Shows the chart in the marimo notebook."""

        self.__createHtmlScene()
        return marimo.iframe(self.sceneHtml)


class Chart(TopLevelMixin):
    """Simple chart class."""

    def __init__(self, data: str | list[dict]):
        """Init sample class.

        Args:
            data: string like JSON format or list of dictionaries with the data.
        """

        super().__init__()
        self.parameters = {}  # Parameters of the chart
        self._baseHtml = ''  # Base HTML of the chart
        self.html = ''  # The base HTML rendered with the parameters of the chart
        if type(data) == str:
            self.data = data
        elif type(data) == list:
            self.data = str(data)[1:-1]  # Take the data as string and delete the brackets
            self.data = self.data.replace("'", '"')  # Replace the character ' to " (sintaxis of charts)
        else:
            raise TypeError(f'Expected str or list[dict], got {type(data).__name__}')

    # Concatenate charts
    def __and__(self, other):
        """Vertical concatenation of charts using symbol &.

        Example:
            >>> import babiaAltair
            >>> data1 = '...'
            >>> data2 = '...'
            >>> upperChart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
            >>> lowerChart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
            >>> finalChart = upperChart & lowerChart
            >>> #finalChart.show()
        """

        return VConcatChart(self, other)

    def __or__(self, other):
        """Horizontal concatenation of charts using symbol |.

        Example:
              >>> import babiaAltair
              >>> data1 = '...'
              >>> data2 = '...'
              >>> leftChart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
              >>> rightChart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
              >>> finalChart = leftChart | rightChart
              >>> #finalChart.show()
        """

        return HConcatChart(self, other)

    def concat(self, other):
        """Horizontal concatenation of charts.

        Example:
            >>> import babiaAltair
            >>> data1 = '...'
            >>> data2 = '...'
            >>> leftChart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
            >>> rightChart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
            >>> finalChart = leftChart.concat(rightChart)
            >>> #finalChart.show()
        """

        return HConcatChart(self, other)

    def hconcat(self, other):
        """Horizontal concatenation of charts.

        Example:
            >>> import babiaAltair
            >>> data1 = '...'
            >>> data2 = '...'
            >>> leftChart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
            >>> rightChart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
            >>> finalChart = leftChart.hconcat(rightChart)
            >>> #finalChart.show()
        """

        return HConcatChart(self, other)

    def vconcat(self, other):
        """Vertical concatenation of charts.

        Example:
            >>> import babiaAltair
            >>> data1 = '...'
            >>> data2 = '...'
            >>> upperChart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
            >>> lowerChart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
            >>> finalChart = upperChart.vconcat(lowerChart)
            >>> #finalChart.show()
        """

        return VConcatChart(self, other)

    # Types of charts
    def mark_arc(self, inner_radius=0):
        """Pie chart (default) and doughnut chart."""

        chartType = 'pie'
        if inner_radius > 0:  # The inner_radius must be positive
            chartType = 'doughnut'
        self.parameters['posX'] = 0  # Default position in the X axis (if not concatenated)
        self.parameters['posY'] = 5  # Default position in the Y axis (if not concatenated)
        self.parameters['posZ'] = -5  # Default position in the Z axis (if not concatenated)
        self._baseHtml = f"""
            <a-entity babia-{chartType}""""""='legend: true; palette: blues; key: {key}; size: {size}; data:[{data}]'
                position="{posX} {posY} {posZ}" rotation="90 0 0">
            </a-entity>
            """
        return self

    def mark_bar(self):
        """Bars chart."""

        self.parameters['posX'] = 0  # Default position in the X axis (if not concatenated)
        self.parameters['posY'] = 0.5  # Default position in the Y axis (if not concatenated)
        self.parameters['posZ'] = -10  # Default position in the Z axis (if not concatenated)
        self._baseHtml = """
            <a-entity babia-bars='legend: true; palette: ubuntu; x_axis: {x}; height: {y}; data:[{data}]'
                position="{posX} {posY} {posZ}" rotation="0 0 0">
            </a-entity>
            """
        return self

    # Parameters of the chart
    def encode(self, theta='', color='', x='', y=''):
        """Completes and returns the necessary HTML to view the chart."""

        centerPoint = -self.data.count(x) / 2  # Value to center the chart (if necessary)
        if x:
            self.parameters['posX'] = centerPoint
        self.parameters.update({'data': self.data, 'key': theta, 'size': color, 'x': x, 'y': y})  # Add to params
        self.charts.append(self)  # Add the chart to the scene
        return self

    def toHtml(self):
        """Returns the HTML string of the chart."""

        self.html = self._baseHtml.format(**self.parameters)  # Fill the necessary parameters in the HTML of the chart
        return self.html

    # Copying the chart
    def copy(self):
        """Returns a copy of the chart."""

        return copy.deepcopy(self)  # Return a deep copy of the chart (changes in the copy do not affect the original)


# Multiple charts in the same scene
class VConcatChart(TopLevelMixin):
    """Vertical concatenation o charts class.

        Example:
            >>> import babiaAltair
            >>> data1 = '...'
            >>> data2 = '...'
            >>> upperChart = babiaAltair.Chart(data1).mark_bar().encode(x='xAxis1', y='yAxis1')
            >>> lowerChart = babiaAltair.Chart(data2).mark_bar().encode(x='xAxis2', y='yAxis2')
            >>> finalChart = babiaAltair.VConcatChart(upperChart, lowerChart)
            >>> #finalChart.show()
        """

    def __init__(self, *charts: Chart):
        """Init sample class. The concatenated chart stores copies of the charts."""

        super().__init__()
        if len(charts) != 2:
            raise TypeError(f'Expected 2 charts, got {len(charts)}')
        for c in charts:
            if type(c) != Chart:
                raise TypeError(f'Expected Chart, got {type(c).__name__}')
            self.charts.append(c.copy())
        self.__repositionCharts()

    def __repositionCharts(self):
        """Repositions the charts in the scene (for vertical concatenation)."""

        upperChart = self.charts[0]
        upperChart.parameters['posY'] += 5  # The upper chart is moved in the Y axis
        upperChart.parameters['posZ'] -= 3  # The chart is placed farther for better visualization
        lowerChart = self.charts[1]
        lowerChart.parameters['posZ'] -= 3  # The chart is placed farther for better visualization


class HConcatChart(TopLevelMixin):
    """Horizontal concatenation o charts class."""

    def __init__(self, *charts: Chart):
        """Init sample class. The concatenated chart stores copies of the charts."""

        super().__init__()
        if len(charts) != 2:
            raise TypeError(f'Expected 2 charts, got {len(charts)}')
        for c in charts:
            if type(c) != Chart:
                raise TypeError(f'Expected Chart, got {type(c).__name__}')
            self.charts.append(c.copy())
        self.__repositionCharts()

    def __repositionCharts(self):
        """Repositions the charts in the scene (for horizontal concatenation)."""

        leftChart = self.charts[0]
        leftChart.parameters['posX'] -= 5
        rightChart = self.charts[1]
        rightChart.parameters['posX'] += 5