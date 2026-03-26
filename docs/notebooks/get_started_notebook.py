import marimo

__generated_with = "0.21.1"
app = marimo.App(app_title="Get started")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Get started**
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
    # Import the library in a separate cell
    import aframexr
    from aframexr.datasets import data

    return aframexr, data


@app.cell
def _(aframexr, data):
    # Load the data
    chart_data = data.cars()

    # Create the chart
    chart = aframexr.Chart(
        chart_data,
        position="0 2 -5"
    ).mark_bar().encode(
        x="model",
        y="sales",
        color="motor"
    )

    # Display the chart in the notebook
    chart  # Can also use chart.show()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
