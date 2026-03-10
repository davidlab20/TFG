import aframexr

# ===== SPACE CONFIGURATION =====
ROOM_DEPTH = 37
ROOM_HEIGHT = 8
ROOM_WIDTH = 32

room = aframexr.Box(
    position=f'0 {ROOM_HEIGHT / 2 - 0.1} {-ROOM_DEPTH / 4}',
    depth=ROOM_DEPTH, height=ROOM_HEIGHT, width=ROOM_WIDTH,
    color='lightGreen'
)

# ===== CHARTS =====
DATA = aframexr.UrlData('https://cdn.jsdelivr.net/gh/davidlab20/TFG@main/docs/static/data/data.json')
PLATFORMS_CONFIG = {'height': 0.2, 'additional_depth': 4, 'additional_width': 3, 'color': 'darkSlateGray'}

_CHART_DEPTH = 1
_CHART_HEIGHT = 3
_CHART_WIDTH = 5

BASE = aframexr.Chart(DATA, depth=_CHART_DEPTH, height=_CHART_HEIGHT, width=_CHART_WIDTH)

charts = []

# === BAR CHARTS ===
# Vertical bar chart
_CENTER_X_POS_BAR_VERTICAL = -6
_CENTER_Z_POS_BAR_VERTICAL = -15

bar_platform_vertical = aframexr.Box(
    position=f'{_CENTER_X_POS_BAR_VERTICAL} {PLATFORMS_CONFIG['height'] / 2} {_CENTER_Z_POS_BAR_VERTICAL}',
    depth=_CHART_DEPTH + PLATFORMS_CONFIG['additional_depth'],
    height=PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + PLATFORMS_CONFIG['additional_width'],
    color=PLATFORMS_CONFIG['color'],
)
bar_chart_vertical = BASE.mark_bar().encode(x='motor', y='sum(sales)').properties(
    position=f'{_CENTER_X_POS_BAR_VERTICAL} {PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_CENTER_Z_POS_BAR_VERTICAL}',
    title='Vertical bar chart',
)

charts.append(bar_platform_vertical), charts.append(bar_chart_vertical)

# Horizontal bar chart
_CENTER_X_POS_BAR_HORIZONTAL = 6
_CENTER_Z_POS_BAR_HORIZONTAL = -15

bar_platform_horizontal = aframexr.Box(
    position=f'{_CENTER_X_POS_BAR_HORIZONTAL} {PLATFORMS_CONFIG['height'] / 2} {_CENTER_Z_POS_BAR_HORIZONTAL}',
    depth=_CHART_DEPTH + PLATFORMS_CONFIG['additional_depth'],
    height=PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + PLATFORMS_CONFIG['additional_width'],
    color=PLATFORMS_CONFIG['color'],
)
bar_chart_horizontal = BASE.mark_bar().encode(x='sum(sales)', y='motor').properties(
    position=f'{_CENTER_X_POS_BAR_HORIZONTAL} {PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_CENTER_Z_POS_BAR_HORIZONTAL}',
    title='Horizontal bar chart',
)

charts.append(bar_platform_horizontal), charts.append(bar_chart_horizontal)

# Colored bar chart
_CENTER_X_POS_BAR_COLOR = -6
_CENTER_Z_POS_BAR_COLOR = -3

bar_platform_color = aframexr.Box(
    position=f'{_CENTER_X_POS_BAR_COLOR} {PLATFORMS_CONFIG['height'] / 2} {_CENTER_Z_POS_BAR_COLOR}',
    depth=_CHART_DEPTH + PLATFORMS_CONFIG['additional_depth'],
    height=PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + PLATFORMS_CONFIG['additional_width'],
    color=PLATFORMS_CONFIG['color'],
)
bar_chart_color = BASE.mark_bar().encode(x='model', y='sales', color='motor').properties(
    position=f'{_CENTER_X_POS_BAR_COLOR} {PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_CENTER_Z_POS_BAR_COLOR}',
    title='Color-Coded Bar Chart',
)

charts.append(bar_platform_color), charts.append(bar_chart_color)

# 3-axis bar chart
_CENTER_X_POS_BAR_3_AXES = 6
_CENTER_Z_POS_BAR_3_AXES = -3
ADDITIONAL_DEPTH = 1

bar_platform_3_axes = aframexr.Box(
    position=f'{_CENTER_X_POS_BAR_3_AXES} {PLATFORMS_CONFIG['height'] / 2} {_CENTER_Z_POS_BAR_3_AXES}',
    depth=_CHART_DEPTH + PLATFORMS_CONFIG['additional_depth'] + ADDITIONAL_DEPTH,
    height=PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + PLATFORMS_CONFIG['additional_width'],
    color=PLATFORMS_CONFIG['color'],
)
bar_chart_3_axes = BASE.mark_bar().encode(x='model', y='sales', z='color').properties(
    position=f'{_CENTER_X_POS_BAR_3_AXES} {PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_CENTER_Z_POS_BAR_3_AXES}',
    title='3-Axes Bar Chart', depth=_CHART_DEPTH + ADDITIONAL_DEPTH
)

charts.append(bar_platform_3_axes), charts.append(bar_chart_3_axes)

