import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium", app_title="Simple charts notebook")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Simple charts notebook**
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
    import json
    import urllib.request  # To import files from web


    data_str = """
        [{"model": "leon", "motor": "electric", "color": "red",
        "doors": 5, "sales": 10},
        {"model": "ibiza", "motor": "electric", "color": "white",
        "doors": 3, "sales": 15},
        {"model": "cordoba", "motor": "diesel", "color": "black",
        "doors": 5, "sales": 3},
        {"model": "toledo", "motor": "diesel", "color": "white",
        "doors": 5, "sales": 18},
        {"model": "altea", "motor": "diesel", "color": "red",
        "doors": 5, "sales": 4},
        {"model": "arosa", "motor": "electric", "color": "red",
        "doors": 3, "sales": 12},
        {"model": "alhambra", "motor": "diesel", "color": "white",
        "doors": 5, "sales": 5},
        {"model": "600", "motor": "gasoline", "color": "yellow",
        "doors": 3, "sales": 20},
        {"model": "127", "motor": "gasoline", "color": "white",
        "doors": 5, "sales": 2},
        {"model": "panda", "motor": "gasoline", "color": "black",
        "doors": 3, "sales": 13}]
    """
    data = aframexr.Data.from_json(data_str)  # Raw data
    url_data = aframexr.URLData('https://davidlab20.github.io/TFG/examples/data/data.json')
    return aframexr, data, json, url_data, urllib


@app.cell
def _(aframexr, data):
    # Pie chart with data as Data object
    pieChart = aframexr.Chart(data, position='0 2 -5').mark_arc().encode(color='model', theta='sales')
    pieChart.show()
    return


@app.cell
def _(aframexr, url_data):
    # Pie chart with data as URLData object
    pieChartJSON = aframexr.Chart(url_data, position='0 2 -5').mark_arc().encode(color='model', theta='sales')
    pieChartJSON.show()
    return


@app.cell
def _(aframexr, data):
    # Bars chart with data as Data object
    barsChart = aframexr.Chart(data, position='0 2 -5').mark_bar().encode(x='model', y='sales')
    barsChart.show()
    return


@app.cell
def _(aframexr, url_data):
    # Bars chart with data as URLData object
    barsChartJSON = aframexr.Chart(url_data, position='0 2 -5').mark_bar().encode(x='model', y='sales')
    barsChartJSON.show()
    return


@app.cell
def _(aframexr, json, urllib):
    # Import a chart from a JSON file storing the specifications of the chart
    with urllib.request.urlopen("https://davidlab20.github.io/TFG/examples/data/simple_chart.json") as json_chart:
        json_specs = json.load(json_chart)

    imported_chart = aframexr.Chart.from_dict(json_specs)
    imported_chart.show()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
