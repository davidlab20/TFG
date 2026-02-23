import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium", app_title="Rotated charts notebook")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Rotated charts notebook**
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

    data = aframexr.URLData('https://raw.githubusercontent.com/davidlab20/TFG/main/static/data/data.json')
    return aframexr, data


@app.cell
def _(aframexr, data):
    non_rotated_chart = aframexr.Chart(data, position='0 2 -5', depth=1).mark_point(size=0.4).encode(x='model', y='sales')
    non_rotated_chart.show()
    return


@app.cell
def _(aframexr, data):
    # Rotation format is 'x y z' in degrees
    rotated_chart = aframexr.Chart(data, position='0 2 -6', rotation='10 -20 10', depth=1).mark_point(size=0.4).encode(x='model', y='sales')
    rotated_chart.show()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
