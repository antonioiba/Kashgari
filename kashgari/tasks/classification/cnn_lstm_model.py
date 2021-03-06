# encoding: utf-8
"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz

@version: 1.0
@license: Apache Licence
@file: cnn_lstm_model.py
@time: 2019-01-19 11:52

"""
import logging

from keras.layers import Dense, Conv1D, MaxPooling1D
from keras.layers.recurrent import LSTM
from keras.models import Model

from kashgari.tasks.classification.base_model import ClassificationModel


class CNNLSTMModel(ClassificationModel):
    __base_hyper_parameters__ = {
        'conv_layer': {
            'filters': 32,
            'kernel_size': 3,
            'padding': 'same',
            'activation': 'relu'
        },
        'max_pool_layer': {
            'pool_size': 2
        },
        'lstm_layer': {
            'units': 100
        }
    }

    def build_model(self):
        base_model = self.embedding.model
        conv_layer = Conv1D(**self.hyper_parameters['conv_layer'])(base_model.output)
        max_pool_layer = MaxPooling1D(**self.hyper_parameters['max_pool_layer'])(conv_layer)
        lstm_layer = LSTM(**self.hyper_parameters['lstm_layer'])(max_pool_layer)
        dense_layer = Dense(len(self.label2idx), activation='sigmoid')(lstm_layer)
        output_layers = [dense_layer]

        model = Model(base_model.inputs, output_layers)
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        self.model = model
        self.model.summary()


if __name__ == "__main__":
    from kashgari.utils.logger import init_logger
    from kashgari.corpus import TencentDingdangSLUCorpus

    init_logger()

    x_data, y_data = TencentDingdangSLUCorpus.get_classification_data()
    classifier = CNNLSTMModel()
    classifier.fit(x_data, y_data, epochs=1)
    classifier.save('./classifier_saved2')

    model = ClassificationModel.load_model('./classifier_saved2')
    logging.info(model.predict('我要听音乐'))
