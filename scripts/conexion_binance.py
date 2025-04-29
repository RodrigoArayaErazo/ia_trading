# scripts/conexion_binance.py

from binance.client import Client

# PON AQUÍ TUS CLAVES REALES
API_KEY = "l5e2K7sv9upj0vibEybKLnbEisWl1feuB92ZQVvD57Jii7zqe4N1jcIXBSaMzpDp"
API_SECRET = "AaZNrypnVMYv7soIYKVfQjFdIaeJDmRMCiHvCPRmngzIOSe9xmcS3u65qMkSyQ88"

# Crear cliente de Binance
def crear_cliente():
    cliente = Client(API_KEY, API_SECRET)
    return cliente

# Función para obtener el último precio de SOL/USDT Futures
def obtener_precio_solusdt_futures():
    cliente = crear_cliente()
    try:
        ticker = cliente.futures_symbol_ticker(symbol="SOLUSDT")
        return float(ticker['price'])
    except Exception as e:
        print(f"❌ Error al conectar a Binance: {e}")
        return None

# Test (opcional)
if __name__ == "__main__":
    precio = obtener_precio_solusdt_futures()
    if precio:
        print(f"✅ Precio actual SOL/USDT Futures: {precio} USD")
    else:
        print("❌ No se pudo obtener el precio actual.")