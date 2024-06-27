import marimo

__generated_with = "0.6.22"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __():
    # zmenme hodnotu x, ba potom zrusme tuto bunku
    x = 1
    print(x)
    return x,


@app.cell
def __(x):
    # vykona sa automaticky, ak sa zmeni predch. bunka
    y = x + 1
    print(y)
    return y,


@app.cell
def __(mo):
    mesiace = mo.ui.slider(start=1, stop=12, show_value=True, label="Mesiace")
    mesiace
    return mesiace,


@app.cell
def __(mesiace, mo):
    mo.md(f"Mesiac = {mesiace.value}")
    return


if __name__ == "__main__":
    app.run()
