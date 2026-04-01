import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Usability Evaluation of AFrameXR**

    Welcome

    In this experiment, you will use AFrameXR to create 3D data visualizations.

    ## <u>Objective</u>

    The goal of this study is to evaluate the usability and clarity of the library's syntax.

    ## <u>What will you do?</u>

    - Complete a series of small visualization tasks
    - Write and execute code
    - Answer a few short questions

    ## <u>Duration</u>

    This experiment will take approximately 10-15 minutes.

    ## <u>Important</u>

    - This is not a test
    - You are allowed to make mistakes
    - We are interested in your experience, not correctness
    """)
    return


@app.cell
def _():
    import aframexr
    from aframexr.datasets import data
    import pandas as pd

    # Load example dataset (AFrameXR Data object)
    chart_data = data.cars()

    # Convert to pandas DataFrame to easily preview
    df_pd = pd.DataFrame(chart_data.values)

    # Show first rows
    df_pd.head()
    return aframexr, df_pd


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## **Example task**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### <u>Task 0</u>

    Create a 3D bars chart:

    - x: model
    - y: sales
    - color: motor

    You can see how the chart is created and the syntax of AFrameXR.
    Try to understand how the code works; the next tasks will not show the solution.
    """)
    return


@app.cell
def _(aframexr, df_pd):
    # Solution
    aframexr.Chart(df_pd, position="0 2 -5").mark_bar().encode(
        x="model",
        y="sales",
        color="motor"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## **Easy tasks**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### <u>Task 1 — 3D Scatter plot</u>

    Create a 3D scatter plot:

    - x: model
    - y: sales
    - color: motor
    """)
    return


@app.cell
def _():
    # Write your code here


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    You should see something like this:
    """)
    return


@app.cell(hide_code=True)
def _(sol_task1):
    sol_task1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### <u>Task 2 — 3D Pie chart</u>

    Create a 3D pie chart:

    - color: model
    - theta: sales
    """)
    return


@app.cell
def _():
    # Write your code here


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    You should see something like this:
    """)
    return


@app.cell(hide_code=True)
def _(sol_task2):
    sol_task2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Medium-level tasks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### <u>Task 3 — 3D Histogram</u>

    Create a 3D Histogram:

    - x: motor
    - y: count()
    """)
    return


@app.cell
def _():
    # Write your code here


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    You should see something like this:
    """)
    return


@app.cell(hide_code=True)
def _(sol_task3):
    sol_task3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### <u>Task 4 — 3D Bubble plot</u>

    Create a 3D bubble plot:

    - x: model
    - y: sales
    - color: motor
    - size: doors (take into account that doors is a **quantitative** value)
    """)
    return


@app.cell
def _():
    # Write your code here


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    You should see something like this:
    """)
    return


@app.cell(hide_code=True)
def _(sol_task4):
    sol_task4
    return


@app.cell
def _(aframexr, df_pd):
    # ===== Solutions =====

    global_position = '0 2 -5'  # Position for every chart (for good visualization)
    base = aframexr.Chart(df_pd, position=global_position)

    # Task 1
    sol_task1 = base.mark_point().encode(
        x="model",
        y="sales",
        color="motor"
    )

    # Task 2
    sol_task2 = base.mark_arc().encode(
        color="model",
        theta="sales"
    )

    # Task 3
    sol_task3 = base.mark_bar().encode(
        x="motor",
        y="count()"
    )

    # Task 4
    sol_task4 = base.mark_point().encode(
        x="model",
        y="sales",
        color="motor",
        size="doors:Q"
    )
    return sol_task1, sol_task2, sol_task3, sol_task4


if __name__ == "__main__":
    app.run()
