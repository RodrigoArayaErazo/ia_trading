# scripts/prediccion_clasificador_4velas.py

import pandas as pd
import numpy as np
import tensorflow as tf
import time
import sys

# Aseguramos que Python encuentre los scripts
sys.path.append('./scripts')

# Archivo de precios
csv_file = "data/precios_reales.csv"

# Cargamos el modelo de clasificación
modelo = tf.keras.models.load_model("modelos/clasificador_4velas_sube_baja.h5")

# Definir el tamaño de ventana que espera la IA
VENTANA = 60  # Como fue entrenado

# Función para hacer la predicción
def hacer_prediccion():
    try:
        precios = pd.read_csv(csv_file)

        # Tomamos solo el precio y las últimas VENTANA filas
        precios_input = precios["precio"].values[-VENTANA:]
        
        if len(precios_input) == VENTANA:
            precios_input = precios_input.reshape(1, VENTANA, 1)  # Reshape para la IA
            prediccion = modelo.predict(precios_input)
            
            if prediccion[0][0] > 0.5:
                print("🔵 Predicción: SUBE 🚀")
            else:
                print("🔴 Predicción: BAJA 🔻")
        else:
            print(f"⚠️ No hay suficientes datos aún. ({len(precios_input)}/{VENTANA})")

    except Exception as e:
        print(f"❌ Error al hacer predicción: {e}")

# Bucle principal
if __name__ == "__main__":
    print("🤖 Sistema de clasificación IA iniciado...\n")
    
    while True:
        hacer_prediccion()
        print("⏳ Esperando 1 minuto para nueva predicción...\n")
        time.sleep(60)
