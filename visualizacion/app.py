# app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")
st.title("📊 Análisis de Ventas - TechNova Retail")

# Subida de archivo
archivo = st.file_uploader("Sube el archivo CSV con datos de ventas", type=["csv"])

if archivo is not None:
    # Leer el CSV con codificación adecuada
    df = pd.read_csv(archivo, encoding="latin-1", sep=";")

    # Limpiar y transformar columna de precios
    df["Precio_unitario(USD)"] = df["Precio_unitario(USD)"].replace('[\$,]', '', regex=True).astype(float)
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True)
    df["Ventas"] = df["Cantidad"] * df["Precio_unitario(USD)"]

    st.subheader("Vista previa del dataset")
    st.dataframe(df.head())

    st.markdown("---")
    st.subheader("1️⃣ Gráfico de Barras: Ventas Totales por Categoría")
    ventas_cat = df.groupby("categoria")["Ventas"].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(10,5))
    sns.barplot(x="categoria", y="Ventas", data=ventas_cat, ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    st.markdown("---")
    st.subheader("2️⃣ Histograma: Distribución de Ventas")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.histplot(df["Ventas"], bins=30, kde=True, ax=ax2)
    st.pyplot(fig2)

    st.markdown("---")
    st.subheader("3️⃣ Gráfico de Línea: Evolución de Ventas en el Tiempo")
    ventas_tiempo = df.groupby("Fecha")["Ventas"].sum().reset_index()
    fig3 = px.line(ventas_tiempo, x="Fecha", y="Ventas", title="Evolución de ventas")
    st.plotly_chart(fig3)

    st.markdown("---")
    st.subheader("4️⃣ Gráfico de Dispersión: Ventas por Categoría")
    fig4, ax4 = plt.subplots(figsize=(10,5))
    sns.stripplot(x="categoria", y="Ventas", data=df, jitter=True, ax=ax4)
    plt.xticks(rotation=45)
    st.pyplot(fig4)

