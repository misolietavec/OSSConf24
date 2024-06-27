import marimo

__generated_with = "0.6.22"
app = marimo.App(width="full")


@app.cell
def __():
    import polars as pl
    import plotly.express as px
    return pl, px


@app.cell
def __(mo):
    mo.md(r"### Pre každý deň by sme chceli znázorniť grafy po hodinách. Urobíme pre nástupy")
    return


@app.cell
def __(pl):
    # nacitame vycistenu frejmu, len stlpce, co pouzijeme v tomto NB
    cols = ["pick_dt", "passengers", "fare"]
    df = pl.read_parquet("data/nyc_taxi310k.parq", columns=cols)
    return cols, df


@app.cell
def __(df, pl):
    # Potrebujeme zoskupit data podla dni a hodin; groupped sama o sebe je nam netreba
    groupped = df.group_by(pl.col("pick_dt").dt.day().alias("pick_day"), pl.col("pick_dt").dt.hour().alias("pick_hour"))
    return groupped,


@app.cell
def __(groupped, pl):
    df_days = groupped.agg(
        [
            pl.col("passengers").sum().alias("pass_count"),
            pl.col("fare").count().alias("fares_count"),
            pl.col("fare").sum().alias("total_fare"),
        ]
    )
    return df_days,


@app.cell
def __(df_days):
    df_days.sort(by=["pick_day", "pick_hour"]).head()
    return


@app.cell
def __(df_days, pl):
    # ako vyberieme jeden den? lahko, napr. 14. jan.
    df_days.filter(pl.col("pick_day") == 14).sort(by="pick_hour").head()
    return


@app.cell
def __(pl):
    # funkcia pre vyrobenie df_days z povodnej df; urobime grupovanie a agregacie na jeden sup
    def daily_frame(frm):  # vyvolame s df ako frm
        df_days = frm.group_by(pl.col("pick_dt").dt.day().alias("pick_day"), pl.col("pick_dt").dt.hour().alias("pick_hour")).agg(
            [
                pl.col("passengers").sum().alias("pass_count"),
                pl.col("fare").count().alias("fares_count"),
                pl.col("fare").sum().alias("total_fare"),
            ]
        )
        return df_days
    return daily_frame,


@app.cell
def __(daily_frame, df, pl, px):
    # mame vsetko, aby sme kreslili
    def daily_plot(day):  # frm tu bude povyssia df_days
        frm_d = daily_frame(df)
        frm_day = frm_d.filter(pl.col("pick_day") == day).sort(by="pick_hour")
        pass_fares_plot = px.bar(
            frm_day,
            x="pick_hour",
            y=["pass_count", "fares_count"],
            barmode="group",
            labels={"pick_hour": "Hodina", "value": "Hodnoty", "variable": "Premenná"},
        )
        pass_fares_plot.update_layout(xaxis=dict(tickmode="array", tickvals=list(range(24))))
        return pass_fares_plot
    return daily_plot,


@app.cell
def __(daily_plot):
    daily_plot(26)
    return


@app.cell
def __():
    import marimo as mo
    return mo,


if __name__ == "__main__":
    app.run()
