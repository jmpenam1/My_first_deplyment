# ========================================
# app.py
# Análisis Exploratorio de Datos Interactivo con Streamlit (Python 3.13 Ready)
# ========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from faker import Faker
import random

# Configuración general
sns.set(style="whitegrid")
fake = Faker()

# ========================================
# Función para generar datos sintéticos
# ========================================
def generar_datos_sinteticos(n=200):
    datos = []
    for i in range(n):
        datos.append({
            "ID": i + 1,
            "Nombre": fake.name(),
            "Edad": random.randint(18, 70),
            "Ciudad": fake.city(),
            "Fecha_Registro": fake.date_between(start_date='-2y', end_date='today'),
            "Ventas": round(random.uniform(100, 5000), 2),
            "Categoria": random.choice(["A", "B", "C"]),
            "Satisfaccion": random.randint(1, 5)
        })
    return pd.DataFrame(datos)

# ========================================
# Configuración de la página
# ========================================
st.set_page_config(page_title="EDA Interactivo - Datos Sintéticos", layout="wide")

st.title("📊 Análisis Exploratorio de Datos (EDA) Interactivo")
st.markdown("Genera datos ficticios y explóralos con filtros y visualizaciones dinámicas.")

# ========================================
# Sidebar - Controles
# ========================================
st.sidebar.header("Configuración de Datos")
num_registros = st.sidebar.slider("Número de registros", 50, 1000, 200, step=50)

if st.sidebar.button("🔄 Regenerar Datos"):
    st.cache_data.clear()

@st.cache_data
def cargar_datos(num):
    return generar_datos_sinteticos(num)

df = cargar_datos(num_registros)

# Filtros adicionales
st.sidebar.subheader("Filtros")
categorias = st.sidebar.multiselect("Filtrar por Categoría", df["Categoria"].unique(), default=df["Categoria"].unique())
edad_min, edad_max = st.sidebar.slider("Rango de Edad", int(df["Edad"].min()), int(df["Edad"].max()), 
                                       (int(df["Edad"].min()), int(df["Edad"].max())))

df_filtrado = df[(df["Categoria"].isin(categorias)) & (df["Edad"].between(edad_min, edad_max))]

# ========================================
# Vista previa
# ========================================
st.subheader("📋 Vista Previa de Datos Filtrados")
st.dataframe(df_filtrado.head())

# ========================================
# Información general
# ========================================
with st.expander("ℹ️ Información del Dataset"):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Dimensiones:**", df_filtrado.shape)
    with col2:
        st.write("**Tipos de datos:**")
        st.write(df_filtrado.dtypes)

# ========================================
# Estadísticas descriptivas
# ========================================
with st.expander("📈 Estadísticas Descriptivas"):
    st.write(df_filtrado.describe(include="all").transpose())

# ========================================
# Distribuciones numéricas dinámicas
# ========================================
st.subheader("📊 Distribuciones")
columna_num = st.selectbox("Selecciona una columna numérica", df_filtrado.select_dtypes(include=np.number).columns)

fig, ax = plt.subplots()
sns.histplot(df_filtrado[columna_num], kde=True, ax=ax)
ax.set_title(f"Distribución de {columna_num}")
st.pyplot(fig)

# ========================================
# Matriz de correlación
# ========================================
with st.expander("🔗 Matriz de Correlación"):
    corr = df_filtrado.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# ========================================
# Distribución categórica
# ========================================
st.subheader("📦 Distribución Categórica")
cat_cols = df_filtrado.select_dtypes(exclude=np.number).columns
if len(cat_cols) > 0:
    col_selected = st.selectbox("Selecciona una columna categórica", cat_cols)
    fig, ax = plt.subplots()
    sns.countplot(x=df_filtrado[col_selected], order=df_filtrado[col_selected].value_counts().index, palette="Set2", ax=ax)
    ax.set_title(f"Distribución de {col_selected}")
    st.pyplot(fig)
else:
    st.write("No hay columnas categóricas en el dataset.")
