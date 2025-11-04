import marimo

__generated_with = "0.17.2"
app = marimo.App()


@app.cell(hide_code=True)
async def _():
    # Import the package from GitHub
    # IMPORTANT: do not change this cell code
    import micropip
    await micropip.install("https://davidlab20.github.io/TFG/dist/babiaxr-2025.11.4-py3-none-any.whl")
    return


@app.cell
def _():
    import babiaxr


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
    return babiaxr, data


@app.cell
def _(babiaxr, data):
    pieChart = babiaxr.Chart(data).mark_arc().encode(theta='model', color='sales')
    pieChart.show()
    return (pieChart,)


@app.cell
def _(babiaxr, data):
    barsChart = babiaxr.Chart(data).mark_bar().encode(x='model', y='sales')
    barsChart.show()
    return (barsChart,)


@app.cell
def _(barsChart, pieChart):
    # Vertical concatenation of charts
    # Can use:
        # finalChart = pieChart & barsChart
        # finalChart = pieChart.vconcat(barsChart)
        # finalChart = babiaAltair.VConcatChart(pieChart, barsChart)
    finalChart = pieChart & barsChart
    finalChart.show()
    return


@app.cell
def _(pieChart):
    # The main chart does not change (the concatenation of charts stores copies of charts)
    pieChart.show()
    return


@app.cell
def _(barsChart, pieChart):
    # Horizontal concatenation of charts
    # Can use:
        # finalChart2 = pieChart | barsChart
        # finalChart2 = pieChart.concat(barsChart)
        # finalChart2 = pieChart.hconcat(barsChart)
        # finalChart2 = babiaAltair.HConcatChart(pieChart, barsChart)
    finalChart2 = pieChart | barsChart
    finalChart2.show()
    return


@app.cell
def _(barsChart):
    # The main chart does not change (the concatenation of charts stores copies of charts)
    barsChart.show()
    return


@app.cell
def _(babiaxr, barsChart, pieChart):
    # Concatenation of charts
    finalChart3 = babiaxr.XConcatChart(top_left=pieChart, top_right=barsChart,
                                       bottom_left=barsChart, bottom_right=pieChart)
    finalChart3.show()
    return


if __name__ == "__main__":
    app.run()
