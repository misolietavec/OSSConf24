import marimo

__generated_with = "0.6.22"
app = marimo.App(width="full")


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Zaujímame sa o miesta na mape, kde ľudia nastupovali a vystupovali. 
        ### Nakreslíme podľa dní aj hodín.
        #### Na to môžeme použiť už známy modul `plotly`, alebo špeciálny mapový modul `ipyleaflet`. Nech je zatiaľ `plotly`, konkrétne funkcia `px.scatter_mapbox`.
        """
    )
    return


@app.cell
def __():
    import polars as pl
    import plotly.express as px
    return pl, px


@app.cell
def __(pl):
    df = pl.read_parquet("data/nyc_taxi310k.parq")
    print(df.columns)  # ktore stlpce nam treba? print - aby to bolo v riadku, nie ako stlpec
    return df,


@app.cell
def __(df, pl):
    # pre nastup, vystup atlpce zacinajuce pick_ alebo drop_ - priklad vyberu podla regularnych vyrazov pre stlpce
    df_pickdrop = df.select(pl.col("^pick_|drop_.*$"))
    print(df_pickdrop.columns)
    return df_pickdrop,


@app.cell
def __(df_pickdrop, pl):
    # vyberieme data pre nejaky den a hodinu, napr. 14. jan o 8-mej
    df_pickdh = df_pickdrop.filter((pl.col("pick_dt").dt.day() == 14) & 
                                   (pl.col("pick_dt").dt.hour() == 8))
    return df_pickdh,


@app.cell
def __(df_pickdh, px):
    # px.scatter_mapbox je funkcia pre mapy v plotly
    mapa = px.scatter_mapbox(
        df_pickdh,
        lat="pick_lat",
        lon="pick_lon",
        mapbox_style="open-street-map",
        zoom=10,
        color_discrete_sequence=["darkblue"],
        width=500,
        height=500,
        opacity=0.3,
        title=f"Počet jázd: {df_pickdh.shape[0]}",
    )
    mapa.update_traces(marker={"size": 4})
    mapa.update_layout(margin={"t": 25, "b": 0}, hovermode=False)
    return mapa,


@app.cell
def __(mo):
    mo.md(r"#### Funkcia pre nakreslenie mapy v oboch prípadoch. Vstupuje do nej frejma celkova (`df_pickdrop`), deň a hodina sú parametre")
    return


@app.cell
def __(pl, px):
    def map_plot(frm, day, hour, pick=True):  # pick=False znamena, ze drop
        col_prefix = "pick_" if pick else "drop_"
        df_dh = frm.filter((pl.col(f"{col_prefix}dt").dt.day() == day) & (pl.col(f"{col_prefix}dt").dt.hour() == hour))
        mapa = px.scatter_mapbox(
            df_dh,
            lat=f"{col_prefix}lat",
            lon=f"{col_prefix}lon",
            mapbox_style="open-street-map",
            zoom=10,
            color_discrete_sequence=["darkblue"],
            width=500,
            height=500,
            opacity=0.3,
            title=f"Počet jázd: {df_dh.shape[0]}",
        )
        mapa.update_traces(marker={"size": 4})
        mapa.update_layout(margin={"t": 30, "b": 10}, hovermode=False)
        return mapa
    return map_plot,


@app.cell
def __(df_pickdrop, map_plot, mo):
    mo.hstack([map_plot(df_pickdrop, 25, 12), map_plot(df_pickdrop, 25, 12, False)])
    return


@app.cell
def __(mo):
    mo.md(r"### V ďalšom NB dáme dokopy všetko, čo sme doteraz porobili a začne sa rysovať webová aplikácia.")
    return


@app.cell
def __():
    import marimo as mo
    return mo,


if __name__ == "__main__":
    app.run()
