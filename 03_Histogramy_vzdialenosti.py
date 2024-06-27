import marimo

__generated_with = "0.6.22"
app = marimo.App(width="full")


@app.cell
def __():
    # obvykly uvodny tanec
    import polars as pl
    import plotly.express as px
    import numpy as np  # potrebujeme pre histogram
    return np, pl, px


@app.cell
def __(pl):
    # nacitame frejmu, stlpce, co pouzijeme v tomto NB, 
    cols = ['distance', 'rtime']
    df_dt = pl.read_parquet('data/nyc_taxi310k.parq', columns=cols)
    return cols, df_dt


@app.cell
def __(mo):
    mo.md(r"### V tomto NB nás budú zaujímať časy jázd a prejazdené vzdialenosti")
    return


@app.cell
def __(df_dt):
    # predbezny prieskum -rozsahy
    for col in df_dt.columns:
        print(col, df_dt[col].min(), df_dt[col].max())
    return col,


@app.cell
def __(df_dt, np):
    # na zaciatok pre vzd. horna hranica 10, pre casy 30
    # motivacia - kvantil - aka cast z 1 je nalavo od neho
    # df_dt['distance'].quantile(0.97)
    # df_dt['rtime'].quantile(0.97)
    # pochopit, co to vrati
    yt, xt = np.histogram(df_dt['rtime'], bins=20, range=(0, 40))
    print(yt, xt)
    return xt, yt


@app.cell
def __(df_dt, np, pl, px):
    # jedna funkcia pre kreslenie staci - aj s np.histogram vnutri, potom dve funkcie pre vzdial. a casy
    def plot_histo(col, rozsah, nbins=20):
        xlabel = 'Vzdialenosť (míle)' if col == 'distance' else 'Čas jazdy'
        y, x = np.histogram(df_dt[col], range=rozsah, bins=nbins)
        x = (x[0:-1] + x[1:]) / 2  # stredy intervalov, nie konce
        df_hist = pl.DataFrame({'x': x, 'y': y})  # pomocna frejma
        return px.bar(df_hist, x='x', y='y', barmode='group', 
                      labels={'x': xlabel, 'y': 'početnosť', 'variable': 'hodnota'}, width=900, height=350)

    def histo_dists(bins):
        return plot_histo('distance', (0, 8), bins)

    def histo_times(bins):
        return plot_histo('rtime', (0, 35), bins)
    return histo_dists, histo_times, plot_histo


@app.cell
def __(plot_histo):
    plot_histo('rtime', (0, 40), 40) # skusat 'distance', rozne nbins aj hornu hranicu
    return


@app.cell
def __(plot_histo):
    plot_histo('distance', (0, 8), 80)
    # preco sa pri niektorom pocte binov histogram pre vzdialenosti 'rozpada' ?
    # df.filter(pl.col('distance') == pl.col('distance').round(1))
    return


@app.cell
def __(mo):
    mo.md(r"### Čo hovoria tie grafy? Že je to zrozumiteľnejšie, ako čísla vo frejmoch?")
    return


@app.cell
def __():
    import marimo as mo
    return mo,


if __name__ == "__main__":
    app.run()
