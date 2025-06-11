import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Configuración de página
st.set_page_config(
    page_title="📊 Dashboard de Ventas - TechNova Retail",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            color: #1f77b4;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("📈 Análisis de Ventas - TechNova Retail")

# Subida del archivo
archivo = st.file_uploader("📂 Sube el archivo CSV con datos de ventas", type=["csv"])

if archivo is not None:
    # Cargar datos
    df = pd.read_csv(archivo, encoding="latin-1", sep=";")
    df["Precio_unitario(USD)"] = df["Precio_unitario(USD)"].replace('[\$,]', '', regex=True).astype(float)
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True)
    df["Ventas"] = df["Cantidad"] * df["Precio_unitario(USD)"]

    # Mostrar vista previa
    st.subheader("🔍 Vista previa del dataset")
    st.dataframe(df.head(), use_container_width=True)

    st.markdown("---")
    st.subheader("📊 1. Ventas Totales por Categoría")
    ventas_cat = df.groupby("categoria")["Ventas"].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(10,5))
    sns.barplot(x="categoria", y="Ventas", data=ventas_cat, ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    st.markdown("---")
    st.subheader("📉 2. Histograma de Ventas")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.histplot(df["Ventas"], bins=30, kde=True, ax=ax2)
    st.pyplot(fig2)

    st.markdown("---")
    st.subheader("📈 3. Evolución de Ventas por Fecha")
    ventas_tiempo = df.groupby("Fecha")["Ventas"].sum().reset_index()
    fig3 = px.line(ventas_tiempo, x="Fecha", y="Ventas", title="Tendencia de Ventas")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.subheader("📌 4. Dispersión de Ventas por Categoría")
    fig4, ax4 = plt.subplots(figsize=(10,5))
    sns.stripplot(x="categoria", y="Ventas", data=df, jitter=True, ax=ax4)
    plt.xticks(rotation=45)
    st.pyplot(fig4)

else:
    st.info("📥 Por favor, sube un archivo CSV para comenzar el análisis.")
