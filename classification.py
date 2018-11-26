import numpy as np
import os
import tensorflow as tf
from tensorflow import keras

my_path = os.path.abspath(os.path.dirname(__file__))

sc2data = np.load(my_path + "/numpyArrays/modData.npz")
#sc2data = np.load(my_path + "\\numpyArrays\\modData.npz")

data = sc2data['data']
dataOut = sc2data['dataOut']



def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

'''
newData = list()
for a,b in zip(data,dataOut):
    a[-1] = b[1]
    a[-2] = b[0]
    newData.append(a)

data = np.array(newData)
#data = np.hstack([data,dataOut])
'''
data, dataOut = unison_shuffled_copies(data,dataOut)
split = int(0.8 * len(data))
train_data = data[:split]
train_out = dataOut[:split]
test_data = data[split:]
test_out = dataOut[split:]

model = keras.Sequential([
    keras.layers.Dense(124, input_shape=(915,), activation=tf.nn.relu),
    keras.layers.Dense(124, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_data, train_out, epochs=5)

test_loss, test_acc = model.evaluate(test_data, test_out)

print('Test accuracy:', test_acc)