import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import MinMaxScaler
import os
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
CSV_FILE = 'data/SOLUSDT_15m_completo.csv'
MODELO_GUARDADO = 'modelos/transformer_4velas.h5'
SECUENCIA_PASADA = 60  # pasos pasados (15 horas)
VELAS_FUTURAS = 4      # predicciones futuras (1 hora)

# === CARGAR Y PREPARAR DATOS ===
df = pd.read_csv(CSV_FILE)

if 'close' not in df.columns:
    raise ValueError("El CSV debe tener una columna llamada 'close'")

precios = df['close'].values.reshape(-1, 1)

# Normalizar
scaler = MinMaxScaler()
precios_normalizados = scaler.fit_transform(precios)

# Crear secuencias de entrada (X) y salida (y)
X = []
y = []
for i in range(SECUENCIA_PASADA, len(precios_normalizados) - VELAS_FUTURAS):
    X.append(precios_normalizados[i-SECUENCIA_PASADA:i, 0])
    y.append(precios_normalizados[i:i+VELAS_FUTURAS, 0])

X = np.array(X)
y = np.array(y)

# Redimensionar X para Transformer
X = np.expand_dims(X, axis=2)

# === DEFINIR TRANSFORMER ===
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

# Crear modelo
modelo = crear_transformer_modelo(input_shape=(SECUENCIA_PASADA, 1), output_steps=VELAS_FUTURAS)

# === ENTRENAMIENTO INTENSO ===
history = modelo.fit(
    X, y,
    epochs=200,
    batch_size=32,
    validation_split=0.1,
    verbose=1
)

# === GUARDAR MODELO ===
os.makedirs(os.path.dirname(MODELO_GUARDADO), exist_ok=True)
modelo.save(MODELO_GUARDADO)
print("\u2705 Modelo guardado en:", MODELO_GUARDADO)

# === GRAFICAR LOSS ===
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Pérdida Entrenamiento')
plt.plot(history.history['val_loss'], label='Pérdida Validación')
plt.title('Curva de Entrenamiento')
plt.xlabel('Epochs')
plt.ylabel('Pérdida (MSE)')
plt.legend()
plt.grid()
plt.show()
