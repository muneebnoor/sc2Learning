import numpy as np
import os
import tensorflow as tf
from tensorflow import keras

my_path = os.path.abspath(os.path.dirname(__file__))

sc2data = np.load(my_path + "/numpyArrays/modData.npz")
#sc2data = np.load(my_path + "\\numpyArrays\\modData.npz")

data = sc2data['data']
dataOut = sc2data['dataOut']



'''
newData = list()
for a,b in zip(data,dataOut):
    a[-1] = b[1]
    a[-2] = b[0]
    newData.append(a)

data = np.array(newData)
#data = np.hstack([data,dataOut])
'''

split = int(0.5 * len(data))
train_data = data[:split]
train_out = dataOut[:split]
test_data = data[split:]
test_out = dataOut[split:]

for (trd,tro) in zip(train_data,train_out):
  print(trd.argmax())

model = keras.Sequential([
    keras.layers.Dense(128, input_shape=(915,), activation=tf.nn.relu),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_data, train_out, epochs=5)

test_loss, test_acc = model.evaluate(test_data, test_out)

print('Test accuracy:', test_acc)