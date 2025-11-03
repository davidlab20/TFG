import marimo

__generated_with = "0.17.2"
app = marimo.App()


@app.cell(hide_code=True)
async def _():
    # Import the package from GitHub
    # IMPORTANT: do not change this cell code
    import micropip
    await micropip.install("https://davidlab20.github.io/TFG/dist/babiaxr-2025.11.3-py3-none-any.whl")
    return


@app.cell
def _():
    # Import BabiaXR Python library in a separate cell
    import babiaxr
    return (babiaxr,)


@app.cell
def _(babiaxr):
    # Load the data having the URL of the JSON file
    url = "https://davidlab20.github.io/TFG/examples/data.json"
    data = babiaxr.URLData(url)  # Create an URLData object

    # Create the chart
    chart = babiaxr.Chart(data).mark_bar().encode(x='model', y='sales')

    # Display the chart in the notebook
    chart.show()
    return


if __name__ == "__main__":
    app.run()
