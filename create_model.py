import cv2
import os
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import normalize
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense
images = "datasets/"
no_tumour = os.listdir(images + "no/")
yes_tumour = os.listdir(images + "yes/")
dataset = []
label = []
for i, image_label in enumerate(no_tumour):
    if (image_label.split(".")[1] == "jpg"):
        image = cv2.imread(images + "no/" + image_label)
        image = Image.fromarray(image, 'RGB')
        image = image.resize((64, 64))
        dataset.append(np.array(image))
        label.append(0)

for i, image_label in enumerate(yes_tumour):
    if (image_label.split(".")[1] == "jpg"):
        image = cv2.imread(images + "yes/" + image_label)
        image = Image.fromarray(image, 'RGB')
        image = image.resize((64, 64))
        dataset.append(np.array(image))
        label.append(1)

dataset = np.array(dataset)
label = np.array(label)
x_train, x_test, y_train, y_test = train_test_split(dataset, label, test_size = 0.2, random_state = 0)
x_train = normalize(x_train, axis = 1)
x_test = normalize(x_test, axis = 1)
model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(32, (3, 3), kernel_initializer = "he_uniform"))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(32, (3, 3), kernel_initializer = "he_uniform"))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation("sigmoid"))

model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])
history = model.fit(x_train, y_train, batch_size = 16, verbose = 1, epochs = 10, validation_data = (x_test, y_test), shuffle=True)
model.save("BrainTumour10Epochs.h5")
score = model.evaluate(x_test, y_test)

import matplotlib.pyplot as plt

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()