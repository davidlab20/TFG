import aframexr

# ===== SPACE CONFIGURATION =====
ROOM_DEPTH = 25
ROOM_HEIGHT = 8
ROOM_WIDTH = 30

room = aframexr.Box(
    position=f'0 {ROOM_HEIGHT / 2 + 0.1} {-ROOM_DEPTH / 4}',
    depth=ROOM_DEPTH, height=ROOM_HEIGHT, width=ROOM_WIDTH,
    color='lightGreen'
)

# ===== CHARTS =====
data = aframexr.UrlData('https://cdn.jsdelivr.net/gh/davidlab20/TFG@main/docs/static/data/data.json')

_CHART_DEPTH = 1
_CHART_HEIGHT = 4
_CHART_WIDTH = 6
BASE = aframexr.Chart(data, depth=_CHART_DEPTH, height=_CHART_HEIGHT, width=_CHART_WIDTH)

_PLATFORMS_CONFIG = {'height': 0.2, 'additional_depth': 4, 'additional_width': 3, 'color': 'darkSlateGray'}

_GROUND_CENTER_POS_Z = -15

charts = []

# Bar chart
_CENTER_X_POS_BAR = -10

bar_platform = aframexr.Box(
    position=f'{_CENTER_X_POS_BAR} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
bar_chart = BASE.mark_bar(color='red').encode(x='model', y='sales').properties(
    position=f'{_CENTER_X_POS_BAR} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_GROUND_CENTER_POS_Z}',
    title='BAR CHART'
)

charts.append(bar_platform), charts.append(bar_chart)

# Chart 2
_CHART_2_RADIUS = 2
_CENTER_X_POS_PIE = 0

pie_platform = aframexr.Box(
    position=f'{_CENTER_X_POS_PIE} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_2_RADIUS + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
pie_chart = BASE.mark_arc(radius=_CHART_2_RADIUS).encode(color='model', theta='sales').properties(
    position=f'{_CENTER_X_POS_PIE} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_GROUND_CENTER_POS_Z}',
    title='PIE CHART'
)

charts.append(pie_platform), charts.append(pie_chart)

# Chart 3
_CENTER_X_POS_POINT = 10

point_platform = aframexr.Box(
    position=f'{_CENTER_X_POS_POINT} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
point_chart = BASE.mark_point(color='green').encode(x='model', y='sales').properties(
    position=f'{_CENTER_X_POS_POINT} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_GROUND_CENTER_POS_Z}',
    title='POINT CHART'
)

charts.append(point_platform), charts.append(point_chart)

# Title
main_plane = aframexr.Plane(
    position=f'0 {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT + 0.2 + 0.5 + 2} {_GROUND_CENTER_POS_Z}',
    height=2, width=25,
)
main_text = aframexr.Text(
    'SIMPLE CHARTS',
    position=f'0 {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT + 0.2 + 0.5 + 2} {_GROUND_CENTER_POS_Z}',
    align='center',
    scale='7 7 7',
    color='black',
)
charts.append(main_plane), charts.append(main_text)

# ===== CHARTS =====
scatter_platform = aframexr.Box(
    position=f'{0} {_PLATFORMS_CONFIG['height'] / 2} {-5}',
    depth=_CHART_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
scatter_plot = BASE.mark_point(size=0.35).encode(x='model', y='sales', color='motor').properties(
    position=f'0 {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} -5'
)

# ===== SCENE =====
scene = room + scatter_plot + scatter_platform
for chart in charts:
    scene += chart

scene.save('demo.html')
