import marimo

__generated_with = "0.17.2"
app = marimo.App()


@app.cell
def _():
    import babiaxr
    import json

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
    data = babiaxr.Data.from_json(data_str)
    return babiaxr, data, json


@app.cell
def _(babiaxr, json):
    with open('./chart.json') as file:
        json_specs = json.load(file)

    chart = babiaxr.Chart.from_dict(json_specs)
    chart.show()
    return


@app.cell
def _(babiaxr, data):
    chart1 = babiaxr.Chart(data).mark_arc().encode(theta='model', color='sales')
    chart2 = babiaxr.Chart.from_json(chart1.to_json())
    assert chart1.__class__ == chart2.__class__
    assert chart1.to_dict() == chart2.to_dict()
    assert chart1.to_html() == chart2.to_html()
    assert chart1.to_json() == chart2.to_json()
    return


@app.cell
def _(babiaxr, json):
    with open('./data.json') as file_data:
        data_json = json.load(file_data)
        data2 = babiaxr.Data(data_json)

    bars = babiaxr.Chart(data2).mark_bar().encode(x='model', y='sales')
    bars.show()
    return (bars,)


@app.cell
def _(bars):
    filtered_bar = bars.transform_filter('datum.motor=diesel')
    filtered_bar.show()
    return


if __name__ == "__main__":
    app.run()
