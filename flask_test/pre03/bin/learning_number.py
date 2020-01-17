#!usr/env/bin py
#-*- encoding : utf-8 -*-

'''
Explain:
- This predict by Deep Neural Network graph prediction.
- Each layer construct is below...
    - Hidden > 2**5 Dense layer with Batch Normalization
    - Hidden > 2**4 Dense layer
    - Activation > 10
- Epochs is 500 learning turn.
- optimizer is Adam optimize.
- Loss function is CategoricalCrossentropy
- Splited the train.csv to 6:4 for confirmation the accuracy.
- Not used the convolutional.
- Divide by 255 for each pix.
'''

import pandas as pd
import tensorflow as tf
import numpy as np
import sys

train = pd.read_table('bin/data/train.csv',sep=',',header=0)
test = pd.read_table('bin/data/test.csv',sep=',',header=0)
submit_format = pd.read_table('bin/data/sample_submission.csv', sep = ',', header = 0)
seed = 201912

## ダミー行列の作成
train_y = pd.get_dummies(train.label).to_numpy()
y_length = len(set(train.label))
train_x = train.iloc[:,1:].to_numpy()
test_x = test.to_numpy()

## feature 加工
train_x = train_x/255
test_x = test_x/255

## epochとかとか
epoch = 500
index_list = np.arange(0,train_x.shape[0])

## tensorflowモデルの作成
tf_model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(2**5, activation = tf.nn.relu)
        , tf.keras.layers.BatchNormalization()
        , tf.keras.layers.Dense(2**4, activation = tf.nn.relu)
        , tf.keras.layers.Dense(y_length, activation = tf.nn.softmax)
    ]
)
tf_model.compile(optimizer = tf.keras.optimizers.Adam()
                , loss = tf.keras.losses.CategoricalCrossentropy()
                , metrics=['accuracy'])

TrainIndex = np.array([True if np.random.rand() <= 0.4 else False for x in index_list])
TrainX = train_x[TrainIndex,:]
TrainY = train_y[TrainIndex,:]
TestIndex = np.logical_not(TrainIndex)
TestX = train_x[TestIndex,:]
TestY = train_y[TestIndex,:]

test_metrix = tf.keras.metrics.Accuracy()
train_metrix = tf.keras.metrics.Accuracy()

metrix_accuracy_train = []
metrix_accuracy_test = []

for i in range(epoch):
    tf_model.fit(TrainX, TrainY, batch_size = 512, epochs=1, verbose = 0)

    predict_val = tf_model(TrainX).numpy()
    train_metrix.update_state(predict_val.argmax(axis = 1), TrainY.argmax(axis = 1))
    metrix_accuracy_train.append(train_metrix.result().numpy())

    predict_val = tf_model(TestX).numpy()
    test_metrix.update_state(predict_val.argmax(axis = 1), TestY.argmax(axis = 1))
    metrix_accuracy_test.append(test_metrix.result().numpy())

    sys.stdout.write('\r {}/{} Accuracy <Train : {}> <Test : {}>'.format(i,epoch,metrix_accuracy_train[-1], metrix_accuracy_test[-1]))

    if i % 100 == 0:
        print('')
        predict_val = tf_model(TestX).numpy()
        test_metrix.update_state(predict_val.argmax(axis = 1), TestY.argmax(axis = 1))
        print('<Accuracy>\n\t Train : {} | \t Test : {}'.format(metrix_accuracy_train[-1], metrix_accuracy_test[-1]))
        print(tf.math.confusion_matrix(predict_val.argmax(axis = 1), TestY.argmax(axis = 1)).numpy())
        tf_model.save('bin/model/number_pictures.h5')
        submit_predicts = tf_model(test_x).numpy()
        submit_predicts = submit_predicts.argmax(axis = 1)
        submit_format['Label'] = submit_predicts
        submit_format.to_csv('bin/data/sample_submission.csv', index = False)