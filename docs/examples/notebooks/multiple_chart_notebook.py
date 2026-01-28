import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Multiple charts notebook**
    """)
    return


@app.cell(hide_code=True)
async def _():
    # Install necessary packages only when running in WASM (browser) mode.
    import sys

    if sys.platform == 'emscripten':  # WASM mode
        import micropip
        await micropip.install(['aframexr', 'wcwidth'])
    return


@app.cell
def _():
    import aframexr


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
    return aframexr, data


@app.cell
def _(aframexr, data):
    pieChart = aframexr.Chart(data, position="-4 2 -4", depth=0.5).mark_arc().encode(color='model', theta='sales')
    pieChart.show()
    return (pieChart,)


@app.cell
def _(aframexr, data):
    barsChart = aframexr.Chart(data, position='3 2 -5').mark_bar().encode(x='model', y='sales')
    barsChart.show()
    return (barsChart,)


@app.cell
def _(barsChart, pieChart):
    # Concatenation of charts (add charts to the same scene)
    finalChart = pieChart + barsChart
    finalChart.show()
    return


@app.cell
def _(aframexr, data):
    # Concatenation of charts
    chart1 = aframexr.Chart(data, position='-4 5 -7', depth=1).mark_arc().encode(color='model', theta='sales')
    chart2 = aframexr.Chart(data, position='4 5 -7', depth=1).mark_arc().encode(color='model', theta='sales')
    chart3 = aframexr.Chart(data, position='-4 2 -7', depth=1).mark_arc().encode(color='model', theta='sales')
    chart4 = aframexr.Chart(data, position='4 2 -7', depth=1).mark_arc().encode(color='model', theta='sales')
    final_chart = chart1 + chart2 + chart3 + chart4
    final_chart.show()
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
