import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium", app_title="Get started")


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

    return (aframexr,)


@app.cell
def _(aframexr):
    # Load the data having the URL of the JSON file
    url = "https://raw.githubusercontent.com/davidlab20/TFG/main/docs/static/data/data.json"
    data = aframexr.URLData(url)  # Create an URLData object

    # Create the chart
    chart = aframexr.Chart(data, position="0 2 -5").mark_bar().encode(x="model", y="sales")

    # Display the chart in the notebook
    chart  # Can also use chart.show()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
