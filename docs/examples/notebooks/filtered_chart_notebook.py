import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Filtered charts notebook**
    """)
    return


@app.cell
def _():
    import aframexr
    import json
    import urllib.request


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
    data = aframexr.Data.from_json(data_str)
    return aframexr, data, json, urllib


@app.cell
def _(aframexr, json, urllib):
    # Import a filtered chart from a JSON file storing the specifications of the chart
    with urllib.request.urlopen("https://davidlab20.github.io/TFG/examples/data/filt_chart.json") as json_chart:
        json_specs = json.load(json_chart)

    imported_chart = aframexr.Chart.from_dict(json_specs)
    imported_chart.show()
    return


@app.cell
def _(aframexr, data):
    chart1 = aframexr.Chart(data).mark_arc().encode(color='model', theta='sales')
    chart2 = aframexr.Chart.from_json(chart1.to_json())
    assert chart1.to_dict() == chart2.to_dict()
    assert chart1.to_html() == chart2.to_html()
    assert chart1.to_json() == chart2.to_json()
    return


@app.cell
def _(aframexr, json, urllib):
    with urllib.request.urlopen("https://davidlab20.github.io/TFG/examples/data/data.json") as file_data:
        data_json = json.load(file_data)
        data2 = aframexr.Data(data_json)

    bars = aframexr.Chart(data2, position='0 2 -5').mark_bar().encode(x='model', y='sales')
    bars.show()
    return (bars,)


@app.cell
def _(bars):
    filtered_bar = bars.transform_filter('datum.motor==diesel')
    filtered_bar.show()
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
