from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Conv1D, Dense, Input, LSTM, Embedding, Dropout, Activation, MaxPooling1D
import numpy as np
import pandas as pd
from gensim.models import KeyedVectors
from keras.models import Model, Sequential
import tensorflowjs as tfjs
import pickle
from sklearn.utils import shuffle
from config.depression import epochs, batch_size, verbose, shuffle, val_size

tokenizer = Tokenizer(num_words=20000)



data = []
with open("data/data.txt", encoding="utf-8") as f:
    for line in f.readlines():
        data.append(line)


with open("data/data2.txt", encoding="utf-8") as f:
    for line in f.readlines():
        data.append(line)

tokenizer.fit_on_texts(data)

sequences_d = tokenizer.texts_to_sequences(data)


word_index = tokenizer.word_index
print('Found %s unique words' % len(word_index))

data_d = pad_sequences(sequences_d, maxlen=140)




nb_words = min(20000, len(word_index))

embedding_matrix = np.zeros((nb_words, 300))

print("Fetching word2vec lib")

EMBEDDING_FILE = 'GoogleNews-vectors-negative300.bin.gz'
word2vec = KeyedVectors.load_word2vec_format(EMBEDDING_FILE, binary=True)


print("Creating embed matrix from vocab")
for (word, idx) in word_index.items():
    if(idx%100==0):
        print(idx, 20000)
    if(idx >= 20000):
        break
    if word in word2vec.index_to_key and idx < 20000:
        embedding_matrix[idx] = word2vec.get_vector(word)


model = Sequential()

# Embedded layer
model.add(Embedding(len(embedding_matrix), 300, weights=[embedding_matrix], 
                            input_length=140, trainable=False))
# CNN Layer
model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.2))
# LSTM Layer
model.add(LSTM(300))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='nadam', metrics=['acc'])
print(model.summary())

labels_d = np.array([1] * 59868 + [0] * 59679)

data_d, labels_d = shuffle(data_d, labels_d)

data_val = data_d[:val_size]
train_data = data_d[val_size:]


labels_val = labels_d[:val_size]
labels_train = labels_d[val_size:]

hist = model.fit(train_data, labels_train,
        validation_data=(data_val, labels_val),
        epochs=epochs, batch_size=batch_size, shuffle=shuffle, verbose=verbose)


model.save("state/depression/keras/model.h5")
tfjs.converters.save_keras_model(model, "state/depression/tfjs")

with open('state/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('state/word2vec.pickle', 'wb') as handle:
    pickle.dump(word2vec, handle, protocol=pickle.HIGHEST_PROTOCOL)