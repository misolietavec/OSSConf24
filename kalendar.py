import marimo

__generated_with = "0.6.22"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    import calendar as cal
    return cal, mo


@app.cell
def __(mo):
    # radio tlacidla pre rozsah rokov
    rozsahy = {"1900-1949": (1900, 1949), "1950-1999": (1950, 1999), "2000-2025": (2000, 2025)}
    rozsah_rokov = mo.ui.radio(options=rozsahy, value="2000-2025", inline=True)
    return rozsah_rokov, rozsahy


@app.cell
def __(mo, rozsah_rokov):
    # posuvniky pre mesiace a roky, posuvnik pre roky je zavisly od hodnoty rozsah_rokov
    start_rok, stop_rok = rozsah_rokov.value
    mesiace = mo.ui.slider(start=1, stop=12, show_value=True, label="Mesiace")
    roky = mo.ui.slider(start=start_rok, stop=stop_rok, show_value=True, label="Roky")
    return mesiace, roky, start_rok, stop_rok


@app.cell
def __(cal, mesiace, mo, roky):
    koncovy_den = cal.monthrange(roky.value, mesiace.value)[1]
    # posuvnik dni zavisi od posuvnikov roky, mesiace
    dni = mo.ui.slider(start=1, stop=koncovy_den, value=koncovy_den, show_value=True, label="Dni")
    return dni, koncovy_den


@app.cell
def __(cal, dni, mesiace, roky):
    week_dict = {0: "Pondelok", 1: "Utorok", 2: "Streda", 3: "Štvrtok", 4: "Piatok", 5: "Sobota", 6: "Nedeľa"}
    # den_tyzdna zavisi od vsetkych troch posuvnikov
    den_tyzdna = week_dict[cal.weekday(roky.value, mesiace.value, dni.value)]
    return den_tyzdna, week_dict


@app.cell
def __(den_tyzdna, dni, mesiace, mo, roky, rozsah_rokov):
    mo.vstack(
        [mo.md("#Skorovečný kalendár"), rozsah_rokov, mo.hstack([roky, mesiace, dni]), mo.md(f"### Deň v týždni: {den_tyzdna}")],
        align="center",
    )
    return


if __name__ == "__main__":
    app.run()
