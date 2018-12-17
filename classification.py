import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras

my_path = os.path.abspath(os.path.dirname(__file__))

dataPath = "D:\\thesis\\datafirst90Perc.npy"
LabelsPath = "D:\\thesis\\dataOutfirst90Perc.npy"
trainsc2 = np.load(my_path + "\\numpyArrays\\trainlast3perc.npz")
testsc2 = np.load(my_path + "\\numpyArrays\\testlast3perc.npz")

traindata = trainsc2['data']
traindataOut = trainsc2['dataOut']

testdata = testsc2['data']
testdataOut = testsc2['dataOut']



model = keras.Sequential([
    #keras.layers.Dropout(0.5),
    keras.layers.Dense(124,  input_shape=(915,),kernel_regularizer= keras.regularizers.l2(0.5) ,activation=tf.nn.relu),
    #keras.layers.Dropout(0.5),
    keras.layers.Dense(124,kernel_regularizer= keras.regularizers.l2(0.5) , activation=tf.nn.relu),
    #keras.layers.Dropout(0.5),
    keras.layers.Dense(2, kernel_regularizer= keras.regularizers.l2(0.5), activation=tf.nn.softmax)
])
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(traindata, traindataOut,validation_data=(testdata,testdataOut) ,epochs=5)


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