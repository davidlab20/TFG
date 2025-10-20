import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import babiaAltair
    import json


    with open('./data.json') as file:
        dataJSON = json.load(file)  # Data from JSON file to a list of dictionaries
    return babiaAltair, dataJSON


@app.cell
def _(babiaAltair, dataJSON):
    pieChart = babiaAltair.Chart(dataJSON).mark_arc().encode(theta='model', color='sales')
    pieChart.show()
    return (pieChart,)


@app.cell
def _(babiaAltair, dataJSON):
    barsChart = babiaAltair.Chart(dataJSON).mark_bar().encode(x='model', y='sales')
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
def _(babiaAltair, barsChart, pieChart):
    # Concatenation of charts
    finalChart3 = babiaAltair.XConcatChart(top_left=pieChart, top_right=barsChart, bottom_left=barsChart,
                                           bottom_right=pieChart)
    finalChart3.show()
    return


if __name__ == "__main__":
    app.run()
