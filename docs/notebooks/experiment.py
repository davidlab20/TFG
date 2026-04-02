import marimo

__generated_with = "0.22.0"
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
    - size: doors (take into account that doors is a **quantitative** value, but nominal is needed)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### <u>Task 5 — 3D Filtered Bar chart</u>

    Create a 3D filtered Bar chart:

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
    You should see something like this:
    """)
    return


@app.cell(hide_code=True)
def _(sol_task5):
    sol_task5
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## High-level tasks
    """)
    return


@app.cell(hide_code=True)
def _(mo, task6_url):
    mo.md(f"""
    ### <u>Task 6 — 3D Line chart with several lines</u>

    Create a 3D Line chart:

    - data's URL: {task6_url} (TIP: look at the objects that Chart() receives)
    - using point markers
    - x: year (take into account that year is a **quantitative** value)
    - y: sales
    - color: model
    """)
    return


@app.cell
def _():
    # Write your code here
    task6_url = "https://cdn.jsdelivr.net/gh/davidlab20/TFG@main/docs/static/data/model_year_sales.json"
    return (task6_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    You should see something like this:
    """)
    return


@app.cell(hide_code=True)
def _(sol_task6):
    sol_task6
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Complex tasks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### <u>Task 7 — 3D Dynamic filtered chart</u>

    Create a parameter with point selection (filtered when click):

    - name: "param" (you can use another)
    - fields: motor

    Create the 3D main chart (Bar chart):

    - color of all the bars: green (no the same as color encoding)
    - x: motor
    - y: sum(sales)
    - add the parameter created before

    Create the 3D dynamic filtered chart (Pie chart):

    - color: model
    - theta: sales
    - filter transformation: the parameter created before

    Add both charts in the same scene

    **TIPS:**

    - charts may have different positions so they can be watched correctly
    - click on the main chart to see the dynamic filtering
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
def _(sol_task7):
    sol_task7
    return


@app.cell(hide_code=True)
def _(aframexr, df_pd, task6_url):
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

    # Task 5
    sol_task5 = base.mark_bar().encode(
        x="model",
        y="sales"
    ).transform_filter("datum.motor == 'diesel'")

    # Task 6
    sol_task6 = base.mark_line(point=True).encode(
        x="year:N",
        y="sales",
        color="model"
    ).properties(data=aframexr.UrlData(task6_url))

    # Task 7
    param_task7 = aframexr.selection_point(
        name="param",
        fields=["motor"]
    )

    main_task7 = base.mark_bar(color="green").encode(
        x="motor",
        y="sum(sales)"
    ).add_params(param_task7).properties(
        position="-3 2 -6"
    )
    filtered_task7 = base.mark_arc().encode(
        color="model",
        theta="sales"
    ).transform_filter(param_task7).properties(
        position="3 2 -6"
    )

    sol_task7 = main_task7 + filtered_task7
    return (
        sol_task1,
        sol_task2,
        sol_task3,
        sol_task4,
        sol_task5,
        sol_task6,
        sol_task7,
    )


if __name__ == "__main__":
    app.run()
