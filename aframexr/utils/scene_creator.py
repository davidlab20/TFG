"""AframeXR scene creator"""

from aframexr.utils.charts_html_creator import ChartsHTMLCreator

HTML_SCENE_TEMPLATE = """<!DOCTYPE html>
<head>
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <script src="https://unpkg.com/aframe-environment-component@1.3.3/dist/aframe-environment-component.min.js"></script>
</head>
<body>
    <a-scene>
        <!-- Camera -->
        <a-camera position="0 4 0"></a-camera>
        
        <!-- Movement controls -->
        <a-entity camera look-controls wasd-controls="acceleration:80"></a-entity>
    
        <!-- Environment -->
        <a-entity environment="preset: forest"></a-entity>
        
        <!-- Elements -->
        {elements}
    </a-scene>
</body>
"""


class SceneCreator:

    @staticmethod
    def create_scene(specs: dict):
        """
        Creates the HTML scene from the JSON specifications.

        Parameters
        ----------
        specs : dict
            Specifications of the elements composing the scene.

        Raises
        ------
        TypeError
            If specs is not a dictionary.

        Notes
        -----
        Suppose that specs is a dictionary for posterior method calls of ChartsHTMLCreator.
        """

        if not isinstance(specs, dict):
            raise TypeError(f'Expected specs to be a dict, got {type(specs).__name__}')
        elements_html = ChartsHTMLCreator.create_charts_html(specs)
        return HTML_SCENE_TEMPLATE.format(elements=elements_html)
