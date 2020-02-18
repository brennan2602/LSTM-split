#code taken and adapted from
# https://github.com/keras-team/keras/edit/master/examples/lstm_text_generation.py
# and
# https://www.tensorflow.org/tutorials/text/text_generation
from __future__ import print_function
import os
import tensorflow as tf
import numpy as np
import io
import matplotlib.pyplot as plt

path = "dataVel.txt" #reference to training data
with io.open(path, encoding='utf-8') as f:
    text = f.read().lower()
print('corpus length:', len(text))

#setting up vocabulary
chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

#convert to vectors
print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
def build_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(128, input_shape=(maxlen, len(chars))))
    model.add(tf.keras.layers.Dense(len(chars), activation='softmax'))
    return model

model=build_model()
model.compile(loss='categorical_crossentropy', optimizer="adam")
checkpoint_dir = './Vel_training_checkpoints'
# Name of the checkpoint files
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

#callback function to save checkpoint when training
checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefix,
    save_weights_only=True)
#training code
history = model.fit(x, y,
          batch_size=128,
          epochs=25, callbacks=[checkpoint_callback])


# tf.train.latest_checkpoint(checkpoint_dir)
# model = build_model()
# model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))
# model.build(tf.TensorShape([1, None]))
# model.summary()

#plotting the learning curve
plt.plot(history.history["loss"])
plt.title("model loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.show()
