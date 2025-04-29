import time
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Configuraciones
VENTANA = 60  # 60 precios de entrada

# Cargar modelos
modelo = load_model('modelos/clasificador_4velas_subebaja_mejorado.h5')

# Ruta del archivo CSV
csv_file = 'data/precios_reales.csv'

def hacer_prediccion():
    try:
        precios = pd.read_csv(csv_file)

        if len(precios) < VENTANA + 4:
            print(f"\u26a0\ufe0f No hay suficientes datos ({len(precios)}/{VENTANA+4})")
            return

        # Preparamos datos de entrada
        precios_input = precios['precio'].values[-(VENTANA+4):-4]
        precios_input = precios_input.reshape(1, VENTANA, 1)

        # Realizar predicción
        prediccion = modelo.predict(precios_input)

        direccion = 'SUBE' if prediccion[0][0] >= 0.5 else 'BAJA'
        print(f"\n\ud83d\udcca Predicción: {direccion} ({prediccion[0][0]:.2f})")

    except FileNotFoundError:
        print("\u274c Archivo precios_reales.csv no encontrado.")
    except Exception as e:
        print(f"\u274c Error inesperado: {e}")

if __name__ == '__main__':
    print("\ud83d\udcbb Sistema de predicción IA SUBE/BAJA iniciado...\n")
    while True:
        hacer_prediccion()
        print("\u23f3 Esperando 1 minuto para nueva predicción...\n")
        time.sleep(60)
