import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

###HOLAAAAAAAAAAAAAAA

df = pd.read_csv("https://cdat.uprh.edu/~eramos/data/crime_processed.csv")

df.columns = ["Fecha", "Horario", "CrimeCode", "Delito","Lat","Lon","Area","Ano","Mes","nombreMEs","Dia",\
               "DiaSemana","nombreDiaSemana","DiaAno","Hora","Min"]

def dameIndice(delito):
    if delito =="Asesinato":
        return 10
    if delito == "Violacion":
        return 9.5
    elif delito == "Trata Humana":
        return 9.0
    elif delito == "Incendio Malicioso":
        return 8.5
    elif delito == "Agresion Agravada":
        return 8.0
    elif delito == "Robo":
        return 7.0
    elif delito == "Escalamiento":
        return 6.0
    elif delito == "Vehiculo Hurtado":
        return 5.5
    elif delito == "Apropiacion Ilegal":
        return 5.0
    else:
        return 4.0

df["IndiceGravedad"] = df["Delito"].apply(dameIndice)

st.title("Mapa de Crímenes")
centro_zoom = dict(lat=18.25178, lon=-66.254513)
mapa_puntos = px.scatter_mapbox(df,
                                lat="Lat",
                                lon="Lon",
                                color="IndiceGravedad",
                                opacity=0.5,
                                height=800,
                                zoom=8.9,
                                center=centro_zoom,
                                mapbox_style="open-street-map",
                                color_continuous_scale=px.colors.sequential.Hot_r)
st.plotly_chart(mapa_puntos, use_container_width=True)