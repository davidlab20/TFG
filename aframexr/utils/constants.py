"""Constant / default values utils file"""

# ----- CONSTANTS -----
AVAILABLE_COLORS = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
CHART_TEMPLATES = {
    'arc': ('<a-ring position="{pos}" radius-inner="{inner_radius}" radius-outer="{outer_radius}" '
            'theta-start="{theta_start}" theta-length="{theta_length}" color="{color}"></a-ring>'),
    'bar': '<a-box position="{pos}" width="{width}" height="{height}" color="{color}"></a-box>',
    'point': '<a-sphere position="{pos}" radius="{radius}" color="{color}"></a-sphere>'
}

# ----- DEFAULTS -----
# General
DEFAULT_CHART_POS = '0 0 0'  # Default position of the chart
DEFAULT_MAX_HEIGHT = 10  # Default maximum height of the chart

# Bar chart
DEFAULT_BAR_WIDTH = 1  # Default bar width

# Pie chart
DEFAULT_PIE_RADIUS = 2  # Default radius of the pie chart
DEFAULT_PIE_INNER_RADIUS = 0  # Default inner radius of the pie chart

# Point chart
DEFAULT_POINT_RADIUS = 1  # Default point radius
DEFAULT_POINT_X_SEPARATION = 1  # Default horizontal separation between points
DEFAULT_POINT_COLOR = "blue"  # Default point color
