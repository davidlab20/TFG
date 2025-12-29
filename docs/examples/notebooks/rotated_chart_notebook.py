import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Rotated charts notebook**
    """)
    return


@app.cell
def _():
    import aframexr

    data = aframexr.URLData('https://davidlab20.github.io/TFG/examples/data/data.json')
    return aframexr, data


@app.cell
def _(aframexr, data):
    non_rotated_chart = aframexr.Chart(data, position='0 5 -11', depth=2).mark_point().encode(x='model', y='sales')
    non_rotated_chart.show()
    return


@app.cell
def _(aframexr, data):
    # Rotation format is 'x y z' in degrees
    rotated_chart = aframexr.Chart(data, position='0 5 -12', rotation='10 -20 10', depth=2).mark_point().encode(x='model', y='sales')
    rotated_chart.show()
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
