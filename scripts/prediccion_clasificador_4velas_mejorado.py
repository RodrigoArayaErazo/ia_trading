import pandas as pd
import numpy as np
import tensorflow as tf
import time
import sys

sys.path.append('./scripts')

# Archivo de precios
data_file = "data/precios_reales.csv"

# Cargar el modelo clasificador
modelo = tf.keras.models.load_model("modelos/clasificador_4velas_sube_baja.h5")

# Tamaño de ventana de entrada
VENTANA = 60  # igual que entrenamiento (ajústalo si es necesario)

# Intervalo corregido (15 minutos)
INTERVALO_SEGUNDOS = 900

def hacer_prediccion():
    try:
        precios = pd.read_csv(data_file)

        if len(precios) < VENTANA:
            print(f"⚠️ No hay suficientes datos. ({len(precios)}/{VENTANA})")
            return

        # Últimas 60 velas (sin tratar de obtener datos futuros)
        precios_input = precios['precio'].values[-VENTANA:]
        precios_input = precios_input.reshape(1, VENTANA, 1)

        # Predicción IA
        prediccion = modelo.predict(precios_input)
        precio_actual = precios['precio'].values[-1]
        timestamp = pd.Timestamp.now()

        if prediccion[0][0] > 0.5:
            print(f"[{timestamp}] 🚀 Predicción IA: SUBE")
            print(f"Precio actual: {precio_actual:.4f} USD\n")
        else:
            print(f"[{timestamp}] 🔻 Predicción IA: BAJA")
            print(f"Precio actual: {precio_actual:.4f} USD\n")

    except Exception as e:
        print(f"❌ Error en predicción: {e}")

def main():
    print("\n🤖 Sistema IA SUBE/BAJA en intervalos de 15 minutos iniciado...\n")

    while True:
        hacer_prediccion()
        print(f"⏳ Próxima predicción en {INTERVALO_SEGUNDOS // 60} minutos...\n")
        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()
