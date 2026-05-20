import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#Titulos
st.sidebar.image("logouprh.png", width=200)
st.set_page_config(layout="wide")

st.title("Datos de Crímenes en Puerto Rico 2013-2016")
st.caption("Fuente de datos: Policía de Puerto Rico")
st.divider()

df = pd.read_csv("https://cdat.uprh.edu/~eramos/data/crime_processed.csv")

df.columns =  ["Fecha", "Horario", "CrimeCode", "Delito","Lat","Lon","Area","Ano","Mes","nombreMEs","Dia",\
               "DiaSemana","nombreDiaSemana","DiaAno","Hora","Min"]


# FilTros
st.sidebar.header("Filtros")
col1, col2, col3, col4 = st.columns(4)


col1 = st.sidebar.selectbox("Área Policiaca", ["Todas las Areas"] + sorted(df["Area"].unique()))

col2 = st.sidebar.multiselect("Delito", df["Delito"].unique(), default=df["Delito"].unique())

col3 = st.sidebar.multiselect("Día de la Semana", df["nombreDiaSemana"].unique(),
                              default=df["nombreDiaSemana"].unique())


col4 = st.sidebar.selectbox("AM o PM", ["Ambas","AM","PM"])

# Filtrado
filtrado = df.copy()
if col1 != "Todas las Areas":
    filtrado = filtrado[filtrado["Area"] == col1]

filtrado = filtrado[filtrado["Delito"].isin(col2)]
filtrado = filtrado[filtrado["nombreDiaSemana"].isin(col3)]

if col4 != "Ambas":
    filtrado = filtrado[filtrado["Horario"] == col4]


    
col1, col2, col3 = st.columns(3)

cantidad = len(filtrado)
delito_frecuencia = filtrado["Delito"].value_counts().idxmax() if cantidad > 0 else ""
area_incidentes = filtrado["Area"].value_counts().idxmax() if cantidad > 0 else ""

col1.metric("Cantidad de incidentes", cantidad)
col2.metric("Delito más frecuente", delito_frecuencia)
col3.metric("Área con más incidentes", area_incidentes)

#Gravedad de los delitos
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

# Mapa de puntos
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


conteo = filtrado["Delito"].value_counts().reset_index()
conteo.columns = ["Delito","Cantidad"]

#Grafica de barras
grafica = px.bar(
        conteo,
        x="Cantidad",
        y="Delito",
        color="Delito",
    )
st.plotly_chart(grafica, use_container_width=True)

