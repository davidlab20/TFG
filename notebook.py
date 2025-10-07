import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    import babiaAltair
    import json


    data = """
        {"model": "leon", "motor": "electric", "color": "red",
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
        "doors": 3, "sales": 13}
    """

    with open('./data.json') as file:
        dataJSON = json.load(file)  # Data from JSON file to a list of dictionaries
    return babiaAltair, data, dataJSON


@app.cell
def _(babiaAltair, data):
    # Pie chart with data as string
    pieChart = babiaAltair.Chart(data).mark_arc().encode(theta='model', color='sales')
    pieChart.show()
    return


@app.cell
def _(babiaAltair, dataJSON):
    # Pie chart with data as JSON file
    pieChartJSON = babiaAltair.Chart(dataJSON).mark_arc().encode(theta='model', color='sales')
    pieChartJSON.show()
    return


@app.cell
def _(babiaAltair, data):
    # Bars chart with data as string
    barsChart = babiaAltair.Chart(data).mark_bar().encode(x='model', y='sales')
    barsChart.show()
    return


@app.cell
def _(babiaAltair, dataJSON):
    # Bars chart with data as JSON file
    barsChartJSON = babiaAltair.Chart(dataJSON).mark_bar().encode(x='model', y='sales')
    barsChartJSON.show()
    return


if __name__ == "__main__":
    app.run()
