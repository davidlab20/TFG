import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Performance comparison between [Altair](https://altair-viz.github.io/) and AFrameXR**
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    This notebook compares the performance of Altair and AFrameXR.

    The objective is to evaluate **build time**, **serialization**, **exporting**, and **memory usage**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Benchmark Setup
    """)
    return


@app.cell
def _():
    import numpy as np
    np.random.seed(0)
    import pandas as pd

    sizes = [10, 20, 50, 100, 250, 500, 1000, 2000, 5000]
    REPEATS = 10

    def generate_dataset(n):
        return pd.DataFrame({
            'x': np.random.rand(n),
            'y': np.random.rand(n),
            'cat': np.random.choice(['A', 'B', 'C'], size=n)
        })

    dataframes = {n: generate_dataset(n) for n in sizes}
    return REPEATS, dataframes, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Comparison
    """)
    return


@app.cell
def _():
    import aframexr as af
    import altair as alt

    def create_chart(data, lib):
        if lib == 'AFrameXR':
            return af.Chart(data).mark_bar(color='green').encode(
                x='x', y='y', color='cat'
            )

        if lib == 'Altair':
            return alt.Chart(data).mark_bar(color='green').encode(
                x='x', y='y', color='cat'
            )

    return alt, create_chart


@app.cell
def _(create_chart):
    import gc
    import json
    import time, tracemalloc

    def measure_phase(func):
        gc.collect()
        tracemalloc.start()

        t0 = time.perf_counter()
        result = func()
        t1 = time.perf_counter()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return (t1 - t0, peak, result)

    def measure(df, lib):
        build_time, build_mem, chart = measure_phase(
            lambda: create_chart(df, lib)
        )

        serialize_time, serialize_mem, spec = measure_phase(
            lambda: chart.to_dict()
        )

        spec_size = len(json.dumps(spec, sort_keys=True, separators=(",", ":")))

        export_time, export_mem, html = measure_phase(
            lambda: chart.to_html()
        )

        return {
            'lib': lib,
            'build_time': build_time,
            'serialize_time': serialize_time,
            'export_time': export_time,
            'build_mem': build_mem,
            'serialize_mem': serialize_mem,
            'export_mem': export_mem,
            'spec_size': spec_size
        }

    return gc, measure


@app.cell
def _(create_chart, dataframes, gc):
    # WARMUP
    libs = ['AFrameXR', 'Altair']

    for df in dataframes.values():
        for l in libs:
            chart = create_chart(df, l)
            chart.to_dict()
            chart.to_html()
            del chart
            gc.collect()
    return (libs,)


