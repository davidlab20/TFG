import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
async def _():
    import marimo as mo

    # Install the necessary packages only when running in WASM (browser) mode.
    import sys

    if sys.platform == 'emscripten':  # WASM mode
        import micropip
        await micropip.install(['aframexr', 'wcwidth'])
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Usability Evaluation of AFrameXR**

    Welcome to this usability study of AFrameXR. This experiment focuses on visualization and interaction in desktop, VR and AR using scenes created with AFrameXR.

    You will need a device compatible with VR and AR (if you are on desktop you can also do the experiment, but the experience will not be the same).

    Please run all cells using the "Run All" button located in the bottom-right corner (it might last a couple of minutes, depending on the computer) and install the necessary dependencies.

    ## <u>What will you do?</u>

    - Complete a series of small visualization tasks
    - Answer a few short questions

    ## <u>Duration</u>

    This experiment will take approximately 5 minutes.

    ## <u>After finishing</u>

    When you are done:

    👉 Please complete the following form:
    https://forms.gle/4Wn3v2vwYoz8DZB86
    """)
    return


@app.cell
def _():
    import aframexr
    from aframexr.datasets import data
    import pandas as pd

    # Load example dataset (AFrameXR Data object)
    chart_data = data.cars()

    # Convert to pandas DataFrame to easily preview
    df_pd = pd.DataFrame(chart_data.values)

    # Show first rows
    df_pd.head()
    return aframexr, df_pd


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## <u>Before Starting</u>

    Read the instructions below to learn how to interact with the scenes depending on the mode you are using.

    - Desktop:
        - **Entering the scene:** Click in the bottom-right corner icon of the scene.
        - **Moving in the scene:** Use the <code>WASD</code> keys of the keyboard to move, arrow keys can also be used. Click and drag the mouse to rotate the camera.
        - **Leaving the scene:** Press the <code>Esc</code> key in the keyboard.

    - VR:
        - **Entering the scene:** Press the <code>VR icon</code> in the bottom-right corner of the scene (if you have a compatible device).
        - **Moving in the scene:** Use the joysticks to move and rotate the camera (left joystick for movement, right joystick for camera rotation).
        - **Leaving the scene:** Hold your device's <code>Menu button</code> and return to the previous screen.

    - AR:
        - **Entering the scene:** Press the <code>AR icon</code> in the bottom-right corner of the scene (if you have a compatible device).
        - **Placing the scene:** Use the <code>trigger button</code> of the controller to place the scene in your room. You can only place the scene once to avoid interaction issues. Exit the scene if you need to reposition the charts.
        - **Moving in the scene:** Just stand up and move around your room.
        - **Leaving the scene:** Hold your device's <code>menu button</code> and return to the previous screen.

    You can interact with the charts by clicking and hovering on the elements. Click on the bars chart to see the changes on the pie chart.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## <u>Desktop and VR</u>

    The following scene has been made with this code (you can modify the code in order to change the visualizations):
    """)
    return


@app.cell
def _(aframexr, df_pd):
    BASE = aframexr.Chart(df_pd, depth=1)

    param = aframexr.selection_point('param', ['motor'])
    charts = (
        # Base bar chart
        BASE.mark_bar().encode(x='motor', y='sum(sales)').properties(title='Sales by motor', position='-3 2 -5').add_params(param)

        +

        # Dynamic pie chart
        BASE.mark_arc().encode(color='model', theta='sales').properties(position='3 2 -5').transform_filter(param)
    )

    charts
    return BASE, param


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## <u>AR</u>

    A compatible device is required to visualize this scene in AR mode. The following scene has been made with this code (you can modify the code in order to change the visualizations):
    """)
    return


@app.cell
def _(BASE, param):
    charts_ar = (
        # Base bar chart
        BASE.mark_bar().encode(x='motor', y='sum(sales)').properties(title='Sales by motor', position='0 2 0').add_params(param)

        +

        # Dynamic pie chart
        BASE.mark_arc().encode(color='model', theta='sales').properties(position='4 2 0').transform_filter(param)
    )

    # Show scene
    charts_ar.show(ar_scale='0.075 0.075 0.075')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## **Feedback**

    Thank you for participating.

    Please complete the form at the beginning of the study.
    """)
    return


if __name__ == "__main__":
    app.run()
