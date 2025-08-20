import argparse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import xemapytools.main_functions as xptmf
import xemapytools.data_treatment as xptdt
import xemapytools.data_download as xptdd
from xemapytools.resources import url_list, XEMA_standards

def imprimir_estacions(df: pd.DataFrame):
    if df.empty:
        print("Cap estació dins el radi indicat.")
        return
    print(f"{'dist_km':>8}  {'codi_estacio':<10}  {'nom_estacio':<50}  {'nom_municipi':<40}  {'latitud':>9}  {'longitud':>9}")
    print("-"*140)
    for _, row in df.iterrows():
        print(f"{row['dist_km']:8.3f}  {row['codi_estacio']:<10}  {row['nom_estacio']:<50}  {row['nom_municipi']:<40}  {row['latitud']:9.5f}  {row['longitud']:9.5f}")

def plot_estacions(df: pd.DataFrame, center_lat: float, center_lon: float, radi_km: float):
    lats_cercle, lons_cercle = xptmf.get_geographic_circle(center_lat, center_lon, radi_km)

    # Data estacions + punt centre
    df_plot = df.copy()
    df_plot['tipus'] = 'Estació'
    centre = pd.DataFrame({
        'codi_estacio': ['CENTRE'],
        'nom_estacio': ['Punt Centre'],
        'nom_municipi': ['-'],
        'latitud': [center_lat],
        'longitud': [center_lon],
        'dist_km': [0.0],
        'tipus': ['Centre']
    })
    df_plot = pd.concat([df_plot, centre], ignore_index=True)

    # Punts (scatter sobre Mapbox)
    fig = px.scatter_map(
        df_plot,
        lat="latitud",
        lon="longitud",
        color="tipus",
        hover_name="nom_estacio",
        hover_data={"dist_km": True, "codi_estacio": True, "nom_municipi": True},
        zoom=10,
        height=600,
        title=f"Estacions XEMA dins {radi_km:.1f} km"
    )

    # Cercle com a polígon tancat
    fig.add_trace(go.Scattermap(
        lat=lats_cercle + [lats_cercle[0]],
        lon=lons_cercle + [lons_cercle[0]],
        mode='lines',
        fill='toself',
        fillcolor='rgba(255,0,0,0.1)',
        line=dict(color='rgba(255,0,0,0.3)', width=3),
        name=f'Radi {radi_km} km'
    ))

    # Configuració del mapa
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=center_lat, lon=center_lon),
            zoom=10,
            style='open-street-map',  # No cal token
        ),
        margin=dict(l=0, r=0, t=30, b=0),
    )

    fig.show()

def main():
    parser = argparse.ArgumentParser(description="Filtra estacions XEMA dins un radi i mostra-les")
    parser.add_argument("--lat", type=float, required=True, help="Latitud del punt centre")
    parser.add_argument("--lon", type=float, required=True, help="Longitud del punt centre")
    parser.add_argument("--radi", type=float, required=True, help="Radi en km per filtrar les estacions")
    args = parser.parse_args()

    # 1) Carregar dades (fitxer separat)
    df = xptdt.load_local_csv_as_dataframe("data_store/stations_raw_metadata.csv")

    # 2) Filtrar per radi (fa servir la distància importada a data_xema)
    estacions_filtrades = xptmf.get_stations_by_radius(args.lat, args.lon, args.radi, df)

    # 3) Sortida
    if estacions_filtrades.empty:
        print("Cap estació dins el radi indicat.")
    else:
        imprimir_estacions(estacions_filtrades)
        plot_estacions(estacions_filtrades, args.lat, args.lon, args.radi)

if __name__ == "__main__":
    main()
