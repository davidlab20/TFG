import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium", app_title="Simple elements notebook")


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    # **Simple elements notebook**
    """)
    return


@app.cell(hide_code=True)
async def _():
    # Install the necessary packages only when running in WASM (browser) mode.
    import sys

    if sys.platform == 'emscripten':  # WASM mode
        import micropip
        await micropip.install(['aframexr', 'wcwidth'])
    return


@app.cell
def _():
    import aframexr

    return (aframexr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Box
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Depth
    box_depth_slider = mo.ui.slider(start=1, stop=5, step=1)
    box_depth_hstack = mo.hstack([mo.md("Depth:"), box_depth_slider])

    # Height
    box_height_slider = mo.ui.slider(start=1, stop=5, step=1)
    box_height_hstack = mo.hstack([mo.md("Height:"), box_height_slider])

    # Width
    box_width_slider = mo.ui.slider(start=1, stop=5, step=1)
    box_width_hstack = mo.hstack([mo.md("Width:"), box_width_slider])

    mo.vstack(
        [box_depth_hstack, box_height_hstack, box_width_hstack],
        align='start'
    )
    return box_depth_slider, box_height_slider, box_width_slider


@app.cell
def _(aframexr, box_depth_slider, box_height_slider, box_width_slider):
    box = aframexr.Box(
        position=f'0 {box_height_slider.value / 2} -4',  # The box is on the ground
        depth=box_depth_slider.value,
        height=box_height_slider.value,
        width=box_width_slider.value,
        color='lightBlue'
    )
    box
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Cone
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Height
    cone_height_slider = mo.ui.slider(start=2, stop=5, step=1)
    cone_height_hstack = mo.hstack([mo.md("Height:"), cone_height_slider])

    # Bottom's radius
    cone_radius_bottom_slider = mo.ui.slider(start=1, stop=2, step=1)
    cone_radius_bottom_hstack = mo.hstack([mo.md("Bottom's radius:"), cone_radius_bottom_slider])

    # Top's radius
    cone_radius_top_slider = mo.ui.slider(start=0.01, stop=2, step=1)
    cone_radius_top_hstack = mo.hstack([mo.md("Top's radius:"), cone_radius_top_slider])

    mo.vstack(
        [cone_height_hstack, cone_radius_bottom_hstack, cone_radius_top_hstack],
        align='start'
    )
    return (
        cone_height_slider,
        cone_radius_bottom_slider,
        cone_radius_top_slider,
    )


@app.cell
def _(
    aframexr,
    cone_height_slider,
    cone_radius_bottom_slider,
    cone_radius_top_slider,
):
    cone = aframexr.Cone(
        position=f'0 {cone_height_slider.value / 2} -4',  # The cone is on the ground
        height=cone_height_slider.value,
        radius_bottom=cone_radius_bottom_slider.value,
        radius_top=cone_radius_top_slider.value,
        color='lightBlue'
    )
    cone
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Cylinder
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Height
    cylinder_height_slider = mo.ui.slider(start=1, stop=3, step=1)
    cylinder_height_hstack = mo.hstack([mo.md("Height:"), cylinder_height_slider])

    # Radius
    cylinder_radius_slider = mo.ui.slider(start=1, stop=2, step=0.5)
    cylinder_radius_hstack = mo.hstack([mo.md("Radius:"), cylinder_radius_slider])

    mo.vstack(
        [cylinder_height_hstack, cylinder_radius_hstack],
        align='start'
    )
    return cylinder_height_slider, cylinder_radius_slider


@app.cell
def _(aframexr, cylinder_height_slider, cylinder_radius_slider):
    cylinder = aframexr.Cylinder(
        position=f'0 {cylinder_height_slider.value / 2} -4',  # The cylinder is on the ground
        height=cylinder_height_slider.value,
        radius=cylinder_radius_slider.value,
        color='lightBlue'
    )
    cylinder
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Dodecahedron
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Radius
    dodecahedron_radius_slider = mo.ui.slider(start=1, stop=2, step=0.5)
    dodecahedron_radius_hstack = mo.hstack([mo.md("Radius:"), dodecahedron_radius_slider])

    mo.vstack([dodecahedron_radius_hstack], align='start')
    return (dodecahedron_radius_slider,)


@app.cell
def _(aframexr, dodecahedron_radius_slider):
    dodecahedron = aframexr.Dodecahedron(
        position=f'0 {dodecahedron_radius_slider.value} -4',
        radius=dodecahedron_radius_slider.value,
        color='lightBlue'
    )
    dodecahedron
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Icosahedron
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Radius
    icosahedron_radius_slider = mo.ui.slider(start=1, stop=2, step=0.5)
    icosahedron_radius_hstack = mo.hstack([mo.md("Radius:"), icosahedron_radius_slider])

    mo.vstack([icosahedron_radius_hstack], align='start')
    return (icosahedron_radius_slider,)


@app.cell
def _(aframexr, icosahedron_radius_slider):
    icosahedron = aframexr.Icosahedron(
        position=f'0 {icosahedron_radius_slider.value} -4',
        radius=icosahedron_radius_slider.value,
        color='lightBlue'
    )
    icosahedron
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Octahedron
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Radius
    octahedron_radius_slider = mo.ui.slider(start=1, stop=2, step=0.5)
    octahedron_radius_hstack = mo.hstack([mo.md("Radius:"), octahedron_radius_slider])

    mo.vstack([octahedron_radius_hstack], align='start')
    return (octahedron_radius_slider,)


@app.cell
def _(aframexr, octahedron_radius_slider):
    octahedron = aframexr.Octahedron(
        position=f'0 {octahedron_radius_slider.value} -4',
        radius=octahedron_radius_slider.value,
        color='lightBlue'
    )
    octahedron
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Plane
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Height
    plane_height_slider = mo.ui.slider(start=1, stop=5, step=1)
    plane_height_hstack = mo.hstack([mo.md("Height:"), plane_height_slider])

    # Width
    plane_width_slider = mo.ui.slider(start=1, stop=5, step=1)
    plane_width_hstack = mo.hstack([mo.md("Width:"), plane_width_slider])

    mo.vstack(
        [plane_height_hstack, plane_width_hstack],
        align='start'
    )
    return plane_height_slider, plane_width_slider


@app.cell
def _(aframexr, plane_height_slider, plane_width_slider):
    plane = aframexr.Plane(
        position=f'0 {plane_height_slider.value / 2} -4',
        height=plane_height_slider.value,
        width=plane_width_slider.value,
        color='lightBlue'
    )
    plane
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Sphere
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Radius
    sphere_radius_slider = mo.ui.slider(start=1, stop=2, step=0.5)
    sphere_radius_hstack = mo.hstack([mo.md("Radius:"), sphere_radius_slider])

    mo.vstack([sphere_radius_hstack], align='start')
    return (sphere_radius_slider,)


@app.cell
def _(aframexr, sphere_radius_slider):
    sphere = aframexr.Sphere(
        position=f'0 {sphere_radius_slider.value} -4',
        radius=sphere_radius_slider.value,
        color='lightBlue'
    )
    sphere
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Tetrahedron
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Radius
    tetrahedron_radius_slider = mo.ui.slider(start=1, stop=2, step=0.5)
    tetrahedron_radius_hstack = mo.hstack([mo.md("Radius:"), tetrahedron_radius_slider])

    mo.vstack([tetrahedron_radius_hstack], align='start')
    return (tetrahedron_radius_slider,)


@app.cell
def _(aframexr, tetrahedron_radius_slider):
    tetrahedron = aframexr.Tetrahedron(
        position=f'0 {tetrahedron_radius_slider.value} -4',
        radius=tetrahedron_radius_slider.value,
        color='lightBlue'
    )
    tetrahedron
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Text
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Value
    text_value = mo.ui.text(value='Introduce some text')
    text_value_hstack = mo.hstack([mo.md("Text:"), text_value])

    # Align
    text_align = mo.ui.radio(options={'left': 'left', 'center': 'center', 'right': 'right'}, value='center', inline=True)
    text_align_hstack = mo.hstack([mo.md("Align:"), text_align])

    mo.vstack(
        [text_value_hstack, text_align_hstack],
        align='start'
    )
    return text_align, text_value


@app.cell
def _(aframexr, text_align, text_value):
    text = aframexr.Text(
        text_value.value,
        position=f'0 2 -4',
        align=text_align.value,
        color='black',
        scale='2 2 2'
    )
    text
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## Torus
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Radius
    torus_radius_slider = mo.ui.slider(start=1, stop=2, step=0.5)
    torus_radius_hstack = mo.hstack([mo.md("Radius:"), torus_radius_slider])

    # Radius tubular
    torus_radius_tubular_slider = mo.ui.slider(start=0.1, stop=0.5, step=0.2)
    torus_radius_tubular_hstack = mo.hstack([mo.md("Radius tubular:"), torus_radius_tubular_slider])

    mo.vstack(
        [torus_radius_hstack, torus_radius_tubular_hstack],
        align='start'
    )
    return torus_radius_slider, torus_radius_tubular_slider


@app.cell
def _(aframexr, torus_radius_slider, torus_radius_tubular_slider):
    torus = aframexr.Torus(
        position=f'0 {torus_radius_slider.value} -4',
        radius=torus_radius_slider.value,
        radius_tubular=torus_radius_tubular_slider.value,
        color='lightBlue'
    )
    torus
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    All this elements can be concatenated with other elements or charts, using concatenation with '+'.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
