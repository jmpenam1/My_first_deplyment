# ========================================
# 1. IMPORTAR LIBRERÍAS
# ========================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from faker import Faker
import random

# Configuración estética
sns.set(style="whitegrid")
fake = Faker()

# ========================================
# 2. GENERAR DATOS SINTÉTICOS
# ========================================
def generar_datos_sinteticos(n=200):
    datos = []
    for _ in range(n):
        datos.append({
            "ID": _ + 1,
            "Nombre": fake.name(),
            "Edad": random.randint(18, 70),
            "Ciudad": fake.city(),
            "Fecha_Registro": fake.date_between(start_date='-2y', end_date='today'),
            "Ventas": round(random.uniform(100, 5000), 2),
            "Categoria": random.choice(["A", "B", "C"]),
            "Satisfaccion": random.randint(1, 5)
        })
    return pd.DataFrame(datos)

df = generar_datos_sinteticos()

# ========================================
# 3. INTERFAZ STREAMLIT
# ========================================
st.title("📊 Análisis Exploratorio de Datos (EDA) con Datos Sintéticos")

st.subheader("Vista previa de los datos")
st.dataframe(df.head())

# ========================================
# 4. INFORMACIÓN GENERAL
# ========================================
st.subheader("Información del Dataset")
st.write("**Dimensiones:**", df.shape)
st.write("**Tipos de datos:**")
st.write(df.dtypes)

# ========================================
# 5. ESTADÍSTICAS DESCRIPTIVAS
# ========================================
st.subheader("Estadísticas Descriptivas")
st.write(df.describe(include='all').transpose())

# ========================================
# 6. VALORES NULOS
# ========================================
st.subheader("Valores Nulos")
st.write(df.isnull().sum())

# ========================================
# 7. DISTRIBUCIONES
# ========================================
st.subheader("Distribuciones de Variables Numéricas")
numeric_cols = df.select_dtypes(include=np.number).columns
fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(6, 4 * len(numeric_cols)))
for i, col in enumerate(numeric_cols):
    sns.histplot(df[col], kde=True, ax=axes[i])
    axes[i].set_title(f"Distribución de {col}")
st.pyplot(fig)

# ========================================
# 8. CORRELACIONES
# ========================================
st.subheader("Matriz de Correlación")
corr = df.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# ========================================
# 9. DISTRIBUCIÓN CATEGÓRICA
# ========================================
st.subheader("Distribución por Categoría")
cat_col = st.selectbox("Selecciona una columna categórica", df.select_dtypes(exclude=np.number).columns)
fig, ax = plt.subplots()
sns.countplot(x=df[cat_col], order=df[cat_col].value_counts().index, palette="Set2", ax=ax)
st.pyplot(fig)
