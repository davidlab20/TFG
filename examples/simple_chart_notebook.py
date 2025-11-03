import marimo

__generated_with = "0.17.2"
app = marimo.App()


@app.cell(hide_code=True)
async def _():
    # Import the package from GitHub
    # IMPORTANT: do not change this cell code
    import micropip
    await micropip.install('https://davidlab20.github.io/TFG/dist/babiaxr-2025.11.3-py3-none-any.whl')
    return


@app.cell
def _():
    import babiaxr
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
    data = babiaxr.Data.from_json(data_str)  # Raw data
    url_data = babiaxr.URLData('./data.json')  # URL of the data
    return babiaxr, data, json, url_data, urllib


@app.cell
def _(babiaxr, data):
    # Pie chart with data as Data object
    pieChart = babiaxr.Chart(data).mark_arc().encode(theta='model', color='sales')
    pieChart.show()
    return


@app.cell
def _(babiaxr, url_data):
    # Pie chart with data as URLData object
    pieChartJSON = babiaxr.Chart(url_data).mark_arc().encode(theta='model', color='sales')
    pieChartJSON.show()
    return


@app.cell
def _(babiaxr, data):
    # Bars chart with data as Data object
    barsChart = babiaxr.Chart(data).mark_bar().encode(x='model', y='sales')
    barsChart.show()
    return


@app.cell
def _(babiaxr, url_data):
    # Bars chart with data as URLData object
    barsChartJSON = babiaxr.Chart(url_data).mark_bar().encode(x='model', y='sales')
    barsChartJSON.show()
    return


@app.cell
def _(babiaxr, json, urllib):
    # Import a chart from a JSON file storing the specifications of the chart
    with urllib.request.urlopen("https://davidlab20.github.io/TFG/examples/chart.json") as json_chart:
        json_specs = json.load(json_chart)

    imported_chart = babiaxr.Chart.from_dict(json_specs)
    imported_chart.show()
    return


if __name__ == "__main__":
    app.run()
