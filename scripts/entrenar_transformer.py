import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import MinMaxScaler
import os

# === CONFIGURACIÓN ===
CSV_FILE = 'data/precios_reales.csv'
MODELO_GUARDADO = 'modelos/transformer_4velas.h5'
SECUENCIA_PASADA = 60  # cuántos datos pasados para predecir
VELAS_FUTURAS = 4  # cuántas velas queremos predecir

# === FUNCIONES ===
def crear_transformer_modelo(input_shape, output_steps):
    inputs = layers.Input(shape=input_shape)

    x = layers.Dense(128, activation='relu')(inputs)
    x = layers.LayerNormalization(epsilon=1e-6)(x)

    attention = layers.MultiHeadAttention(num_heads=4, key_dim=64)(x, x)
    x = layers.Add()([x, attention])
    x = layers.LayerNormalization(epsilon=1e-6)(x)

    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dense(64, activation='relu')(x)
    outputs = layers.Dense(output_steps)(x)

    modelo = models.Model(inputs, outputs)
    modelo.compile(optimizer='adam', loss='mse')
    return modelo

# === CARGAR DATOS ===
df = pd.read_csv(CSV_FILE)

if 'precio' not in df.columns:
    raise ValueError("El CSV debe tener una columna llamada 'precio'")

precios = df['precio'].values.reshape(-1, 1)

# === NORMALIZAR ===
scaler = MinMaxScaler()
precios_normalizados = scaler.fit_transform(precios)

# === CREAR SECUENCIAS ===
X = []
y = []
for i in range(SECUENCIA_PASADA, len(precios_normalizados) - VELAS_FUTURAS):
    X.append(precios_normalizados[i-SECUENCIA_PASADA:i, 0])
    y.append(precios_normalizados[i:i+VELAS_FUTURAS, 0])

X = np.array(X)
y = np.array(y)

# === REDIMENSIONAR PARA TRANSFORMER ===
X = np.expand_dims(X, axis=2)

# === CREAR MODELO ===
modelo = crear_transformer_modelo(input_shape=(SECUENCIA_PASADA, 1), output_steps=VELAS_FUTURAS)

# === ENTRENAR ===
modelo.fit(X, y, epochs=50, batch_size=32, validation_split=0.1)

# === GUARDAR ===
os.makedirs(os.path.dirname(MODELO_GUARDADO), exist_ok=True)
modelo.save(MODELO_GUARDADO)

print("\u2705 Entrenamiento finalizado y modelo guardado en:", MODELO_GUARDADO)
