import tensorflow as tf
from tensorflow import keras
import numpy as np
import keras.datasets.imdb as data
import tensorflowjs as tfjs

(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=88000)


word_index = data.get_word_index()
word_index = {k:(v+3) for k, v in word_index.items()}


train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=0, padding="post", maxlen=250)
test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=0, padding="post", maxlen=250)


model = keras.Sequential()
model.add(keras.layers.Embedding(88000, 8))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(8, activation="relu"))
model.add(keras.layers.Dense(1, activation="sigmoid"))


model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

x_val = train_data[:10000]
x_train = train_data[10000:]

y_val = train_labels[:10000]
y_train = train_labels[10000:]

model.fit(x_train,y_train, epochs=40, batch_size=256, validation_data=(x_val,y_val), verbose=1)


model.save("state/sentiment/keras/model.h5")
tfjs.converters.save_keras_model(model, "state/sentiment/tfjs")