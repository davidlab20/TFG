"""Constant / default values utils file"""

# ----- CONSTANTS -----
AVAILABLE_COLORS = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
CHART_TEMPLATES = {
    'arc': ('<a-cylinder position="{pos}" rotation="-90 0 0" height="0.5" radius-inner="{inner_radius}" '
            'radius-outer="{outer_radius}" theta-start="{theta_start}" theta-length="{theta_length}" '
            'color="{color}"></a-cylinder>'),
    'bar': '<a-box position="{pos}" width="{width}" height="{height}" color="{color}"></a-box>',
    'point': '<a-sphere position="{pos}" radius="{radius}" color="{color}"></a-sphere>'
}
LABELS_X_DELTA = -3  # Variation in the x-axis between the labels and the axis (add to y and z axis pos for label pos)
LABELS_Y_DELTA = 0.01  # Variation in the y-axis between the labels and the axis (add to x and z axis pos for label pos)
LABELS_Z_DELTA = 1  # Variation in the y-axis between the labels and the axis (add to x-axis pos for label pos)
Y_NUM_OF_TICKS = 5  # Number of ticks in the y-axis

# ----- DEFAULTS -----
# General
DEFAULT_CHART_POS = '0 0 0'  # Default position of the chart
DEFAULT_MAX_DEPTH = 10  # Default maximum depth of the chart
DEFAULT_MAX_HEIGHT = 10  # Default maximum height of the chart

# Bar chart
DEFAULT_BAR_DEPTH = 1  # Default bar depth
DEFAULT_BAR_HEIGHT = 1  # Default bar height (if not field for y-axis specified)
DEFAULT_BAR_WIDTH = 1  # Default bar width

# Pie chart
DEFAULT_PIE_RADIUS = 2  # Default radius of the pie chart
DEFAULT_PIE_INNER_RADIUS = 0  # Default inner radius of the pie chart

# Point chart
DEFAULT_POINT_RADIUS = 1  # Default point radius
DEFAULT_POINT_X_SEPARATION = 1  # Default horizontal separation between points
DEFAULT_POINT_COLOR = "blue"  # Default point color
