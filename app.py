# ========================================
# app.py
# Análisis Exploratorio de Datos con Datos Sintéticos en Streamlit
# ========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from faker import Faker
import random

# Configuración de estilo de gráficos
sns.set(style="whitegrid")
fake = Faker()

# ========================================
# 1. Función para generar datos sintéticos
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
# 2. Configuración de la app Streamlit
# ========================================
st.set_page_config(page_title="EDA con Datos Sintéticos", layout="wide")

st.title("📊 Análisis Exploratorio de Datos (EDA) con Datos Sintéticos")
st.markdown("Este dashboard genera datos ficticios y realiza un análisis exploratorio de datos interactivo.")

# Generar datos
num_registros = st.sidebar.slider("Número de registros", 50, 1000, 200, step=50)
df = generar_datos_sinteticos(num_registros)

# ========================================
# 3. Vista previa de datos
# ========================================
st.subheader("Vista previa de los datos")
st.dataframe(df.head())

# ========================================
# 4. Información general
# ========================================
st.subheader("Información del Dataset")
col1, col2 = st.columns(2)
with col1:
    st.write("**Dimensiones:**", df.shape)
with col2:
    st.write("**Tipos de datos:**")
    st.write(df.dtypes)

# ========================================
# 5. Estadísticas descriptivas
# ========================================
st.subheader("Estadísticas Descriptivas")
st.write(df.describe(include="all").transpose())

# ========================================
# 6. Valores nulos
# ========================================
st.subheader("Valores Nulos por Columna")
st.write(df.isnull().sum())

# ========================================
# 7. Distribuciones numéricas
# ========================================
st.subheader("Distribuciones de Variables Numéricas")
numeric_cols = df.select_dtypes(include=np.number).columns
fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(6, 4 * len(numeric_cols)))
if len(numeric_cols) == 1:
    axes = [axes]
for i, col in enumerate(numeric_cols):
    sns.histplot(df[col], kde=True, ax=axes[i])
    axes[i].set_title(f"Distribución de {col}")
st.pyplot(fig)

# ========================================
# 8. Matriz de correlación
# ========================================
st.subheader("Matriz de Correlación")
corr = df.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# ========================================
# 9. Distribución categórica
# ========================================
st.subheader("Distribución por Categoría")
cat_cols = df.select_dtypes(exclude=np.number).columns
if len(cat_cols) > 0:
    col_selected = st.selectbox("Selecciona una columna categórica", cat_cols)
    fig, ax = plt.subplots()
    sns.countplot(x=df[col_selected], order=df[col_selected].value_counts().index, palette="Set2", ax=ax)
    ax.set_title(f"Distribución de {col_selected}")
    st.pyplot(fig)
else:
    st.write("No hay columnas categóricas en el dataset.")
