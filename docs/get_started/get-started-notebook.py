import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Get started**
    """)
    return


@app.cell
def _():
    # Import the library in a separate cell
    import aframexr
    return (aframexr,)


@app.cell
def _(aframexr):
    # Load the data having the URL of the JSON file
    url = "https://davidlab20.github.io/TFG/examples/data/data.json"
    data = aframexr.URLData(url)  # Create an URLData object

    # Create the chart
    chart = aframexr.Chart(data, position="0 5 -11").mark_bar().encode(x='model', y='sales')

    # Display the chart in the notebook
    chart  # Can also use chart.show()
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
