import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium", app_title="Aggregated data notebook")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Aggregated data notebook**
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

    return (aframexr,)


@app.cell
def _(aframexr):
    csv_data = aframexr.URLData('https://raw.githubusercontent.com/davidlab20/TFG/main/static/data/aggregate_data.csv')
    return (csv_data,)


@app.cell
def _(aframexr, csv_data):
    non_aggregate_chart = aframexr.Chart(csv_data, position='0 2 -5').mark_bar().encode(x='model', y='sales')
    non_aggregate_chart.show()
    return


@app.cell
def _(aframexr, csv_data):
    aggregate_chart1 = aframexr.Chart(csv_data, position='0 2 -5').mark_bar().encode(x='model', y='mean(sales)')
    aggregate_chart1.show()
    return


@app.cell
def _(aframexr, csv_data):
    aggregate_chart2 = aframexr.Chart(csv_data, position='0 2 -5').mark_bar().encode(x='model', y='mean_sales').transform_aggregate(
        mean_sales='mean(sales)',  # Must be the same name as used in the encoding() argument, order can change
    )
    aggregate_chart2.show()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
