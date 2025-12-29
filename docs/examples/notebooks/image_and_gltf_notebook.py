import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Images and GLTF notebook**
    """)
    return


@app.cell
def _():
    import aframexr
    return (aframexr,)


@app.cell
def _(aframexr):
    image_url = aframexr.URLData('https://davidlab20.github.io/TFG/imgs/logo.png')

    image_chart = aframexr.Chart(image_url, position='0 4 -5').mark_image(height=4, width=4)
    image_chart.show()
    return


@app.cell
def _(aframexr):
    gltf_url = aframexr.URLData(
        url='https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/refs/heads/main/Models/AntiqueCamera/glTF/AntiqueCamera.gltf'
    )

    gltf_chart = aframexr.Chart(gltf_url, position='0 0 -15', rotation='0 30 0').mark_gltf(scale='2 2 2')
    gltf_chart.show()
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
