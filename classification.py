import numpy as np
import os
import tensorflow as tf
from tensorflow import keras

my_path = os.path.abspath(os.path.dirname(__file__))

sc2data = np.load(my_path + "\\numpyArrays\\subsets\\subsetOut.npz")

test_data = sc2data['test']
test_out = sc2data['test_out']

train_data = sc2data['train']
train_out = sc2data['trainout']

model = keras.Sequential([
    keras.layers.Dense(128, input_shape=(458,), activation=tf.nn.relu),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_data, train_out, epochs=5)

test_loss, test_acc = model.evaluate(test_data, test_out)

print('Test accuracy:', test_acc)