import marimo

__generated_with = "0.17.0"
app = marimo.App()


@app.cell
def _():
    import babiaxr.components as babiaxr


    data = """
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
    return babiaxr, data


@app.cell
def _(babiaxr, data):
    # Pie chart with data as string
    pieChart = babiaxr.Chart(data).mark_arc().encode(theta='model', color='sales')
    pieChart.show()
    return


@app.cell
def _(babiaxr):
    # Pie chart with data as JSON file
    pieChartJSON = babiaxr.Chart('./data.json').mark_arc().encode(theta='model', color='sales')
    pieChartJSON.show()
    return


@app.cell
def _(babiaxr, data):
    # Bars chart with data as string
    barsChart = babiaxr.Chart(data).mark_bar().encode(x='model', y='sales')
    barsChart.show()
    return


@app.cell
def _(babiaxr):
    # Bars chart with data as JSON file
    barsChartJSON = babiaxr.Chart('./data.json').mark_bar().encode(x='model', y='sales')
    barsChartJSON.show()
    return


if __name__ == "__main__":
    app.run()
