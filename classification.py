import numpy as np
import os
import tensorflow as tf
import pickle
import matplotlib.pyplot as plt
from tensorflow import keras

my_path = os.path.abspath(os.path.dirname(__file__))

dataPath = "D:\\thesis\\datafirst90Perc.npy"
LabelsPath = "D:\\thesis\\dataOutfirst90Perc.npy"
trainsc2 = np.load(my_path + "\\numpyArrays\\trainlast3percx.npz")
testsc2 = np.load(my_path + "\\numpyArrays\\testlast3percx.npz")
'''
traindata = trainsc2['data']
traindataOut = trainsc2['dataOut']
testdata = testsc2['data']
testdataOut = testsc2['dataOut']
'''

traindata = []
traindataOut = []
testdata = []
testdataOut = []

with open('D:\\thesis\\train2Z vs T3percx.npy', 'rb') as f:
    traindata = np.array(pickle.load(f))
with open('D:\\thesis\\trainout2Z vs T3percx.npy', 'rb') as f:
    traindataOut = np.array(pickle.load(f))
with open('D:\\thesis\\test2Z vs T3percx.npy', 'rb') as f:
    testdata = np.array(pickle.load(f))
with open('D:\\thesis\\testout2Z vs T3percx.npy', 'rb') as f:
    testdataOut = np.array(pickle.load(f))



model = keras.Sequential([
    keras.layers.Dense(128, input_shape=(914,),activation=tf.nn.relu),
    keras.layers.Dense(128,activation=tf.nn.relu),
    keras.layers.Dense(2,activation=tf.nn.softmax)
])
model.compile(optimizer=tf.train.AdadeltaOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(traindata, traindataOut,validation_data=(testdata,testdataOut) ,epochs=300)


# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()