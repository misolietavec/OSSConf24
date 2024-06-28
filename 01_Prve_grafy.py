import marimo

__generated_with = "0.6.22"
app = marimo.App(width="full")


@app.cell
def __(mo):
    mo.md(
        """
        ### Na načítanie a spracovanie dát použijeme `polars` (nie `pandas`, ako je to obecne zvykom)
        ### Na kreslenie budeme používať modul `plotly`, konkrétne `plotly.express`, čo aj vám odporúčame.
        """
    )
    return


@app.cell
def __():
    import polars as pl
    import plotly.express as px
    import numpy as np
    return np, pl, px


@app.cell
def __(mo, pl):
    datafile = "data/nyc_taxi310k.parq"
    schema = pl.read_parquet_schema(datafile)
    popis_schemy = mo.md("#### Schéma dátového súboru (názvy stĺpcov a ich dátové typy):\n")
    mo.vstack([popis_schemy, schema])
    return datafile, popis_schemy, schema


@app.cell
def __(mo, pl):
    cols = ["pick_dt", "passengers", "fare"]
    df = pl.read_parquet("data/nyc_taxi310k.parq", columns=cols)
    mo.vstack([mo.md("#### Vyberieme len tri stĺpce, prvých niekoľko riadkov je:"), df.head()])
    return cols, df


@app.cell
def __(mo):
    mo.md(
        """
        ### Všetky dáta sú z januára 2015. Zoberme nástupy (pick).
        ### Chceme grafy po jednotlivých dňoch. Počet pasažierov, počet jázd.
        """
    )
    return


@app.cell
def __(df, pl):
    df_days = df.group_by(pl.col("pick_dt").dt.day().alias("Deň")).agg(pl.col("passengers").sum().alias("Cestujúci"))
    return df_days,


@app.cell
def __(df_days, mo):
    mo.vstack(["Prvých niekoľko riadkov z df_days:", df_days.head()])
    return


@app.cell
def __(mo):
    mo.md("### Nakreslíme stĺpcový graf, na osi x budú dni (1, 2, .... 31. jan.), na osi y počty cestujúcich")
    return


@app.cell
def __(df_days, px):
    pass_plot = px.bar(df_days, x="Deň", y="Cestujúci")
    pass_plot.update_layout(xaxis=dict(tickmode="array", tickvals=list(range(1, 32))))
    return pass_plot,


@app.cell
def __(mo):
    mo.md(
        """
        ## Čo za katastrófa sa stala 27. januára? Strašný pokles oproti iným dňom.
        ### Vidíme nejakú (približnú) periodicitu v dátach?
        ### Podobné grafy by sme chceli pre počty jázd.
        """
    )
    return


@app.cell
def __(df, pl):
    df_days_numfares = (
        df.group_by(pl.col("pick_dt").dt.day().alias("Deň"))
        .agg(Cestujúci=pl.col("passengers").sum(), Zárobok=pl.col("fare").sum(), Jazdy=pl.col("fare").count())
        .sort(by="Deň")
    )
    return df_days_numfares,


@app.cell
def __(df_days_numfares, mo):
    mo.vstack(["Datafrejma po dňoch", df_days_numfares.head()])
    return


@app.cell
def __(df_days_numfares, px):
    pass_fares_plot = px.bar(
        df_days_numfares,
        x="Deň",
        y=["Cestujúci", "Jazdy"],
        barmode="group",
        labels={"value": "Počet cestujúcich a jázd"},
    )
    pass_fares_plot.update_layout(xaxis=dict(tickmode="array", tickvals=list(range(1, 32))))
    return pass_fares_plot,


@app.cell
def __(mo):
    mo.md(
        """
        ### Grafy pre tie isté veličiny, no podľa hodín - to isté, len grupovanie podľa hodín.
        ### Jediná funkcia pre datafrejmu a aj pre graf podľa hodín i dní.
        """
    )
    return