@app.cell
def _(REPEATS, dataframes, gc, libs, measure):
    import os

    results = []
    gc.collect()

    for n, data in dataframes.items():
        for _ in range(REPEATS):
            for lib in libs:
                results.append({
                    'n': n,
                    **measure(data, lib)
                })
    return (results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Results
    """)
    return


@app.cell
def _(alt, pd, results):
    df_res = pd.DataFrame(results)

    summary = df_res.groupby(['n', 'lib']).median(numeric_only=True).reset_index()

    num_cols = summary.select_dtypes(include='number').columns

    pivot = summary.pivot(index='n', columns='lib')

    alt_df = pivot.xs('Altair', level=1, axis=1)
    afr_df = pivot.xs('AFrameXR', level=1, axis=1)

    factor_ratio = pd.DataFrame({
        'n': pivot.index,

        'build_time_factor': alt_df['build_time'] / afr_df['build_time'],
        'serialize_time_factor': alt_df['serialize_time'] / afr_df['serialize_time'],
        'export_time_factor': alt_df['export_time'] / afr_df['export_time'],

        'build_mem_factor': alt_df['build_mem'] / afr_df['build_mem'],
        'serialize_mem_factor': alt_df['serialize_mem'] / afr_df['serialize_mem'],
        'export_mem_factor': alt_df['export_mem'] / afr_df['export_mem'],
    })

    num_cols = factor_ratio.select_dtypes(include='number').columns

    def make_result_chart(df, y, y_title):
        return alt.Chart(df).mark_line(point=alt.OverlayMarkDef(size=80), strokeWidth=3).encode(
            x=alt.X('n:Q', title='Dataset size [n]', scale=alt.Scale(type='log')),
            y=alt.Y(f'{y}:Q', title=y_title, scale=alt.Scale(type='log')),
            color=alt.Color(
                'lib:N',
                title='Library',
                scale=alt.Scale(
                    domain=['Altair', 'AFrameXR'],
                    range=['cornflowerblue', 'darkorange']
                ), legend=alt.Legend(
                    titleFontSize=18,
                    labelFontSize=14
                )
            ),
            tooltip=['n', 'lib', y]
        ).properties(
            width=370,
            height=250
        )

    def make_factor_chart(df, y):
        line = alt.Chart(df).mark_line(point=alt.OverlayMarkDef(size=80), strokeWidth=3).encode(
            x=alt.X('n:Q', title='Dataset size [n]'),
            y=alt.Y(f'{y}:Q', title='Overhead'),
            tooltip=['n', y]
        )

        rule = alt.Chart(df).mark_rule(
            color='red',
            strokeDash=[4,4]
        ).encode(
            y=alt.datum(1)
        )

        return (line + rule).properties(
            width=400,
            height=250
        )

    chart_build_time = make_result_chart(summary, 'build_time', 'Time [s]')
    chart_serialize_time = make_result_chart(summary, 'serialize_time', 'Time [s]')
    chart_export_time = make_result_chart(summary, 'export_time', 'Time [s]')

    chart_build_mem = make_result_chart(summary, 'build_mem', 'Memory [bytes]')
    chart_serialize_mem = make_result_chart(summary, 'serialize_mem', 'Memory [bytes]')
    chart_export_mem = make_result_chart(summary, 'export_mem', 'Memory [bytes]')

    chart_factor_time_build = make_factor_chart(factor_ratio, 'build_time_factor')
    chart_factor_mem_build = make_factor_chart(factor_ratio, 'build_mem_factor')

    chart_factor_time_serialize = make_factor_chart(factor_ratio, 'serialize_time_factor')
    chart_factor_mem_serialize = make_factor_chart(factor_ratio, 'serialize_mem_factor')

    chart_factor_time_export = make_factor_chart(factor_ratio, 'export_time_factor')
    chart_factor_mem_export = make_factor_chart(factor_ratio, 'export_mem_factor')
    return (
        chart_build_mem,
        chart_build_time,
        chart_export_mem,
        chart_export_time,
        chart_factor_mem_build,
        chart_factor_mem_export,
        chart_factor_mem_serialize,
        chart_factor_time_build,
        chart_factor_time_export,
        chart_factor_time_serialize,
        chart_serialize_mem,
        chart_serialize_time,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Build
    """)
    return


@app.cell
def _(chart_build_mem, chart_build_time):
    chart_build_time.properties(title='Build Time') | chart_build_mem.properties(title='Build Memory')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Serialize
    """)
    return


@app.cell
def _(chart_serialize_mem, chart_serialize_time):
    chart_serialize_time.properties(title='Serialize Time') | chart_serialize_mem.properties(title='Serialize Memory')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Export
    """)
    return


@app.cell
def _(chart_export_mem, chart_export_time):
    chart_export_time.properties(title='Export Time') | chart_export_mem.properties(title='Export Memory')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Ratios
    """)
    return


@app.cell
def _(alt, chart_factor_mem_build, chart_factor_time_build):
    (
        chart_factor_time_build.properties(title='Slowdown Factor (Altair / AFrameXR)') | 
        chart_factor_mem_build.properties(title='Memory Ratio (Altair / AFrameXR)')
    ).properties(title=alt.Title('Build Phase', fontSize=16, anchor='middle', offset=20))
    return


@app.cell
def _(alt, chart_factor_mem_serialize, chart_factor_time_serialize):
    (
        chart_factor_time_serialize.properties(title='Slowdown Factor (Altair / AFrameXR)') | 
        chart_factor_mem_serialize.properties(title='Memory Ratio (Altair / AFrameXR)')
    ).properties(title=alt.Title('Serialize Phase', fontSize=16, anchor='middle', offset=20))
    return


@app.cell
def _(alt, chart_factor_mem_export, chart_factor_time_export):
    (
        chart_factor_time_export.properties(title='Slowdown Factor (Altair / AFrameXR)') | 
        chart_factor_mem_export.properties(title='Memory Ratio (Altair / AFrameXR)')
    ).properties(title=alt.Title('Export Phase', fontSize=16, anchor='middle', offset=20))
    return


if __name__ == "__main__":
    app.run()
