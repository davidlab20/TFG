"""BabiaXR scene creator"""


from utils.chartsHtmlCreator import ChartsHTMLCreator


DATA_QUERY_ID = 'query'  # Data query id of the HTML entity of the data


class SceneCreator:
    """Scene creator class. Creates the iframe scene from the JSON specifications."""

    def __init__(self):
        pass

    @staticmethod
    def create_iframe_scene(specs: dict):
        """
        Creates the iframe scene from the JSON specifications.

        Parameters
        ----------
        specs : dict
            JSON Schema specifications.

        Returns
        -------
        str
            HTML iframe scene.

        Raises
        ------
        TypeError
            If specs is not a dictionary.
        KeyError
            If a key is not found in the JSON specification.

        Notes
        -----
        Suppose specs is a dictionary for posterior function calls of ChartsHTMLCreator.
        """

        # Inner functions
        def data_html() -> str:
            """Inner function to create the HTML of the data zone."""

            if not 'data' in specs:  # Verificate 'data' is on the specifications
                raise KeyError('Specs must contain "data".')
            if 'url' in specs['data']:  # Data comes from a URL
                url = specs['data']['url']
                return f'<a-entity id="{DATA_QUERY_ID}" babia-queryjson="url: {url};"></a-entity>'
            if 'values' in specs['data']:  # Data comes raw
                data = specs['data']['values']
                return f'<a-entity id="{DATA_QUERY_ID}" babia-queryjson="data: {data};"></a-entity>'
            else:
                raise KeyError('Error when decoding the data. Incorrect format.')

        def charts_html() -> str:
            """Inner function to create the HTML of the chart zone."""

            if 'concat' in specs:
                return ChartsHTMLCreator.create_charts_html(specs, 'concat')
            elif 'hconcat' in specs:
                return ChartsHTMLCreator.create_charts_html(specs, 'hconcat')
            elif 'vconcat' in specs:
                return ChartsHTMLCreator.create_charts_html(specs, 'vconcat')
            else:
                return ChartsHTMLCreator.create_charts_html(specs)  # Single chart specification

        # Main function
        if not isinstance(specs, dict):
            raise TypeError(f'Specs must be a dictionary, got {type(specs).__name__}.')
        html_iframe_scene = f"""
            <!DOCTYPE html>
            <html class="a-html" lang="en">
                <head>
                    <script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script>
                    <script src="https://unpkg.com/aframe-environment-component@1.5.x/dist/aframe-environment-component.min.js"></script>
                    <script src="https://unpkg.com/aframe-babia-components/dist/aframe-babia-components.min.js"></script>
                    <script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v7.2.0/dist/aframe-extras.min.js"></script>
                    <script src="https://gitlab.com/babiaxr/aframe-babia-components/-/raw/master/dist/aframe-babia-components.js"></script>
                    <script src="https://unpkg.com/aframe-babia-components@1.3.4/dist/aframe-babia-components.min.js"></script>
                </head>  
                <body class="a-body">
                    <a-scene>
                        <!-- Environment -->
                        <a-entity environment="preset: forest"></a-entity>
                        
                        <!-- Data -->
                        {data_html()}
                        
                        <!-- Charts -->
                        {charts_html()}
                        
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
        return html_iframe_scene
