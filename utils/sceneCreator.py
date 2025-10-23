"""BabiaXR scene creator"""

from babiaxr.filters import FilterTransform
from utils.chartsHtmlCreator import ChartsHTMLCreator


DATA_QUERY_ID = 'query'  # Data query id of the HTML entity of the data
FILTERS_QUERY_ID = 'filter_query'  # Filtered data query id of the HTML entity of the data
FINAL_DATA_QUERY_ID = DATA_QUERY_ID  # Will change if raw data is transformed (for example, if filtered)


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

            data_field = ''

            # Main data
            if not 'data' in specs:  # Verificate 'data' is on the specifications
                raise KeyError('Specs must contain "data".')
            if 'url' in specs['data']:  # Data comes from a URL
                url = specs['data']['url']
                data_field += f'''<a-entity id="{DATA_QUERY_ID}" babia-queryjson='url: {url};'></a-entity>'''
            elif 'values' in specs['data']:  # Data comes raw
                data = str(specs['data']['values']).replace("\'", "\"")  # Replace ' to " because of syntaxis
                data_field += f'''<a-entity id="{DATA_QUERY_ID}" babia-queryjson='data: {data};'></a-entity>'''
            else:
                raise KeyError('Error when decoding the data. Incorrect format.')

            # Filtered data (if existing)
            if specs.get('transform'):  # There are transformations of the data
                for transformation in specs['transform']:
                    if transformation.get('filter'):  # FilterTransform field
                        filter_object = FilterTransform.from_string(
                            transformation['filter'])  # Create filter from equation
                        data_field += f'''
                            <a-entity id="{FILTERS_QUERY_ID}" babia-filter="from: {DATA_QUERY_ID}; 
                                filter: {filter_object.equation_to_string()}">
                            </a-entity>
                        '''

                        # Change the id of the HTML field of the final data so charts get transformed data
                        global FINAL_DATA_QUERY_ID
                        FINAL_DATA_QUERY_ID = FILTERS_QUERY_ID
                    else:
                        pass  # Not implemented jet
            return data_field

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
        global FINAL_DATA_QUERY_ID
        FINAL_DATA_QUERY_ID = DATA_QUERY_ID  # Set FINAL_QUERY_DATA_ID to the default id (in case it has been changed)
        html_iframe_scene = f"""
            <!DOCTYPE html>
            <html class="a-html" lang="en">
                <head>
                    <script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script>
                    <script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v7.2.0/dist/aframe-extras.min.js"></script>
                    <script src="https://unpkg.com/aframe-environment-component@1.3.3/dist/aframe-environment-component.min.js"></script>
                    <script src="https://unpkg.com/aframe-text-geometry-component@0.5.1/dist/aframe-text-geometry-component.min.js"></script>
                    <script src="https://unpkg.com/aframe-babia-components/dist/aframe-babia-components.min.js"></script>
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
