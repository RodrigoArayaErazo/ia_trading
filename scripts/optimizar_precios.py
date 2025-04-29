import pandas as pd
import time

# Ruta del archivo de precios
csv_file = "data/precios_reales.csv"

# Número máximo de filas que queremos mantener
MAX_FILAS = 500

# Intervalo de verificación (por ejemplo, cada 5 minutos = 300 segundos)
INTERVALO_SEGUNDOS = 300

while True:
    try:
        precios = pd.read_csv(csv_file)

        if len(precios) > MAX_FILAS:
            # Si hay más filas que el máximo, cortamos las más antiguas
            precios = precios.iloc[-MAX_FILAS:]
            precios.to_csv(csv_file, index=False)
            print(f"🧹 Archivo optimizado: se mantuvieron las últimas {MAX_FILAS} filas.")

        else:
            print(f"✅ Archivo OK ({len(precios)} filas). No requiere optimización.")

    except FileNotFoundError:
        print("⚠️ Archivo de precios no encontrado. Esperando...")
    except Exception as e:
        print(f"❌ Error al optimizar precios: {e}")

    # Esperar antes de volver a verificar
    time.sleep(INTERVALO_SEGUNDOS)
