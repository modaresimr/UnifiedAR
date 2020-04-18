from classifier.classifier_abstract import Classifier
import tensorflow as tf
import tensorflow_addons as tfa
from sklearn.utils.class_weight import compute_class_weight


import numpy as np
import logging
logger = logging.getLogger(__file__)

class KerasClassifier(Classifier):
    
    @staticmethod
    def tf_f1_score(y_true, y_pred):
        """Computes 3 different f1 scores, micro macro
        weighted.
        micro: f1 score accross the classes, as 1
        macro: mean of f1 scores per class
        weighted: weighted average of f1 scores per class,
                weighted from the support of each class


        Args:
            y_true (Tensor): labels, with shape (batch, num_classes)
            y_pred (Tensor): model's predictions, same shape as y_true

        Returns:
            tuple(Tensor): (micro, macro, weighted)
                        tuple of the computed f1 scores
        """

        f1s = [0, 0, 0]

        y_true = tf.cast(y_true, tf.float64)
        y_pred = tf.cast(y_pred, tf.float64)

        for i, axis in enumerate([None, 0]):
            TP = tf.math.count_nonzero(y_pred * y_true, axis=axis)
            FP = tf.math.count_nonzero(y_pred * (y_true - 1), axis=axis)
            FN = tf.math.count_nonzero((y_pred - 1) * y_true, axis=axis)

            precision = TP / (TP + FP)
            recall = TP / (TP + FN)
            f1 = 2 * precision * recall / (precision + recall)

            f1s[i] = tf.reduce_mean(f1)

        weights = tf.reduce_sum(y_true, axis=0)
        weights /= tf.reduce_sum(weights)

        f1s[2] = tf.reduce_sum(f1 * weights)

        micro, macro, weighted = f1s
        return micro

    # @staticmethod
    # def f1(y_true, y_pred):
    #     K=tf.keras.backend
    #     y_true=K.cast(y_true, 'float')
    #     y_pred = K.round(y_pred)
    #     tp = K.sum(K.cast(y_true*y_pred, 'float'), axis=0)
    #     tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
    #     fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    #     fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    #     p = tp / (tp + fp + K.epsilon())
    #     r = tp / (tp + fn + K.epsilon())

    #     f1 = 2*p*r / (p+r+K.epsilon())
    #     f1 = tf.where(tf.math.is_nan(f1), tf.zeros_like(f1), f1)
    #     return K.mean(f1)
    def _createmodel(self, inputsize, outputsize):
        self.outputsize = outputsize
        a=tfa.metrics.F1Score(num_classes=outputsize,average='micro')
        a.average ='macro'
        METRICS = [
            #   tf.keras.metrics.TruePositives(name='tp'),
            #   tf.keras.metrics.FalsePositives(name='fp'),
            #   tf.keras.metrics.TrueNegatives(name='tn'),
            #   tf.keras.metrics.FalseNegatives(name='fn'),
            # CategoricalTruePositives(name='tp',num_classes=outputsize,batch_size=500),
            # KerasClassifier.tf_f1_score,
            # a,
            tf.keras.metrics.SparseCategoricalAccuracy(name='acc'),
            # tf.keras.metrics.BinaryAccuracy(name='accuracy'),
            # tf.keras.metrics.Precision(name='precision'),
            # tf.keras.metrics.Recall(name='recall'),
            # tf.keras.metrics.AUC(name='auc'),
        ]
        
        loss=tfa.losses.sparsemax_loss
        loss=tfa.losses.sigmoid_focal_crossentropy
        loss='sparse_categorical_crossentropy'
        model = self.getmodel(inputsize, outputsize)
        model.summary()
        model.compile(
            optimizer='adam',loss=loss, metrics=METRICS)
        self.model = model
        return model

    def getmodel(self, inputsize, outputsize):
        raise NotImplementedError
    
    def _train(self, trainset, trainlabel):
        if(np.max(trainlabel)==0):
            self.trained=False
            return
        
        cw = compute_class_weight("balanced", range(self.outputsize), trainlabel)
        return self.model.fit(trainset, trainlabel, epochs=self.epochs, 
        # validation_split=0.2,
        class_weight=cw
        )
        self.trained=True

    def _evaluate(self, testset, testlabel):
        if(self.trained):
            self.model.evaluate(testset, testlabel)
        else:
            print("model not trained")

    def _predict(self, testset):
        if(self.trained):
            return self.model.predict(testset)
        else:
            return self.model.predict(testset)*0
        

    def _predict_classes(self, testset):
        if(self.trained):
            return self.model.predict_classes(testset)
        else:
            return self.model.predict_classes(testset)*0

    def save(self, file):
        logger.debug('saving model to %s', file)
        self.model.save(file+'.h5')

    def load(self, file):
        logger.debug('loading model from %s', file)
        if not('.h5' in file):
            file = file+'.h5'
        self.model = tf.keras.models.load_model(file)


class SequenceNN(KerasClassifier):
    def _reshape(self, data):
        if(len(data.shape) == 2):
            return np.reshape(
                data, (data.shape[0], 1, data.shape[1]))
        return data

    

class LSTMTest(SequenceNN):

    def getmodel(self, inputsize, outputsize):

        return tf.keras.models.Sequential([
			# tf.keras.layers.Dense(128, input_shape=inputsize),
            # tf.keras.layers.Embedding(input_dim=inputsize,output_dim=100),
            tf.keras.layers.LSTM(128, activation=tf.nn .relu,input_shape=inputsize),
            #tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(outputsize, activation=tf.nn.softmax)
        ], name=self.shortname())


class SimpleKeras(KerasClassifier):
    def getmodel(self, inputsize, outputsize):
        return tf.keras.models.Sequential([
            tf.keras.layers.Dense(128, input_shape=inputsize),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(outputsize, activation=tf.nn.softmax)
        ], name=self.shortname())


class WangMLP(KerasClassifier):

    def getmodel(self, inputsize, outputsize):
        from pyActLearn.learning.nn.mlp import MLP
        return MLP(inputsize, outputsize, [1000])


class CategoricalTruePositives(tf.keras.metrics.Metric):
    import tensorflow.keras.backend as K

    def __init__(self, num_classes, batch_size,
                 name="categorical_true_positives", **kwargs):
        super(CategoricalTruePositives, self).__init__(name=name, **kwargs)

        self.batch_size = batch_size
        self.num_classes = num_classes

        self.cat_true_positives = self.add_weight(
            name="ctp", initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):

        y_true = K.argmax(y_true, axis=-1)
        y_pred = K.argmax(y_pred, axis=-1)
        y_true = K.flatten(y_true)

        true_poss = K.sum(K.cast((K.equal(y_true, y_pred)), dtype=tf.float32))

        self.cat_true_positives.assign_add(true_poss)

    def result(self):

        return self.cat_true_positives
