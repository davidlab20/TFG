"""Constant / default values utils file"""

# ----- CONSTANTS -----
AVAILABLE_AGGREGATES = ('count', 'max', 'median', 'mean', 'min', 'std', 'sum', 'var')
AVAILABLE_COLORS = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
AVAILABLE_ENCODING_TYPES = {'Q': 'quantitative', 'N': 'nominal'}

START_LABEL_OFFSET = 0.25  # Offset for the start label of the axis
X_LABELS_Z_DELTA = 0.5  # Variation in the y-axis between the labels and the axis (add to x-axis pos for label pos)
LABELS_X_DELTA = -0.5  # Variation in the x-axis between the labels and the axis (add to y and z axis pos for label pos)
LABELS_Y_DELTA = 0.01  # Variation in the y-axis between the labels and the axis (add to x and z axis pos for label pos)

# ----- TEMPLATES -----
CHART_TEMPLATES = {
    'arc': ('<a-cylinder id="{id}" position="{pos}" height="{depth}" radius="{radius}" theta-start="{theta_start}" '
            'theta-length="{theta_length}" material="color: {color}" data-raycastable></a-cylinder>'),
    'bar': ('<a-box id="{id}" position="{pos}" width="{width}" height="{height}" material="color: {color}" '
            'depth="{depth}" data-raycastable></a-box>'),
    'point': ('<a-sphere id="{id}" position="{pos}" radius="{radius}" material="color: {color}" data-raycastable>'
             '</a-sphere>')
}
IMAGES_TEMPLATES = {
    'gltf': '<a-gltf-model src="{src}" scale="{scale}"></a-gltf-model>',
    'image': '<a-image src="{src}" width="{width}" height="{height}"></a-image>'
}
ALL_TEMPLATES = {**CHART_TEMPLATES, **IMAGES_TEMPLATES}  # Grouped dictionary with all templates

# ----- DEFAULTS -----
# General
DEFAULT_CHART_POS = '0 0 0'  # Default position of the chart
DEFAULT_CHART_ROTATION = '0 0 0'  # Default chart rotation
DEFAULT_CHART_DEPTH = 10  # Default depth of the chart
DEFAULT_CHART_HEIGHT = 10  # Default height of the chart
DEFAULT_CHART_WIDTH = 10  # Default width of the chart

DEFAULT_NUM_OF_TICKS_IF_QUANTITATIVE_AXIS = 5  # Number of ticks in the axis if it is quantitative

# Bar chart
DEFAULT_BAR_AXIS_SIZE = 1  # Default bar size in the nominal axes and in the axis that are not defined.

# Pie chart
DEFAULT_PIE_RADIUS = 2  # Default radius of the pie chart
DEFAULT_PIE_ROTATION = '-90 0 0'  # Default pie chart rotation
DEFAULT_PIE_INNER_RADIUS = 0  # Default inner radius of the pie chart

# GLTF model
DEFAULT_GLTF_SCALE = '1 1 1'  # Default scale of the GLTF model

# Image
DEFAULT_IMAGE_HEIGHT = 1  # Default height of the image
DEFAULT_IMAGE_WIDTH = 1  # Default width of the image

# Point chart
DEFAULT_POINT_COLOR = "blue"  # Default point color
DEFAULT_POINT_HEIGHT_WHEN_NO_Y_AXIS = 2  # Default point height (if not field for y-axis specified)
DEFAULT_POINT_RADIUS = 1  # Default point radius
DEFAULT_POINT_CENTER_SEPARATION = 2  # Default separation between points' center
