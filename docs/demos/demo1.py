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

_GROUND_CENTER_POS_X_1 = -9
_GROUND_CENTER_POS_Z_1 = -8

_INFO_BOX_1_DEPTH = 0.1
_INFO_BOX_1_HEIGHT = 1.5
_INFO_BOX_1_WIDTH = 3

platform_1 = aframexr.Box(
    position=f'{_GROUND_CENTER_POS_X_1} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z_1}',
    depth=_CHART_1_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_1_WIDTH + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
chart_1 = aframexr.Chart(
    data,
    position=f'{_GROUND_CENTER_POS_X_1} {_PLATFORMS_CONFIG['height'] + _CHART_1_HEIGHT / 2} {_GROUND_CENTER_POS_Z_1}',
    depth=_CHART_1_DEPTH, height=_CHART_1_HEIGHT, width=_CHART_1_WIDTH
).mark_bar().encode(x='model', y='sales')

info_box_pos = [
    _GROUND_CENTER_POS_X_1 + _CHART_1_WIDTH / 2 + _PLATFORMS_CONFIG['additional_width'],
    _INFO_BOX_1_HEIGHT / 2 + _PLATFORMS_CONFIG['height'],
    _GROUND_CENTER_POS_Z_1 + _CHART_1_DEPTH / 2 + _PLATFORMS_CONFIG["additional_depth"] / 2 - _INFO_BOX_1_DEPTH / 2
]
info_box = aframexr.Box(
    position=f'{info_box_pos[0]} {info_box_pos[1]} {info_box_pos[2]}',
    depth=_INFO_BOX_1_DEPTH, height=_INFO_BOX_1_HEIGHT, width=_INFO_BOX_1_WIDTH,
)
info_text = aframexr.Text(
    'TIP:\n\nPlace mouse on bars to\ndisplay more information.',
    position=f'{info_box_pos[0]} {info_box_pos[1]} {info_box_pos[2] + _INFO_BOX_1_DEPTH / 2}',
    align='center',
    color='black',
)
title_box = aframexr.Plane(
    position=f'{_GROUND_CENTER_POS_X_1} {_PLATFORMS_CONFIG['height'] + _CHART_1_HEIGHT + 0.2 + 0.5} {_GROUND_CENTER_POS_Z_1}',
    width=_CHART_1_WIDTH,
    color='white',
)
title_text = aframexr.Text(
    'Simple bar chart',
    position=f'{_GROUND_CENTER_POS_X_1} {_PLATFORMS_CONFIG['height'] + _CHART_1_HEIGHT + 0.2 + 0.5} {_GROUND_CENTER_POS_Z_1}',
    align='center',
    color='black',
    scale='1.5 1.5 1.5',
)

charts.append(platform_1), charts.append(chart_1), charts.append(info_box), charts.append(info_text), charts.append(title_box), charts.append(title_text)

# Chart 2
_CHART_2_DEPTH = 1
_CHART_2_HEIGHT = 4
_CHART_2_WIDTH = 6

_GROUND_CENTER_POS_X_2 = 7
_GROUND_CENTER_POS_Z_2 = -8

_INFO_BOX_2_DEPTH = 0.1
_INFO_BOX_2_HEIGHT = 2
_INFO_BOX_2_WIDTH = 3

platform_2 = aframexr.Box(
    position=f'{_GROUND_CENTER_POS_X_2} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z_2}',
    depth=_CHART_2_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_2_WIDTH + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
chart_2 = aframexr.Chart(
    data,
    position=f'{_GROUND_CENTER_POS_X_2} {_PLATFORMS_CONFIG['height'] + _CHART_2_HEIGHT / 2} {_GROUND_CENTER_POS_Z_2}',
    depth=_CHART_2_DEPTH, height=_CHART_2_HEIGHT, width=_CHART_2_WIDTH
).mark_point().encode(x='model', y='sales')

info_box_pos = [
    _GROUND_CENTER_POS_X_2 + _CHART_2_WIDTH / 2 + _PLATFORMS_CONFIG['additional_width'],
    _INFO_BOX_2_HEIGHT / 2 + _PLATFORMS_CONFIG['height'],
    _GROUND_CENTER_POS_Z_2 + _CHART_2_DEPTH / 2 + _PLATFORMS_CONFIG["additional_depth"] / 2 - _INFO_BOX_2_DEPTH / 2
]
info_box = aframexr.Box(
    position=f'{info_box_pos[0]} {info_box_pos[1]} {info_box_pos[2]}',
    depth=_INFO_BOX_2_DEPTH, height=_INFO_BOX_2_HEIGHT, width=_INFO_BOX_2_WIDTH,
)
info_text = aframexr.Text(
    'Simple point chart.\n\n\nRaycaster:\nPlace mouse on spheres to\ndisplay more information.',
    position=f'{info_box_pos[0]} {info_box_pos[1]} {info_box_pos[2] + _INFO_BOX_2_DEPTH / 2}',
    align='center',
    color='black',
)

charts.append(platform_2), charts.append(chart_2), charts.append(info_box), charts.append(info_text)

# ===== SCENE =====
scene = room
for chart in charts:
    scene += chart

scene.save('demo.html')
