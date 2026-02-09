"""Constant / default values utils file"""

# ----- CONSTANTS -----
AVAILABLE_AGGREGATES = {'count', 'max', 'median', 'mean', 'min', 'std', 'sum', 'var'}
AVAILABLE_COLORS = {'red', 'green', 'blue', 'yellow', 'magenta', 'cyan'}
AVAILABLE_ENCODING_TYPES = {'Q': 'quantitative', 'N': 'nominal'}
AVAILABLE_MARKS = {'arc', 'bar', 'point'}

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

# ========== ERROR MESSAGES ==========
ERROR_MESSAGES = {
    'AGGREGATE_OPERATION': 'Invalid aggregate operation: {operation}',
    'AGGREGATE_OPERATION_NOT_IN_AGGREGATE': 'Aggregate must contain key "op"',
    'DATA_WITH_VALUES_AND_URL_IN_SPECS': 'Data cannot contain both "values" and "url"; they are mutually exclusive',
    'DATA_WITH_NOT_VALUES_NEITHER_URL_IN_SPECS': 'Data must contain key "values" or "url"',
    'DATA_NOT_IN_SPECS': 'Invalid chart specifications. Must contain key "data"',
    'ELEMENT_TYPE': 'Invalid element type: {element}',
    'ENCODING_NOT_IN_SPECS': 'Invalid chart specifications. Must contain key "encoding"',
    'ENCODING_TYPE': 'Invalid encoding type: {encoding_type}',
    'MARK_AND_ELEMENT_IN_SPECS': 'Specifications cannot contain both "mark" and "element"; they are mutually exclusive',
    'MARK_AND_ELEMENT_NOT_IN_SPECS': 'Invalid chart specifications. Must contain key "mark" or "element"',
    'MARK_TYPE': 'Invalid mark type: {mark_type}',
    'NOT_3_AXES_POSITION_OR_ROTATION': 'The {pos_or_rot}: {pos_or_rot_value} is not correct. Must be "x y z"',
    'NOT_ALL_DATA_VALUES_ARE_DICT': 'Data field "values" must be a list of dictionaries',
    'NOT_ALL_ENCODINGS_ARE_DICT': 'Encoding channels must be dictionaries',
    'PARAM_NOT_SPECIFIED_IN_MARK_ARC': 'Parameter "{param}" must be specified in arc chart',
    'POSITIVE_NUMBER': 'The "{param_name}" must be greater than 0.',
    'LESS_THAN_2_XYZ_ENCODING': 'At least 2 of (x, y, z) must be specified when encoding "mark_bar" or "mark_point"',
    'TRANSFORM_TYPE': 'Invalid transform type: {transform_type}',
    'TYPE': 'Expected "{param_name}" to be {expected_type}, got {current_type} instead',
}
