# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# -----------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------
st.set_page_config(
    page_title="EDA Interactivo",
    page_icon="📊",
    layout="wide"
)

# -----------------------
# ESTILOS PERSONALIZADOS
# -----------------------
st.markdown("""
    <style>
    .main { background-color: #F5F7FA; }
    h1, h2, h3, h4 { color: #333; }
    .sidebar .sidebar-content { background-color: #EAF2F8; }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# MENÚ LATERAL
# -----------------------
menu = st.sidebar.radio(
    "📌 Menú",
    ["Generar Datos Sintéticos", "Subir un Archivo", "Análisis Gráfico", "Acerca de"]
)

# -----------------------
# FUNCIÓN PARA CREAR DATOS
# -----------------------
def generar_datos(filas=100):
    np.random.seed(42)
    data = pd.DataFrame({
        "Edad": np.random.randint(18, 70, filas),
        "Ingresos": np.random.randint(1000, 5000, filas),
        "Género": np.random.choice(["Masculino", "Femenino"], filas),
        "Compra": np.random.choice(["Sí", "No"], filas)
    })
    return data

# -----------------------
# OPCIÓN 1: Generar datos sintéticos
# -----------------------
if menu == "Generar Datos Sintéticos":
    st.title("📊 Generador de Datos Sintéticos")
    filas = st.slider("Cantidad de filas:", 10, 1000, 100, step=10)
    if st.button("Generar Datos"):
        df = generar_datos(filas)
        st.success(f"Se generaron {filas} filas de datos.")
        st.dataframe(df)

        fig = px.histogram(df, x="Edad", title="Distribución de Edades", color="Género")
        st.plotly_chart(fig, use_container_width=True)

# -----------------------
# OPCIÓN 2: Subir archivo
# -----------------------
elif menu == "Subir un Archivo":
    st.title("📂 Cargar Archivo CSV")
    file = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if file is not None:
        df = pd.read_csv(file)
        st.dataframe(df.head())

        if st.button("Mostrar Descripción"):
            st.write(df.describe())

# -----------------------
# OPCIÓN 3: Análisis gráfico
# -----------------------
elif menu == "Análisis Gráfico":
    st.title("📈 Análisis de Datos")
    df = generar_datos(200)
    col_x = st.selectbox("Selecciona variable X", df.columns)
    col_y = st.selectbox("Selecciona variable Y", df.columns)

    fig, ax = plt.subplots()
    ax.scatter(df[col_x], df[col_y], alpha=0.5)
    ax.set_xlabel(col_x)
    ax.set_ylabel(col_y)
    st.pyplot(fig)

# -----------------------
# OPCIÓN 4: Acerca de
# -----------------------
elif menu == "Acerca de":
    st.title("ℹ️ Acerca de")
    st.markdown("""
    Esta aplicación permite:
    - Generar datos sintéticos.
    - Cargar y analizar datasets.
    - Visualizar datos con gráficos interactivos.

    Creada con ❤️ usando **Streamlit**.
    """)
