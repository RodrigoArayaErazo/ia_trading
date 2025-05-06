import streamlit as st
import pandas as pd

st.set_page_config(page_title="Predicción SOL/USDT", layout="centered")
st.title("📈 Próximas 4 velas (SOL/USDT)")

try:
    df = pd.read_csv("data/predicciones.csv")

    if df.empty:
        st.warning("⚠️ El archivo predicciones.csv está vacío.")
    else:
        ultima = df.iloc[-1]

        st.markdown(f"📅 **Hora predicción:** `{ultima['datetime']}`")
        st.markdown(f"💰 **Último precio real:** ${ultima['real']:.4f}")

        st.markdown("### 🔮 Predicción próximas 4 velas:")
        for i in range(1, 5):
            st.info(f"Vela {i}: **${ultima[f'pred_{i}']:.4f}**")

except Exception as e:
    st.error(f"❌ Error al leer predicciones.csv: {e}")
