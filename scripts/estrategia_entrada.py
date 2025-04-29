import pandas as pd
import numpy as np
import tensorflow as tf
import time

# Modelo entrenado
modelo = tf.keras.models.load_model('modelos/clasificador_4velas_sube_baja.h5')

# Parámetros
CSV_FILE = 'data/precios_reales.csv'
TAKE_PROFIT = 0.0030
STOP_LOSS = 0.0015
VENTANA = 60

def esperar_nuevo_dato(ultimo_ts):
    print("⏳ Esperando nuevo dato...")
    while True:
        precios = pd.read_csv(CSV_FILE)
        nuevo_ts = precios['timestamp'].values[-1]
        if nuevo_ts != ultimo_ts:
            return precios
        time.sleep(15)

def hacer_estrategia(precios):
    try:
        if len(precios) < VENTANA:
            print(f"⚠️ Datos insuficientes ({len(precios)}/{VENTANA}).")
            return

        precios_input = precios['precio'].values[-VENTANA:].reshape(1, VENTANA, 1)
        prediccion = modelo.predict(precios_input)
        precio_entrada = precios['precio'].values[-1]
        timestamp = pd.Timestamp.now()

        if prediccion[0][0] > 0.5:
            tp = precio_entrada * (1 + TAKE_PROFIT)
            sl = precio_entrada * (1 - STOP_LOSS)
            print(f"\n[{timestamp}] 🟢 LONG activado:")
            print(f"   🎯 Entrada: {precio_entrada:.4f} USD")
            print(f"   📈 TP: {tp:.4f} USD (+0.30%)")
            print(f"   📉 SL: {sl:.4f} USD (-0.15%)")
        else:
            tp = precio_entrada * (1 - TAKE_PROFIT)
            sl = precio_entrada * (1 + STOP_LOSS)
            print(f"\n[{timestamp}] 🔴 SHORT activado:")
            print(f"   🎯 Entrada: {precio_entrada:.4f} USD")
            print(f"   📈 TP: {tp:.4f} USD (+0.30% inverso)")
            print(f"   📉 SL: {sl:.4f} USD (-0.15% inverso)")

    except Exception as e:
        print(f"❌ Error en estrategia: {e}")

if __name__ == "__main__":
    print("📊 Sistema IA sincronizado esperando nuevo dato...\n")
    precios = pd.read_csv(CSV_FILE)
    ultimo_ts = precios['timestamp'].values[-1]

    while True:
        precios = esperar_nuevo_dato(ultimo_ts)
        ultimo_ts = precios['timestamp'].values[-1]
        hacer_estrategia(precios)
# Guardar en senales.csv
nueva_senal = pd.DataFrame([{
    "timestamp": timestamp,
    "precio_entrada": precio_entrada,
    "senal": "LONG" if prediccion[0][0] > 0.5 else "SHORT",
    "take_profit": tp,
    "stop_loss": sl
}])

try:
    historial = pd.read_csv("data/senales.csv")
    historial = pd.concat([historial, nueva_senal], ignore_index=True)
except FileNotFoundError:
    historial = nueva_senal

historial.to_csv("data/senales.csv", index=False)
