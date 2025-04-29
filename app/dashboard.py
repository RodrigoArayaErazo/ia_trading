import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Trading - Dashboard", layout="centered")

st.title("📊 Dashboard de Predicción IA")

# Leer precios actuales
try:
    precios = pd.read_csv("data/precios_reales.csv")
    ultimo_precio = precios.iloc[-1]
    st.subheader("🟢 Último precio real:")
    st.markdown(f"**{ultimo_precio['timestamp']} → ${ultimo_precio['precio']:.4f} USD**")
except Exception as e:
    st.error(f"Error al leer precios reales: {e}")

# Leer predicciones
try:
    predicciones = pd.read_csv("data/predicciones.csv")
    ultima_pred = predicciones.iloc[-1]

    st.subheader("🤖 Predicción de próximas 4 velas:")
    st.markdown(f"""
    - Vela 1: **${ultima_pred['vela_1']:.4f}**
    - Vela 2: **${ultima_pred['vela_2']:.4f}**
    - Vela 3: **${ultima_pred['vela_3']:.4f}**
    - Vela 4: **${ultima_pred['vela_4']:.4f}**
    """)
except Exception as e:
    st.error(f"Error al leer predicciones: {e}")

# Información general
st.markdown("---")
st.markdown("🔄 Los datos se actualizan automáticamente cada vez que la IA recibe un nuevo precio.")

