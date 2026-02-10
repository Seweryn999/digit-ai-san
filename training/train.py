import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import os


# 1. Ładowanie danych MNIST
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# 2. Normalizacja (0-255 -> 0-1)
x_train = x_train / 255.0
x_test = x_test / 255.0

# 3. Budowa modelu
model = keras.Sequential([
    layers.Reshape((28,28,1), input_shape=(28,28)),
    layers.Conv2D(32, (3,3), activation="relu"),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax")
])


# 4. Kompilacja
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# 5. Trenowanie
history = model.fit(
    x_train,
    y_train,
    epochs=8,
    validation_split=0.1
)

# 6. Test
loss, acc = model.evaluate(x_test, y_test)
print("Accuracy:", acc)

# 7. Wykres accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['train', 'val'])
plt.title("Accuracy")
plt.show()

# 8. Zapis modelu


model.save(save_path)

