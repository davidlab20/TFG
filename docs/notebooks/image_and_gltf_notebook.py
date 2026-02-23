import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium", app_title="Image and GLTF notebook")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # **Images and GLTF notebook**
    """)
    return


@app.cell(hide_code=True)
async def _():
    # Install the necessary packages only when running in WASM (browser) mode.
    import sys

    if sys.platform == 'emscripten':  # WASM mode
        import micropip
        await micropip.install(['aframexr', 'wcwidth'])
    return


@app.cell
def _():
    import aframexr

    return (aframexr,)


@app.cell
def _(aframexr):
    image_url = 'https://raw.githubusercontent.com/davidlab20/TFG/main/docs/static/imgs/logo.png'

    image = aframexr.Image(image_url, position='0 2 -5', height=3, width=3)
    image.show()
    return


@app.cell
def _(aframexr):
    gltf_url ='https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/refs/heads/main/Models/AntiqueCamera/glTF/AntiqueCamera.gltf'

    gltf = aframexr.GLTF(gltf_url, position='0 0 -4', rotation='0 30 0', scale='0.5 0.5 0.5')
    gltf.show()
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
