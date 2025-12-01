"""Constants for testing."""

# ----- GENERAL -----
# Data
URL_DATA = 'https://davidlab20.github.io/TFG/examples/data/data.json'

# Positions OK
POSITIONS = ['0 0 0', '0 0 2', '0 2 0', '0 2 2', '2 0 0', '2 0 2', '2 2 0', '2 2 2']
POSITION_FORMATS = ['1 1 1', '1  1  1', '  1 1 1  ', '  1  1  1  ']

# Rotations OK
ROTATIONS = ['0 0 0', '0 0 30', '0 30 0', '0 30 30', '30 0 0', '30 0 30', '30 30 0', '30 30 30']
ROTATION_FORMATS = ['30 30 30', '30  30  30', '  30 30 30  ', '  30  30  30  ']

# Positions and rotations ERROR
NOT_3AXIS_POSITIONS_ROTATIONS = [' ', '1', '1 1', '1 1 1 1']
NOT_NUMERIC_POSITIONS_ROTATIONS = ['1 1 a', '1 a 1', '1 a a', 'a 1 1', 'a 1 a', 'a a 1', 'a a a']

# Filters OK
FILTER_EQUATIONS = ['datum.motor = diesel', 'datum.doors = 3', 'datum.doors > 4', 'datum.doors < 4']

# Filters WARNING
WARNING_FILTER_EQUATIONS = ['datum.motor = bad_value', 'datum.doors = 0', 'datum.doors > 100', 'datum.doors < 0']

# Filters ERROR
ERROR_FILTER_EQUATIONS = ['motor = diesel', 'doors = 0', 'doors > 100', 'doors < 0']

# ----- MARK ARC -----
# Radius OK
MARK_ARC_RADIUS = [0.5, 1, 1.5]

# Radius ERROR
NOT_GREATER_THAN_0_MARK_ARC_RADIUS = [-1, 0]

# Encodings ERROR
NOT_VALID_MARK_ARC_ENCODINGS = [{'color': 'model'}, {'theta': 'sales'}, {'x': 'model', 'y': 'sales'}]

# ----- MARK BAR / MARK POINT -----
# Sizes OK
MARK_BAR_POINT_SIZES = [0.5, 1, 1.5]

# Heights OK
MARK_BAR_POINT_HEIGHTS = [0.5, 10, 20]

# Sizes and heights ERROR
NOT_GREATER_THAN_0_MARK_BAR_POINT_SIZES_HEIGHTS = [-1, 0]

# Encodings OK
MARK_BAR_ENCODINGS = [{'x': 'model', 'y': 'sales'}, {'x': 'model', 'z': 'motor'}, {'y': 'sales', 'z': 'motor'},
                      {'x': 'model', 'y': 'sales', 'z': 'motor'}]
MARK_POINT_ENCODINGS = [{'x': 'model', 'y': 'sales', 'color': 'motor'}, {'x': 'model', 'y': 'sales', 'size': 'doors'},
                        {'x': 'model', 'y': 'sales', 'color': 'motor', 'size': 'doors'}, *MARK_BAR_ENCODINGS]

# Encodings ERROR
NOT_VALID_MARK_BAR_POINT_ENCODINGS = [{'x': 'model'}, {'y': 'sales'}, {'z': 'motor'}, {'color': 'motor'}]

# ----- MARK GLTF / MARK IMAGE -----
# Scales OK
MARK_GLTF_SCALES = ['-2  1  -1', '-1', '1', '2', '2  2', '2 2 2', '2 2   2 2 ', '2 2  2   2 2']

# ----- MARK IMAGE -----
# Widths and heights OK
MARK_IMAGE_WIDTHS_HEIGHTS = [0.5, 1, 1.5, 2, 5, 10]

# Widths and heights ERROR
NOT_GREATER_THAN_0_MARK_IMAGE_WIDTHS_HEIGHTS = [-1, 0]
