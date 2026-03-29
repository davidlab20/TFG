from .entities_html_creator import ChartsHTMLCreator

HTML_SCENE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <title>VR Scene</title>
  <meta charset="utf-8">
  <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
  <script src="https://cdn.jsdelivr.net/gh/c-frame/aframe-extras@7.6.1/dist/aframe-extras.min.js"></script>
  <script src="https://unpkg.com/aframe-environment-component@1.5.0/dist/aframe-environment-component.min.js"></script>
  <script src="https://cdn.jsdelivr.net/gh/davidlab20/TFG@v0.10.1/docs/static/scripts/main.min.js"></script>
</head>
<body>
<a-scene cursor="rayOrigin: mouse" raycaster="objects: [raycastable]" drag-controls="mode: cursor"
         xr-mode-ui="XRMode: xr" webxr="optionalFeatures: hit-test, local-floor;" ar-hit-test="target: #charts">
  <a-entity id="user" movement-controls="speed: 0.1">

    <!-- Camera -->
    <a-camera id="camera" position="0 1.6 0" active="true" wasd-controls="acceleration: 15"></a-camera>

    <!-- VR controllers -->
    <a-entity laser-controls="hand: right" raycaster="objects: [raycastable]" drag-controls="mode: vr"></a-entity>
    <a-entity laser-controls="hand: left" raycaster="objects: [raycastable]" drag-controls="mode: vr"></a-entity>
  </a-entity>

  <!-- HUD -->
  <a-entity id="HUD" visible="false" scale-on-enter-ar>
    <a-plane id="HUD-plane" width="2" shader="flat" color="grey"></a-plane>
    <a-entity id="HUD-texts"></a-entity>
  </a-entity>

  <!-- Environment -->
  <a-entity environment="preset: {environment}" hide-on-enter-ar></a-entity>
  <a-light type="ambient" show-on-enter-ar></a-light>

  <!-- Elements -->
  <a-entity id="charts" scale-on-enter-ar{ar_scale_value} look-at-camera-on-ar>
    {elements}
  </a-entity>
</a-scene>
</body>
</html>"""


class SceneCreator:
    @staticmethod
    def create_scene(specs: dict):
        """
        Creates the HTML scene from the JSON specifications.

        Parameters
        ----------
        specs : dict
            Specifications of the elements composing the scene.
        """
        ar_scale = specs.get('ar_scale')
        if ar_scale is None:
            ar_scale_value = ''  # Using default's JavaScript value
        else:
            ar_scale_value = f'="scale: {ar_scale}"'  # Setting value for JavaScript
        environment = specs.get('environment', 'default')
        elements_html = ChartsHTMLCreator.create_charts_html(specs)
        return HTML_SCENE_TEMPLATE.format(
            ar_scale_value=ar_scale_value, environment=environment, elements=elements_html
        )
