#%%
import pandas as pd
import streamlit as st
from streamlit_plotly_events import plotly_events
import plotly.express as px
from pathlib import Path


#%%
df0 = pd.read_csv(Path(__file__).parent.parent / "01_Data/Inventario_recursos_turisticos.csv", encoding='latin', sep=';')
dflima = df0.loc[df0["REGIÓN"]=='Lima'].dropna(subset=["LATITUD","LONGITUD"]).rename({'LATITUD':'LONGITUD','LONGITUD':'LATITUD'}, axis=1)
dflima["CATEGORÍA"] = dflima["CATEGORÍA"].astype('category')
dflima.index = range(dflima.shape[0])

# %%

st.title("Inventario de recursos turísticos de Lima región")
st.text("Autor: Ronal Wilfredo Arela Bobadilla")

st.text("Nota: Información elaborada con datos del Ministerio de Comercio Exterior y Turismo")

st.text("Use las herramientas de selección para elegir un grupo de recursos y su información se mostrará en la tabla debajo.")

st.subheader("Figura 1. Mapa de recursos turísticos de Lima región")

band_colors_list =  ['green', 'red', 'blue', 'orange', 'purple', 'gray', 'yellow']
figm2 = px.scatter_mapbox(dflima, lon="LONGITUD", lat="LATITUD", color="CATEGORÍA",
                          zoom=11, color_discrete_sequence=band_colors_list,
                          hover_data=['NOMBRE DEL RECURSO','CATEGORÍA'])
figm2.update_layout(mapbox_style="carto-positron",
                    margin=dict(l=20, r=20, t=20, b=20),
                    mapbox=dict(
                    bearing=0,
                    center=dict(
                        lat=-12.116747,
                        lon=-77.043542
                    ),
                    pitch=0,
                    zoom=8
                    ),
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

selected_points = plotly_events(figm2, click_event=False, select_event=True)

points = []
for point in selected_points:
  points.append(dflima.loc[(dflima['CATEGORÍA'].cat.codes==point['curveNumber'])].iloc[[point['pointIndex']]])
# dfpoints = dflima.loc[dflima['CATEGORÍA'].cat.codes==points].iloc[points]
# print(points)
# print(selected_points)
if len(points)>0:
    dfpoints = pd.concat(points)
else:
   dfpoints = pd.DataFrame()

st.subheader("Tabla 01. Tabla de información")
st.table(dfpoints)