# -*- coding: utf-8 -*-
"""Eval

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u_qxf95lZdZIVll-Xc2dUK6jjt-GOTaN
"""

import keras
import sys
import h5py
import tensorflow as tf
import numpy as np

# threshold taken using computation in notebook.

RECONSTRUCTION_LOSS_THRESHOLD = np.array([0.09690079] * 2500)
clean_data_filename = str(sys.argv[1])
model_filename = str(sys.argv[2])
VAE_file_name = str(sys.argv[3])


# /content/drive/MyDrive/data/anonymous_1_poisoned_data.h5
# clean_data_filename = "/content/drive/MyDrive/data/clean_test_data.h5"
# model_filename = '/content/CSAW-HackML-2020/models/sunglasses_bd_net.h5'
# VAE_file_name = "/content/drive/MyDrive/VAE.h5"


def data_loader(filepath):
    data = h5py.File(filepath, 'r')
    x_data = np.array(data['data'])
    y_data = np.array(data['label'])
    x_data = x_data.transpose((0, 2, 3, 1))
    return x_data, y_data


def data_preprocess(x_data):
    print("Preprocessing...")
    return x_data / 255


def detect_anomaly(model, data, x_test, threshold, clean_model):
    reconstructions = model(data)
    result = []
    total = 0
    for reconstruction, image, original_image in zip(reconstructions, data, x_test):
        loss = tf.keras.losses.mae(reconstruction, image)
        loss = np.mean(loss) + np.std(loss)
        valid = 1283 if loss > threshold[0] else clean_model.predict(original_image.reshape((1, 55, 47, 3))).argmax()
        result.append(valid)
    return np.array(result)


def convert_to_size(desiredX, desiredY, data):
    padded_images = []
    for img in data:
        shape = img.shape
        xDiff = desiredX - shape[0]
        xLeft = xDiff // 2
        xRight = xDiff - xLeft
        yDiff = desiredY - shape[1]
        yLeft = yDiff // 2
        yRight = yDiff - yLeft
        padded_images.append(np.pad(img, ((xLeft, xRight), (yLeft, yRight), (0, 0)), mode='constant'))
    padded_images = np.array(padded_images)
    return padded_images


def main():
    x_test, y_test = data_loader(clean_data_filename)
    print("Test Data loaded")
    x_test = data_preprocess(x_test)
    clean_model = keras.models.load_model(model_filename)
    print("Clean Model loaded")

    clean_model.load_weights(model_filename)

    # clean_model.summary()

    # clean_model = keras.models.load_model(model_filename)

    VAEModel = keras.models.load_model(VAE_file_name)
    print("VAE Model loaded")

    VAE_input = convert_to_size(56, 48, x_test)

    input_data = VAEModel.predict(VAE_input[:2500]).astype("float32")

    print("VAE model predictions made...")

    clean_label_p = detect_anomaly(VAEModel, input_data, x_test, RECONSTRUCTION_LOSS_THRESHOLD, clean_model)

    print("Anomalies detected, predictions made")
    # clean_label_p = np.argmax(bd_model.predict(x_test), axis=1)
    class_accuracy = np.mean(np.equal(clean_label_p, y_test[:2500])) * 100

    print('Classification accuracy:', class_accuracy)


main()
