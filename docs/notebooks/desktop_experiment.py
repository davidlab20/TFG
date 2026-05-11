import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
async def _():
    import marimo as mo

    # Install the necessary packages only when running in WASM (browser) mode.
    import sys

    if sys.platform == 'emscripten':  # WASM mode
        import micropip
        await micropip.install(['aframexr', 'wcwidth'])
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Ease of use Evaluation of AFrameXR**

    Welcome to this ease of use study of AFrameXR.

    In this experiment, you will use AFrameXR to create 3D data visualizations.

    Please run all cells and install the necessary dependencies.

    ## <u>Objective</u>

    The goal of this study is to evaluate the clarity of the library.

    ## <u>What will you do?</u>

    - Complete a series of small visualization tasks
    - Write and execute code
    - Answer a few short questions

    ## <u>Duration</u>

    This experiment will take approximately 10 minutes.

    ## <u>Important</u>

    - This is not an assessment
    - You are allowed to make mistakes
    - We are interested in your experience, not correctness
    - You are not required to complete all tasks. The goal is to explore the interface, so you may stop at any time or skip tasks if you prefer.

    ## <u>After finishing</u>

    When you are done:

    👉 Please complete the following form:
    https://forms.gle/Zj9DUUY3Ft4LNmM69
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
    ## <u>Example (Task 0)</u>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Create a 3D bars chart:

    - x: model
    - y: sales
    - color: motor

    You can see how the chart is created and the syntax of AFrameXR.
    Review the code to understand how the chart is constructed.
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
    ## <u>Easy Tasks</u>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### **Task 1 — 3D Scatter plot**

    Considering that the <code>mark_point()</code> method is used to define a scatter plot.

    Modify the task 0 code to create the following visualization:

    Scatter plot (position="0 2 -5"):

    - x: model
    - y: sales
    - color: motor
    - size: doors
    """)
    return


@app.cell
def _():
    # Write your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Expected output:
    """)
    return


@app.cell(hide_code=True)
def _(sol_task1):
    sol_task1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### **Task 2 — Histogram**

    Considering that the <code>count()</code> function is used inside the <code>encode()</code> method to count the number of occurrences in each category.

    Modify the code from Task 0 to create the following visualization:

    Bar chart (position="0 2 -5"):

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
    Expected output:
    """)
    return


@app.cell
def _(sol_task2):
    sol_task2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## <u>Medium-level tasks</u>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### **Task 3 — 3D Filtered Bar chart**

    Considering that the <code>transform_filter()</code> method is used to filter the data by applying a condition before visualization.

    Modify the code from Task 0 to create the following visualization:

    Bar chart (position="0 2 -5"):

    - x: model
    - y: sales
    - filter transformation: datum.motor == "diesel"
    """)
    return


@app.cell
def _():
    # Write your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Expected output:
    """)
    return


@app.cell(hide_code=True)
def _(sol_task3):
    sol_task3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## <u>Complex tasks</u>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### **Task 4 — 3D Dynamic filtered chart**

    <u>Step 1</u>

    Considering that a selection parameter enables interactive filtering based on user clicks, and can be created using <code>aframexr.selection_point()</code>.

    Create a parameter with point selection (filtered when click):

    - name: "param" (you can use another)
    - fields: motor

    <u>Step 2</u>

    Considering that the color of the chart can be directly specified in the <code>mark_bar()</code> method, using <code>mark_bar(color="...")</code>.

    You can add parameters to charts adding <code>.add_params()</code> method.

    Create the 3D main chart, Bar chart (position="-3 2 -6"):

    - color of all the bars: green (set via <code>mark_bar()</code>)
    - x: motor
    - y: sum(sales)
    - add the previously created parameter

    <u>Step 3</u>

    Considering that the <code>mark_arc()</code> method is used to define a Pie chart.

    Also considering that <code>.transform_filter()</code> method can receive the parameter created before.

    Create the 3D dynamic filtered chart, Pie chart (position="3 2 -6"):

    - color: model
    - theta: sales
    - filter transformation: the parameter created before

    <u>Step 4</u>

    Considering that you can add charts in the same scene using <code>+</code> operator (<code>chart1 + chart2 + chart3 + ...</code>).

    Add both charts in the same scene

    **TIPS:**

    - click on the main chart (Bar chart) to see the dynamic filtering
    """)
    return


@app.cell
def _():
    # Write your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Expected output:
    """)
    return


@app.cell(hide_code=True)
def _(sol_task4):
    sol_task4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## **Feedback**

    Thank you for participating.

    Please complete the form at the beginning of the study.
    """)
    return


@app.cell(hide_code=True)
def _(aframexr, df_pd):
    # ===== Solutions =====

    global_position = '0 2 -5'  # Position for every chart (for good visualization)
    base = aframexr.Chart(df_pd, position=global_position)

    # Task 1
    sol_task1 = base.mark_point().encode(
        x="model",
        y="sales",
        color="motor",
        size="doors"
    )

    # Task 2
    sol_task2 = base.mark_bar().encode(
        x="motor",
        y="count()"
    )

    # Task 3
    sol_task3 = base.mark_bar().encode(
        x="model",
        y="sales"
    ).transform_filter("datum.motor == 'diesel'")

    # Task 4
    param_task4 = aframexr.selection_point(
        name="param",
        fields=["motor"]
    )

    main_task4 = base.mark_bar(color="green").encode(
        x="motor",
        y="sum(sales)"
    ).add_params(param_task4).properties(
        position="-3 2 -6"
    )
    filtered_task4 = base.mark_arc().encode(
        color="model",
        theta="sales"
    ).transform_filter(param_task4).properties(
        position="3 2 -6"
    )

    sol_task4 = main_task4 + filtered_task4
    return sol_task1, sol_task2, sol_task3, sol_task4


if __name__ == "__main__":
    app.run()
