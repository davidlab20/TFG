import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Aggregated data notebook**
    """)
    return


@app.cell
def _():
    import aframexr
    return (aframexr,)


@app.cell
def _(aframexr):
    csv_data = aframexr.URLData('https://davidlab20.github.io/TFG/examples/data/aggregate_data.csv')
    return (csv_data,)


@app.cell
def _(aframexr, csv_data):
    non_aggregate_chart = aframexr.Chart(csv_data, position='-8 0 -10').mark_bar().encode(x='model', y='sales')
    non_aggregate_chart.show()
    return


@app.cell
def _(aframexr, csv_data):
    aggregate_chart1 = aframexr.Chart(csv_data, position='-8 0 -10').mark_bar().encode(x='model', y='mean(sales)')
    aggregate_chart1.show()
    return


@app.cell
def _(aframexr, csv_data):
    aggregate_chart2 = aframexr.Chart(csv_data, position='-8 0 -10').mark_bar().encode(x='model', y='mean_sales').transform_aggregate(
        mean_sales='mean(sales)',  # Must be the same name as in encoding()
    )
    aggregate_chart2.show()
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
