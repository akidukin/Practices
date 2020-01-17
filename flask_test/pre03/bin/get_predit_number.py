#!usr/env/bin py
#-*- encoding : utf-8 -*-

import tensorflow as tf
from PIL import Image
import numpy as np
import sys

class get_number:

    def __init__(self, pict_path):
        self.pict_path = pict_path
        self.model_path = 'bin/model/number_pictures.h5'
        self.tf_model = tf.keras.models.load_model(self.model_path)

    def _reshape_rescale_picture(self):
        pict = np.array(Image.open(self.pict_path).convert('L').resize((28,28)))
        return (255 - pict.ravel())/255

    def call_value(self):
        input_values = self._reshape_rescale_picture().reshape((1, 28**2))
        pred_values = self.tf_model(input_values).numpy()
        defined_value = pred_values.argmax(axis = 1).item()
        each_predict_values = [(i,x*100) for i,x in enumerate(pred_values[0])]
        return defined_value, each_predict_values

if __name__=='__main__':
    gn = get_number('seven_hard.png')
    print(gn.call_value())