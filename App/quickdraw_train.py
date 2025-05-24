# quickdraw_train.py
import numpy as np, tensorflow as tf, pathlib, random
from sklearn.model_selection import train_test_split
from tqdm import tqdm

CLASES = ["sun", "house", "tree", "cat", "fish"]
DATA_PATH = pathlib.Path("data/quickdraw")
IMG_SIZE = 28 * 28
SAMPLES_PER_CLASS = 6000          # para que entrene rápido

def cargar_clase(nombre):
    arr = np.load(DATA_PATH / f"{nombre}.npy")
    idx = np.random.choice(len(arr), SAMPLES_PER_CLASS, replace=False)
    return arr[idx] / 255.0       # normalizar 0-1

X, y = [], []
for i, c in enumerate(CLASES):
    print("Cargando", c)
    datos = cargar_clase(c)
    X.append(datos)
    y.append(np.full(len(datos), i))

X = np.vstack(X)
y = np.hstack(y)

# entrenamiento / prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# one-hot
y_train_cat = tf.keras.utils.to_categorical(y_train, len(CLASES))
y_test_cat  = tf.keras.utils.to_categorical(y_test,  len(CLASES))

# MLP de 2 capas ocultas
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation="relu", input_shape=(IMG_SIZE,)),
    tf.keras.layers.Dense(64,  activation="relu"),
    tf.keras.layers.Dense(len(CLASES), activation="softmax")
])

model.compile(optimizer="adam",
              loss="categorical_crossentropy",
              metrics=["accuracy"])

model.fit(X_train, y_train_cat, epochs=10, batch_size=128,
          validation_split=0.1)

print("Accuracy test:",
      model.evaluate(X_test, y_test_cat, verbose=0)[1])

model.save("modelos/quickdraw_mlp.h5")
print("Modelo guardado en modelos/quickdraw_mlp.h5")
