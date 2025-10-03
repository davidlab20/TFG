import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    import babiaAltair
    import marimo as mo


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
    return babiaAltair, data, mo


@app.cell
def _(babiaAltair, data, mo):
    # Pie chart
    pieChart = babiaAltair.Chart(data).mark_arc().encode(theta='model', color='sales')
    mo.iframe(pieChart.html)
    return


@app.cell
def _(babiaAltair, data, mo):
    # Bars chart
    barsChart = babiaAltair.Chart(data).mark_bar().encode(x='model', y='sales')
    mo.iframe(barsChart.html)
    return


if __name__ == "__main__":
    app.run()
