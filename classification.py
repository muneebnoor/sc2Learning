import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras

my_path = os.path.abspath(os.path.dirname(__file__))

sc2data = np.load(my_path + "/numpyArrays/data05Perc.npz")
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

model = keras.Sequential([
    keras.layers.Dense(124, input_shape=(915,), activation=tf.nn.relu),
    keras.layers.Dense(124, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(data, dataOut,  validation_split=0.25, epochs=5)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()


#print('Test accuracy:', history['val_acc'])