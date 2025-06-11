
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="📊 Dashboard de Ventas - TechNova Retail",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        body {
            background-color: #111;
            color: #EEE;
        }
        .main {
            background-color: #111;
            color: #EEE;
        }
        h1, h2, h3 {
            color: #1f77b4;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Análisis de Ventas - TechNova Retail")

archivo = st.file_uploader("📂 Sube el archivo CSV con datos de ventas", type=["csv"])
if archivo is None:
    archivo = "Ventas_Minoristas.csv"

try:
    df = pd.read_csv(archivo, encoding="latin-1", sep=";")
    df["Precio_unitario(USD)"] = df["Precio_unitario(USD)"].replace('[\$,]', '', regex=True).astype(float)
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True)
    df["Ventas"] = df["Cantidad"] * df["Precio_unitario(USD)"]

    st.subheader("🔍 Vista previa del dataset")
    st.dataframe(df.head(), use_container_width=True)

    st.markdown("---")
    st.subheader("📊 1. Ventas Totales por Categoría de Producto")
    ventas_cat = df.groupby("categoria")["Ventas"].sum().reset_index().sort_values(by="Ventas", ascending=False)
    fig1, ax1 = plt.subplots(figsize=(10,5))
    sns.barplot(x="categoria", y="Ventas", data=ventas_cat, ax=ax1, palette="deep")
    plt.xticks(rotation=45)
    st.pyplot(fig1)
    top_cat = ventas_cat.iloc[0]
    st.markdown(
        f"""**Análisis:**  
La categoría con mayores ventas es **{top_cat['categoria']}**, con aproximadamente **${top_cat['Ventas']:,.2f} USD**.  
Esto indica fuerte demanda en esa línea.  
**Herramienta:** `Seaborn` permite visualizar comparaciones entre grupos categóricos de forma clara."""
    )

    st.markdown("---")
    st.subheader("📉 2. Histograma: Distribución de Ventas")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.histplot(df["Ventas"], bins=30, kde=True, ax=ax2, color="skyblue")
    st.pyplot(fig2)
    st.markdown(
        f"""**Análisis:**  
Las ventas individuales tienen una media de **${df['Ventas'].mean():,.2f}** y una mediana de **${df['Ventas'].median():,.2f}**, lo que refleja una concentración en ventas medias-bajas.  
**Herramienta:** `Seaborn` permite mostrar histogramas con densidad superpuesta."""
    )

    st.markdown("---")
    st.subheader("📈 3. Evolución de Ventas por Fecha")
    ventas_tiempo = df.groupby("Fecha")["Ventas"].sum().reset_index()
    fig3 = px.line(ventas_tiempo, x="Fecha", y="Ventas", title="Tendencia de Ventas", template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)
    peak = ventas_tiempo[ventas_tiempo["Ventas"] == ventas_tiempo["Ventas"].max()]
    fecha_max = peak["Fecha"].dt.strftime("%d/%m/%Y").values[0]
    monto_max = peak["Ventas"].values[0]
    st.markdown(
        f"""**Análisis:**  
El día de mayor venta fue **{fecha_max}**, con un total de **${monto_max:,.2f}**.  
Esto es útil para identificar picos estacionales.  
**Herramienta:** `Plotly` es ideal para visualizar datos temporales de forma interactiva."""
    )

    st.markdown("---")
    st.subheader("📌 4. Dispersión de Ventas por Categoría")
    fig4, ax4 = plt.subplots(figsize=(10,5))
    sns.stripplot(x="categoria", y="Ventas", data=df, jitter=True, ax=ax4, palette="deep")
    plt.xticks(rotation=45)
    st.pyplot(fig4)
    st.markdown(
        """**Análisis:**  
Algunas categorías como *Electrónica* muestran mayor dispersión en montos de ventas, lo que indica variedad de productos con diferentes precios.  
**Herramienta:** `Seaborn stripplot` permite observar variabilidad interna en cada grupo."""
    )

except Exception as e:
    st.warning("⚠️ No se pudo cargar el archivo. Asegúrate de que esté en el formato correcto.")
    st.error(f"Error: {e}")
