
---

## 📜 app.py
```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from faker import Faker

# Configuración de página
st.set_page_config(page_title="My First Deployment", layout="wide")

# Generador de datos
faker = Faker()

# Sidebar
st.sidebar.header("Configuración de datos")
n_rows = st.sidebar.slider("Número de filas", 10, 500, 100)
show_plot = st.sidebar.checkbox("Mostrar gráfico", True)

# Generar DataFrame
@st.cache_data
def generar_datos(n):
    data = {
        "Nombre": [faker.name() for _ in range(n)],
        "Ciudad": [faker.city() for _ in range(n)],
        "Edad": np.random.randint(18, 70, size=n),
        "Ingreso": np.random.randint(1000, 5000, size=n)
    }
    return pd.DataFrame(data)

df = generar_datos(n_rows)

# Mostrar tabla
st.write("## 📋 Datos Generados")
st.dataframe(df)

# Gráfico
if show_plot:
    st.write("## 📊 Distribución de Edades")
    fig, ax = plt.subplots()
    sns.histplot(df["Edad"], bins=10, kde=True, ax=ax, color="skyblue")
    st.pyplot(fig)

# Filtro por ciudad
ciudad_sel = st.selectbox("Filtrar por ciudad", ["Todas"] + df["Ciudad"].unique().tolist())
if ciudad_sel != "Todas":
    df = df[df["Ciudad"] == ciudad_sel]
    st.write(f"Mostrando {len(df)} registros para la ciudad: **{ciudad_sel}**")
    st.dataframe(df)
