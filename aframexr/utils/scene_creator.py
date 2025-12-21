"""AframeXR scene creator"""

from aframexr.utils.entities_html_creator import ChartsHTMLCreator

HTML_SCENE_TEMPLATE = """<!DOCTYPE html>
<head>
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <script src="https://unpkg.com/aframe-environment-component@1.5.0/dist/aframe-environment-component.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/davidlab20/TFG@v0.5.5/docs/scripts/main.min.js"></script>
</head>
<body>
    <a-scene cursor="rayOrigin: mouse" raycaster="objects: [data-raycastable]">
    
        <!-- Camera -->
        <a-camera position="0 4 0" active="true">

            <!-- Element information -->
            <a-entity id="HUD" position="-4.5 2 -4" visible="false">
				<a-plane height="1" width="2.5" shader="flat" color="grey"></a-plane>
				<a-text id="HUD-text" value="" align="center"></a-text>
			</a-entity>
        </a-camera>
    
        <!-- Environment -->
        <a-entity environment="preset: default"></a-entity>
        
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
