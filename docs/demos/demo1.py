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

_CHART_DEPTH = 2
_CHART_HEIGHT = 4
_CHART_WIDTH = 6
BASE = aframexr.Chart(data, depth=_CHART_DEPTH, height=_CHART_HEIGHT, width=_CHART_WIDTH)

_PLATFORMS_CONFIG = {'height': 0.2, 'additional_depth': 4, 'additional_width': 2, 'color': 'darkSlateGray'}

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
bar_chart = BASE.mark_bar().encode(x='model', y='sales').properties(
    position=f'{_CENTER_X_POS_BAR} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_GROUND_CENTER_POS_Z}'
)

bar_title_box = aframexr.Plane(
    position=f'{_CENTER_X_POS_BAR} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT + 0.7} {_GROUND_CENTER_POS_Z}',
    width=_CHART_WIDTH,
    color='white',
)
bar_title_text = aframexr.Text(
    'BAR CHART',
    position=f'{_CENTER_X_POS_BAR} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT + 0.7} {_GROUND_CENTER_POS_Z}',
    align='center',
    color='black',
    scale='1.5 1.5 1.5',
)

charts.append(bar_platform), charts.append(bar_chart), charts.append(bar_title_box), charts.append(bar_title_text)

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
    position=f'{_CENTER_X_POS_PIE} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_GROUND_CENTER_POS_Z}'
)

pie_title_box = aframexr.Plane(
    position=f'{_CENTER_X_POS_PIE} {_PLATFORMS_CONFIG['height'] + _CHART_2_RADIUS * 2 + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    width=_CHART_2_RADIUS * 2,
    color='white',
)
pie_title_text = aframexr.Text(
    'PIE CHART',
    position=f'{_CENTER_X_POS_PIE} {_PLATFORMS_CONFIG['height'] + _CHART_2_RADIUS * 2 + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    align='center',
    color='black',
    scale='1.5 1.5 1.5',
)

charts.append(pie_platform), charts.append(pie_chart), charts.append(pie_title_box), charts.append(pie_title_text)

# Chart 3
_CENTER_X_POS_POINT = 10

point_platform = aframexr.Box(
    position=f'{_CENTER_X_POS_POINT} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z}',
    depth=_CHART_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_CHART_WIDTH + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
point_chart = BASE.mark_point(size=0.4).encode(x='model', y='sales').properties(
    position=f'{_CENTER_X_POS_POINT} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT / 2} {_GROUND_CENTER_POS_Z}'
)

point_title_box = aframexr.Plane(
    position=f'{_CENTER_X_POS_POINT} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    width=_CHART_WIDTH,
    color='white',
)
point_title_text = aframexr.Text(
    'POINT CHART',
    position=f'{_CENTER_X_POS_POINT} {_PLATFORMS_CONFIG['height'] + _CHART_HEIGHT + 0.2 + 0.5} {_GROUND_CENTER_POS_Z}',
    align='center',
    color='black',
    scale='1.5 1.5 1.5',
)

charts.append(point_platform), charts.append(point_chart), charts.append(point_title_box), charts.append(point_title_text)

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

# ===== ELEMENTS =====
_GROUND_CENTER_POS_Z_ELEMENTS = -5
_ELEMENTS_COLOR = 'lightBlue'

elements = [
    aframexr.Box(position=f'-15 1 {_GROUND_CENTER_POS_Z_ELEMENTS}'),
    aframexr.Cone(position=f'-12 1 {_GROUND_CENTER_POS_Z_ELEMENTS}'),
    aframexr.Cylinder(position=f'-9 1 {_GROUND_CENTER_POS_Z_ELEMENTS}'),
    aframexr.Dodecahedron(position=f'-6 1 {_GROUND_CENTER_POS_Z_ELEMENTS}'),
    aframexr.GLTF(
        'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/refs/heads/main/Models/AntiqueCamera/glTF/AntiqueCamera.gltf',
        position=f'-'
    ),
    aframexr.Icosahedron(),
    aframexr.Image('https://raw.githubusercontent.com/davidlab20/TFG/main/docs/static/imgs/logo.png'),
    aframexr.Octahedron(),
    aframexr.Plane(),
    aframexr.Sphere(),
    aframexr.Tetrahedron(),
    aframexr.Text('Simple text'),
    aframexr.Torus()
]

# Box
_BOX_CENTER_X_POS = -10
_BOX_DEPTH = _BOX_HEIGHT = _BOX_WIDTH = 2

box_platform = aframexr.Box(
    position=f'{_BOX_CENTER_X_POS} {_PLATFORMS_CONFIG['height'] / 2} {_GROUND_CENTER_POS_Z_ELEMENTS}',
    depth=_BOX_DEPTH + _PLATFORMS_CONFIG['additional_depth'],
    height=_PLATFORMS_CONFIG['height'],
    width=_BOX_WIDTH + _PLATFORMS_CONFIG['additional_width'],
    color=_PLATFORMS_CONFIG['color'],
)
box = aframexr.Box(
    position=f'{_BOX_CENTER_X_POS} {_PLATFORMS_CONFIG['height'] + _BOX_HEIGHT / 2} {_GROUND_CENTER_POS_Z_ELEMENTS}',
    depth=_BOX_DEPTH, height=_BOX_HEIGHT, width=_BOX_WIDTH,
    color=_ELEMENTS_COLOR,
)

# ===== SCENE =====
scene = room
for chart in charts:
    scene += chart
scene += box_platform + box

scene.save('demo.html')
