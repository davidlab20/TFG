import marimo

__generated_with = "0.17.0"
app = marimo.App()


@app.cell
def _():
    import babiaxr.components as babiaxr
    import json
    return babiaxr, json


@app.cell
def _(babiaxr, json):
    with open('./chart.json') as file:
        json_specs = json.load(file)

    chart = babiaxr.Chart.from_dict(json_specs)
    chart.show()
    return


@app.cell
def _(babiaxr):
    chart1 = babiaxr.Chart('./data.json').mark_arc().encode(theta='model', color='sales')
    chart2 = babiaxr.Chart.from_json(chart1.to_json())
    assert chart1.__class__ == chart2.__class__
    assert chart1.to_dict() == chart2.to_dict()
    assert chart1.to_html() == chart2.to_html()
    assert chart1.to_json() == chart2.to_json()
    return


@app.cell
def _(babiaxr, json):
    with open('./data.json') as file_data:
        data = json.load(file_data)

    bars = babiaxr.Chart(data).mark_bar().encode(x='model', y='sales')
    bars.show()
    return (bars,)


@app.cell
def _(bars):
    filtered_bar = bars.transform_filter('datum.motor=diesel')
    filtered_bar.show()
    return


if __name__ == "__main__":
    app.run()