# === POINT CHARTS ===
# Simple point chart
_CENTER_X_POS_POINT_SIMPLE = 6
_CENTER_Z_POS_POINT_SIMPLE = 3

point_platform_simple = aframexr.Box(
    position=f'{_CENTER_X_POS_POINT_SIMPLE} {PLATFORMS_CONFIG['height'] / 2} {_CENTER_Z_POS_POINT_SIMPLE}',
    depth=_CHART_DEPTH + PLATFORMS_CONFIG['additional_depth'],
    height=PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + PLATFORMS_CONFIG['additional_width'],
    color=PLATFORMS_CONFIG['color'],
)
point_chart_simple = BASE.mark_point().encode(x='model', y='sales').properties(
    position=f'{_CENTER_X_POS_POINT_SIMPLE} {PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_CENTER_Z_POS_POINT_SIMPLE}',
    title='Simple point chart', depth=_CHART_DEPTH
)

charts.append(point_platform_simple), charts.append(point_chart_simple)

# Colored point chart
_CENTER_X_POS_POINT_COLOR = -6
_CENTER_Z_POS_POINT_COLOR = 3

point_platform_color = aframexr.Box(
    position=f'{_CENTER_X_POS_POINT_COLOR} {PLATFORMS_CONFIG['height'] / 2} {_CENTER_Z_POS_POINT_COLOR}',
    depth=_CHART_DEPTH + PLATFORMS_CONFIG['additional_depth'],
    height=PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + PLATFORMS_CONFIG['additional_width'],
    color=PLATFORMS_CONFIG['color'],
)
point_chart_color = BASE.mark_point().encode(x='model', y='sales', color='motor').properties(
    position=f'{_CENTER_X_POS_POINT_COLOR} {PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_CENTER_Z_POS_POINT_COLOR}',
    title='Color-Coded Point Chart',
)

charts.append(point_platform_color), charts.append(point_chart_color)

# Size point chart
_CENTER_X_POS_POINT_SIZE = -6
_CENTER_Z_POS_POINT_SIZE = -9

point_platform_size = aframexr.Box(
    position=f'{_CENTER_X_POS_POINT_SIZE} {PLATFORMS_CONFIG['height'] / 2} {_CENTER_Z_POS_POINT_SIZE}',
    depth=_CHART_DEPTH + PLATFORMS_CONFIG['additional_depth'],
    height=PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + PLATFORMS_CONFIG['additional_width'],
    color=PLATFORMS_CONFIG['color'],
)
point_chart_size = BASE.mark_point().encode(x='model', y='sales', size='doors').properties(
    position=f'{_CENTER_X_POS_POINT_SIZE} {PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_CENTER_Z_POS_POINT_SIZE}',
    title='Size-Coded Point Chart',
)
charts.append(point_platform_size), charts.append(point_chart_size)

# Dynamic filtered bar chart
_CENTER_X_POS_BAR_DYNAMIC_FILTER = -10
_CENTER_X_POS_PIE_DYNAMIC_FILTER = 0
_CENTER_Z_POS_DYNAMIC_FILTER = -25

bar_platform_dynamic_filter = aframexr.Box(
    position=f'{_CENTER_X_POS_BAR_DYNAMIC_FILTER} {PLATFORMS_CONFIG['height'] / 2} {_CENTER_Z_POS_DYNAMIC_FILTER}',
    depth=_CHART_DEPTH + PLATFORMS_CONFIG['additional_depth'],
    height=PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + PLATFORMS_CONFIG['additional_width'],
    color=PLATFORMS_CONFIG['color'],
)
chart_dynamic_filter_param = aframexr.selection_point('param', ['motor'])
bar_chart_dynamic_filter = BASE.mark_bar().encode(x='motor', y='sum(sales)').properties(
    position=f'{_CENTER_X_POS_BAR_DYNAMIC_FILTER} {PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_CENTER_Z_POS_DYNAMIC_FILTER}',
    title='Dynamic filter bar chart',
).add_params(chart_dynamic_filter_param)

_PIE_DYNAMIC_FILTER_RADIUS = 2.5
pie_platform_dynamic_filter = aframexr.Box(
    position=f'{_CENTER_X_POS_PIE_DYNAMIC_FILTER} {PLATFORMS_CONFIG['height'] / 2} {_CENTER_Z_POS_DYNAMIC_FILTER}',
    depth=_CHART_DEPTH + PLATFORMS_CONFIG['additional_depth'],
    height=PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + PLATFORMS_CONFIG['additional_width'],
    color=PLATFORMS_CONFIG['color'],
)
pie_chart_dynamic_filter = BASE.mark_arc(radius=2.5).encode(color='model', theta='sales').properties(
    position=f'{_CENTER_X_POS_PIE_DYNAMIC_FILTER} {PLATFORMS_CONFIG['height'] + _PIE_DYNAMIC_FILTER_RADIUS} {_CENTER_Z_POS_DYNAMIC_FILTER}',
    title='Dynamic filter pie chart'
).transform_filter(chart_dynamic_filter_param)

charts.append(bar_platform_dynamic_filter), charts.append(bar_chart_dynamic_filter)
charts.append(pie_platform_dynamic_filter), charts.append(pie_chart_dynamic_filter)

scene = room
for c in charts:
    scene += c

scene.save('data-demo.html')
