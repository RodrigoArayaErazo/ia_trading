import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import time
import sys

sys.path.append('./scripts')

# Modelo y parámetros
modelo = tf.keras.models.load_model('modelos/transformer_4velas.h5')
ARCHIVO_PRECIOS = 'data/precios_reales.csv'
ARCHIVO_PREDICCIONES = 'data/predicciones.csv'
VENTANA_ENTRADA = 60
VENTANA_SCALER = 200

def esperar_nuevo_dato(ultimo_timestamp):
    print("⏳ Esperando nuevo dato...")
    while True:
        precios = pd.read_csv(ARCHIVO_PRECIOS)
        nuevo_timestamp = precios['timestamp'].values[-1]
        if nuevo_timestamp != ultimo_timestamp:
            return precios
        time.sleep(15)

def hacer_prediccion(precios):
    try:
        precios['precio'] = precios['precio'].astype(float)
        datos = precios['precio'].values.reshape(-1, 1)
        precio_actual = float(datos[-1])

        # Normalizar
        ventana_scaler = datos[-VENTANA_SCALER:]
        scaler = MinMaxScaler()
        scaler.fit(ventana_scaler)
        normalizados = scaler.transform(datos)
        entrada = normalizados[-VENTANA_ENTRADA:].reshape(1, VENTANA_ENTRADA, 1)

        # Predicción
        pred = modelo.predict(entrada)
        pred = scaler.inverse_transform(pred.reshape(-1, 1))

        timestamp = pd.Timestamp.now()
        print(f"\n🧠 [{timestamp}] Predicción de próximas 4 velas (precio aproximado):")
        for i, p in enumerate(pred, 1):
            print(f"Vela {i}: {p[0]:.2f} USD")

        # Guardar en CSV
        nueva_fila = pd.DataFrame([{
            "timestamp": timestamp,
            "precio_actual": precio_actual,
            "vela_1": pred[0][0],
            "vela_2": pred[1][0],
            "vela_3": pred[2][0],
            "vela_4": pred[3][0]
        }])

        try:
            historico = pd.read_csv(ARCHIVO_PREDICCIONES)
            historico = pd.concat([historico, nueva_fila], ignore_index=True)
        except FileNotFoundError:
            historico = nueva_fila

        historico.to_csv(ARCHIVO_PREDICCIONES, index=False)

    except Exception as e:
        print(f"❌ Error en predicción: {e}")

# Bucle principal
if __name__ == "__main__":
    print("🚀 Sistema sincronizado de predicción con guardado iniciado...\n")

    precios = pd.read_csv(ARCHIVO_PRECIOS)
    ultimo_ts = precios['timestamp'].values[-1]

    while True:
        precios = esperar_nuevo_dato(ultimo_ts)
        ultimo_ts = precios['timestamp'].values[-1]
        hacer_prediccion(precios)
