# scripts/actualizar_precios.py

import pandas as pd
import time
from conexion_binance import obtener_precio_solusdt_futures

# Ruta del archivo CSV
csv_file = "data/precios_reales.csv"

# Intervalo de actualización en segundos (1 minuto)
INTERVALO_SEGUNDOS = 900

def actualizar_precio():
    try:
        precios = pd.read_csv(csv_file)
    except FileNotFoundError:
        precios = pd.DataFrame(columns=["timestamp", "precio"])

    while True:
        precio_actual = obtener_precio_solusdt_futures()
        timestamp = pd.Timestamp.now()

        if precio_actual is not None:
            nuevo_registro = pd.DataFrame({
                "timestamp": [timestamp],
                "precio": [precio_actual]
            })
            precios = pd.concat([precios, nuevo_registro], ignore_index=True)
            precios.to_csv(csv_file, index=False)

            print(f"✅ [{timestamp}] Precio actualizado: {precio_actual:.2f} USD")
        else:
            print(f"❌ [{timestamp}] Error al obtener precio.")

        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    print("🚀 Sistema de actualización de precios iniciado...")
    actualizar_precio()
