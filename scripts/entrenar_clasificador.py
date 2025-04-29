import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os

# === CONFIGURACION ===
CSV_FILE = 'data/SOLUSDT_15m_completo.csv'
MODELO_GUARDADO = 'modelos/clasificador_4velas_sube_baja.h5'
SECUENCIA_PASADA = 60   # Cuantas velas pasadas usamos
VELAS_FUTURAS = 4       # Cuantas velas futuras evaluamos

# === CARGAR Y PREPARAR DATOS ===
df = pd.read_csv(CSV_FILE)

if 'close' not in df.columns:
    raise ValueError("El CSV debe tener una columna llamada 'close'")

precios = df['close'].values.reshape(-1, 1)

# Normalizar precios
scaler = MinMaxScaler()
precios_normalizados = scaler.fit_transform(precios)

# Crear X (entradas) e y (salidas)
X = []
y = []
for i in range(SECUENCIA_PASADA, len(precios_normalizados) - VELAS_FUTURAS):
    pasada = precios_normalizados[i-SECUENCIA_PASADA:i, 0]
    futura = precios_normalizados[i:i+VELAS_FUTURAS, 0]

    precio_actual = pasada[-1]
    precio_futuro_promedio = np.mean(futura)

    # Si el promedio de las 4 velas futuras es mayor al precio actual => SUBE
    if precio_futuro_promedio > precio_actual:
        etiqueta = 1  # SUBE
    else:
        etiqueta = 0  # BAJA

    X.append(pasada)
    y.append(etiqueta)

X = np.array(X)
y = np.array(y)

# Redimensionar X para que tenga (batch_size, timesteps, features)
X = np.expand_dims(X, axis=2)

# Dividir en entrenamiento y validacion
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42, shuffle=True)

# === DEFINIR MODELO CLASIFICADOR ===
def crear_clasificador(input_shape):
    inputs = layers.Input(shape=input_shape)
    x = layers.LSTM(64, return_sequences=False)(inputs)
    x = layers.Dense(32, activation='relu')(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)

    modelo = models.Model(inputs, outputs)
    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return modelo

# Crear modelo
modelo = crear_clasificador(input_shape=(SECUENCIA_PASADA, 1))

# === ENTRENAMIENTO ===
history = modelo.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_val, y_val)
)

# === GUARDAR MODELO ===
os.makedirs(os.path.dirname(MODELO_GUARDADO), exist_ok=True)
modelo.save(MODELO_GUARDADO)

print("\u2705 Clasificador entrenado y guardado en:", MODELO_GUARDADO)
