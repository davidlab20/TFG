"""Aframe library"""


from abc import abstractmethod, ABC


# Chart types
class Chart(ABC):
    """Aframe chart abstract class."""

    @abstractmethod
    def toHTML(self):
        """Must be created by child class."""

        pass


class PieChart(Chart):
    """Aframe piechart."""

    def __init__(self, data, key, size, title='', position='front'):
        self.data = data
        self.key = key  # Name of the data key field
        self.size = size  # Name of the value data field. Must be numeric
        self.title = title
        self.position = position  # Choices: ['front', 'back', 'left', 'right'], default: 'front'

    def toHTML(self):
        """Converts the pie chart to HTML format."""

        positions = {'front': '0 5 -5', 'back': '0 5 5', 'right': '5 5 0', 'left': '-5 5 0'}
        rotations = {'front': '90 0 0', 'back': '90 0 180', 'right': '90 0 90', 'left': '-90 0 90'}
        # titlePosition: higher X, more to the right; higher Y, more to the back; higher Z, more to the ground
        # titlePosition is relative to the actual position of the chart (taking rotation into account, it rotates axis)
        return f"""
            <a-entity babia-pie='legend: true; palette: blues; key: {self.key}; size: {self.size}; title: {self.title};
                titlePosition: 4 -5 -3; data:[{self.data}]' position="{positions.get(self.position)}"
                rotation="{rotations.get(self.position)}">
            </a-entity>
            """


class BarsChart(Chart):
    """Aframe bars chart."""

    def __init__(self, data, xAxis, yAxis, title='', position='front'):
        self.data = data
        self.xAxis = xAxis  # Data name field of the X axis
        self.yAxis = yAxis  # Data name field of the Y axis (height). Must be numeric
        self.title = title
        self.position = position  # Choices: ['front', 'back', 'left', 'right'], default: 'front'

    def toHTML(self):
        """Converts the bars chart to HTML format."""

        centerPoint = self.data.count(self.xAxis) / 2  # Value to center the chart
        titleHeight = 11  #json.loads(f'[{self.data}]')  # Height value of the title
        #print(titleHeight)
        positions = {'front': f'-{centerPoint} 0.5 -10', 'back': f'{centerPoint} 0.5 10',
                     'right': f'10 0.5 -{centerPoint}', 'left': f'-10 0.5 {centerPoint}'}
        rotations = {'front': '0 0 0', 'back': '180 0 180', 'right': '0 -90 0', 'left': '0 90 0'}
        return f"""
            <a-entity babia-bars='legend: true; palette: ubuntu; x_axis: {self.xAxis}; height: {self.yAxis};
                title: {self.title}; titlePosition: 9 {titleHeight} 0; data:[{self.data}]'
                position="{positions.get(self.position)}" rotation="{rotations.get(self.position)}">
            </a-entity>
            """


class BarsMapChart(Chart):
    """Aframe bars map chart."""

    def __init__(self, data: str, xAxis, yAxis, zAxis, title='', position='front'):
        self.data = data
        self.xAxis = xAxis  # Data name field of the X axis
        self.yAxis = yAxis  # Data name field of the Y axis (height). Must be numeric
        self.zAxis = zAxis  # Data name field of the Z axis
        self.title = title
        self.position = position  # Choices: ['front', 'back', 'left', 'right'], default: 'front'

    def toHTML(self):
        """Converts the bars map chart to HTML format."""

        centerPoint = self.data.count(self.xAxis) / 2  # Value to center the chart
        positions = {'front': f'-{centerPoint} 0.5 -12', 'back': f'{centerPoint} 0.5 12',
                     'right': f'12 0.5 -{centerPoint}', 'left': f'-12 0.5 {centerPoint}'}
        rotations = {'front': '0 0 0', 'back': '180 0 180', 'right': '0 -90 0', 'left': '0 90 0'}
        return f"""
            <a-entity babia-barsmap='legend: true; palette: ubuntu; x_axis: {self.xAxis}; height: {self.yAxis};
                z_axis: {self.zAxis}; title: {self.title}; data:[{self.data}]'
                position="{positions.get(self.position)}" rotation="{rotations.get(self.position)}">
            </a-entity>
            """


class CylsChart(Chart):
    """Aframe cyls chart."""

    def __init__(self, data, xAxis, yAxis, radius, title='', position='front'):
        self.data = data
        self.xAxis = xAxis  # Data name field of the X axis
        self.yAxis = yAxis  # Data name field of the Y axis (height). Must be numeric
        self.radius = radius  # Data name field of the cylinder radius. Must be numeric
        self.title = title
        self.position = position  # Choices: ['front', 'back', 'left', 'right'], default: 'front'

    def toHTML(self):
        """Converts the cyls chart to HTML format."""

        centerPoint = self.data.count(self.xAxis)  # Value to center the chart
        positions = {'front': f'-{centerPoint} 0.5 -10', 'back': f'{centerPoint} 0.5 10',
                     'right': f'10 0.5 -{centerPoint}', 'left': f'-10 0.5 {centerPoint}'}
        rotations = {'front': '0 0 0', 'back': '180 0 180', 'right': '0 -90 0', 'left': '0 90 0'}
        return f"""
            <a-entity babia-cyls='legend: true; palette:foxy; x_axis: {self.xAxis}; height: {self.yAxis};
                radius: {self.radius}; title: {self.title}; data:[{self.data}]' position="{positions.get(self.position)}"
                rotation="{rotations.get(self.position)}" scale="0.5 0.5 0.5">
            </a-entity>
            """


# Scenes
class Scene:
    """Aframe scene."""

    def __init__(self, environment='default'):
        self.environment = environment
        self.charts = ''  # Scene is initialized with no charts

    def addChart(self, *charts: Chart):
        """Add charts to the scene."""

        for chart in charts:
            self.charts += chart.toHTML()

    def toHTML(self):
        """Converts the scene to HTML format."""

        return f"""
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
                    <a-entity environment="preset: {self.environment}"></a-entity>
                    
                    <!-- Charts -->
                    {self.charts}
        
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


# LINEA 59 Y 60, TODAVIA NO FUNCIONA EL TITULO DEL CHART
""" Para obtener data formato string sin los corchetes si data es un fichero .json
with open('data.json', 'r') as AAA:
    data = json.load(AAA)
    print(str(data)[1:-1])
"""
