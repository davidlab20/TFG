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

_PLATFORMS_CONFIG = {'height': 0.3, 'additional_depth': 4, 'additional_width': 2, 'color': 'darkSlateGray'}

charts = []

# Chart 1
_CHART_1_DEPTH = 2
_CHART_1_HEIGHT = 4
_CHART_1_WIDTH = 6

_GROUND_CENTER_POS_X_1 = -10
_GROUND_CENTER_POS_Z = -15

_INFO_BOX_1_DEPTH = 0.1
_INFO_BOX_1_HEIGHT = 1.5
_INFO_BOX_1_WIDTH = 3

platform_1 = aframexr.Box(
    position=f'{_GROUND_CENTER_POS_X_1} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_1_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_1_WIDTH + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
chart_1 = aframexr.Chart(
    data,
    position=f'{_GROUND_CENTER_POS_X_1} {_PLATFORMS_CONFIG['height'] + _CHART_1_HEIGHT / 2} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_1_DEPTH, height=_CHART_1_HEIGHT, width=_CHART_1_WIDTH
).mark_bar().encode(x='model', y='sales')

title_box = aframexr.Plane(
    position=f'{_GROUND_CENTER_POS_X_1} {_PLATFORMS_CONFIG['height'] + _CHART_1_HEIGHT + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    width=_CHART_1_WIDTH,
    color='white',
)
title_text = aframexr.Text(
    'BAR CHART',
    position=f'{_GROUND_CENTER_POS_X_1} {_PLATFORMS_CONFIG['height'] + _CHART_1_HEIGHT + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    align='center',
    color='black',
    scale='1.5 1.5 1.5',
)

charts.append(platform_1), charts.append(chart_1), charts.append(title_box), charts.append(title_text)

# Chart 2
_CHART_2_DEPTH = 0.5
_CHART_2_RADIUS = 2

_GROUND_CENTER_POS_X_2 = 0

platform_2 = aframexr.Box(
    position=f'{_GROUND_CENTER_POS_X_2} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_2_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_2_RADIUS + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
chart_2 = aframexr.Chart(
    data,
    position=f'{_GROUND_CENTER_POS_X_2} {_PLATFORMS_CONFIG['height'] + _CHART_2_RADIUS + 0.1} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_2_DEPTH
).mark_arc(radius=_CHART_2_RADIUS).encode(color='model', theta='sales')

title_box = aframexr.Plane(
    position=f'{_GROUND_CENTER_POS_X_2} {_PLATFORMS_CONFIG['height'] + _CHART_2_RADIUS * 2 + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    width=_CHART_2_RADIUS * 2,
    color='white',
)
title_text = aframexr.Text(
    'PIE CHART',
    position=f'{_GROUND_CENTER_POS_X_2} {_PLATFORMS_CONFIG['height'] + _CHART_2_RADIUS * 2 + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    align='center',
    color='black',
    scale='1.5 1.5 1.5',
)

charts.append(platform_2), charts.append(chart_2), charts.append(title_box), charts.append(title_text)

# Chart 3
_CHART_3_DEPTH = 1
_CHART_3_HEIGHT = 4
_CHART_3_WIDTH = 6

_GROUND_CENTER_POS_X_3 = 10

platform_3 = aframexr.Box(
    position=f'{_GROUND_CENTER_POS_X_3} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_3_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_3_WIDTH + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
chart_3 = aframexr.Chart(
    data,
    position=f'{_GROUND_CENTER_POS_X_3} {_PLATFORMS_CONFIG['height'] + _CHART_3_HEIGHT / 2} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_3_DEPTH, height=_CHART_3_HEIGHT, width=_CHART_3_WIDTH
).mark_point().encode(x='model', y='sales')

title_box = aframexr.Plane(
    position=f'{_GROUND_CENTER_POS_X_3} {_PLATFORMS_CONFIG['height'] + _CHART_3_HEIGHT + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    width=_CHART_3_WIDTH,
    color='white',
)
title_text = aframexr.Text(
    'POINT CHART',
    position=f'{_GROUND_CENTER_POS_X_3} {_PLATFORMS_CONFIG['height'] + _CHART_3_HEIGHT + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    align='center',
    color='black',
    scale='1.5 1.5 1.5',
)

charts.append(platform_3), charts.append(chart_3), charts.append(title_box), charts.append(title_text)

# Title
main_plane = aframexr.Plane(
    position=f'0 {_PLATFORMS_CONFIG['height'] + _CHART_1_HEIGHT + 0.2 + 0.5 + 2} {_GROUND_CENTER_POS_Z}',
    height=2, width=25,
)
main_text = aframexr.Text(
    'SIMPLE CHARTS',
    position=f'0 {_PLATFORMS_CONFIG['height'] + _CHART_1_HEIGHT + 0.2 + 0.5 + 2} {_GROUND_CENTER_POS_Z}',
    align='center',
    scale='7 7 7',
    color='black',
)
charts.append(main_plane), charts.append(main_text)

# ===== SCENE =====
scene = room
for chart in charts:
    scene += chart

scene.save('demo.html')