@app.cell
def __(df, pl, px):
    def monthly_frame(frm, day=True):
        groupped = frm.group_by(pl.col("pick_dt").dt.day()) if day else frm.group_by(pl.col("pick_dt").dt.hour())
        column = "pick_day" if day else "pick_hour"
        df_month = groupped.agg(
            [
                pl.col("fare").sum().alias("Platby"),
                pl.col("passengers").sum().alias("Cestujúci"),
                pl.col("fare").count().alias("Jazdy"),
            ]
        ).sort(by="pick_dt")
        df_month = df_month.rename({"pick_dt": column})
        return df_month


    def monthly_plot(dhc):
        day = dhc == "Podľa dní"
        xcol = "pick_day" if day else "pick_hour"
        mframe = monthly_frame(df, day)
        xcol = "pick_day" if day else "pick_hour"
        xlabel = {"pick_day": "Deň", "pick_hour": "Hodina"}
        xticks = {"pick_day": list(range(1, 32)), "pick_hour": list(range(24))}
        pass_fares_plot = px.bar(
            mframe,
            x=xcol,
            y=["Cestujúci", "Jazdy"],
            barmode="group",
            labels={xcol: xlabel[xcol], "value": "Hodnoty", "variable": "Premenná"},
        )
        pass_fares_plot.update_layout(xaxis=dict(tickmode="array", tickvals=xticks[xcol]))
        return pass_fares_plot
    return monthly_frame, monthly_plot


@app.cell
def __(monthly_plot):
    monthly_plot("Podľa hodín")
    return


@app.cell
def __(mo):
    mo.md("### Nebolo by odveci, mať graf aj pre cestujúcich, jazdy podľa dní v týždni.")
    return


@app.cell
def __(df, pl):
    df_weekday_group = (
        df.group_by(pl.col("pick_dt").dt.weekday()).agg(pl.col("passengers").sum().alias("pass_count")).sort(by="pick_dt")
    )
    df_weekday = df_weekday_group.rename({"pick_dt": "pick_day"})
    return df_weekday, df_weekday_group


@app.cell
def __():
    from datetime import date

    print(date(2015, 1, 1).weekday())  # 0 - pondelok, ..., 6 - nedeľa
    # ale v polars dt.weekday je 1 - pondelok, ..., 7 - nedeľa
    return date,


@app.cell
def __(df_weekday, np, pl):
    pocty = np.array([4, 4, 4, 5, 5, 5, 4])  # preco?
    df_weekday_mean = df_weekday.with_columns(pl.col("pass_count") / pocty)
    df_weekday_mean
    return df_weekday_mean, pocty


@app.cell
def __(df_weekday_mean, px):
    graf = px.bar(df_weekday_mean, x="pick_day", y="pass_count", barmode="group", width=750, height=400)
    xtext = ["Pondelok", "Utorok", "Streda", "Štvrtok", "Piatok", "Sobota", "Nedeľa"]
    graf.update_layout(
        xaxis=dict(tickmode="array", tickvals=list(range(1, 8)), title="Deň v týždni", ticktext=xtext, tickangle=0),
        yaxis=dict(title="Priem. počet cestujúcich"),
    )
    return graf, xtext


@app.cell
def __(df, monthly_plot, np, pl, px):
    def week_plot(frm):
        df_weekday = (
            frm.group_by(pl.col("pick_dt").dt.weekday()).agg(pl.col("passengers").count().alias("pass_count")).sort(by="pick_dt")
        )
        df_weekday = df_weekday.rename({"pick_dt": "pick_day"})
        pocty = np.array([4, 4, 4, 5, 5, 5, 4])
        df_weekday = df_weekday.with_columns(pl.col("pass_count") / pocty)
        graf = px.bar(df_weekday, x="pick_day", y="pass_count", barmode="group", width=750, height=400)
        xtext = ["Pondelok", "Utorok", "Streda", "Štvrtok", "Piatok", "Sobota", "Nedeľa"]
        graf.update_layout(
            xaxis=dict(tickmode="array", tickvals=list(range(1, 8)), title="Deň v týždni", ticktext=xtext, tickangle=0),
            yaxis=dict(title="Priem. počet cestujúcich"),
        )
        return graf


    def view_month_week(doh):
        if doh in ["Podľa dní", "Podľa hodín"]:
            return monthly_plot(doh)
        return week_plot(df)
    return view_month_week, week_plot


@app.cell
def __():
    import marimo as mo
    return mo,


if __name__ == "__main__":
    app.run()
