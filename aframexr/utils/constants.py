"""Constant / default values utils file"""

# ----- CONSTANTS -----
AVAILABLE_AGGREGATES = {'count', 'max', 'median', 'mean', 'min', 'std', 'sum', 'var'}
AVAILABLE_COLORS = {'red', 'green', 'blue', 'yellow', 'magenta', 'cyan'}
AVAILABLE_ENCODING_TYPES = {'Q': 'quantitative', 'N': 'nominal'}

START_LABEL_OFFSET = 0.25  # Offset for the start label of the axis
X_LABELS_Z_DELTA = 0.5  # Variation in the y-axis between the labels and the axis (add to x-axis pos for label pos)
LABELS_X_DELTA = -0.5  # Variation in the x-axis between the labels and the axis (add to y and z axis pos for label pos)
LABELS_Y_DELTA = 0.01  # Variation in the y-axis between the labels and the axis (add to x and z axis pos for label pos)

# ----- DEFAULTS -----
# General
DEFAULT_CHART_POS = '0 0 0'  # Default position of the chart
DEFAULT_CHART_ROTATION = '0 0 0'  # Default chart rotation
DEFAULT_CHART_DEPTH = 2  # Default depth of the chart
DEFAULT_CHART_HEIGHT = 4  # Default height of the chart
DEFAULT_CHART_WIDTH = 4  # Default width of the chart

DEFAULT_NUM_OF_TICKS_IF_QUANTITATIVE_AXIS = 5  # Number of ticks in the axis if it is quantitative

PRECISION_DECIMALS = 4  # Number of decimals of the elements' values

# Pie chart
DEFAULT_PIE_RADIUS = 1  # Default radius of the pie chart
DEFAULT_PIE_ROTATION = '-90 0 0'  # Default pie chart rotation

# Point chart
DEFAULT_POINT_COLOR = "blue"  # Default point color
DEFAULT_POINT_RADIUS = 0.5  # Default point radius
