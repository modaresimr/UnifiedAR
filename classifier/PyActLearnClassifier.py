from pyActLearn.learning.nn.mlp import MLP
import pyActLearn.learning.nn.lstm
import tensorflow as tf
from classifier.classifier_abstract import Classifier
from pyActLearn.learning.nn.sda import SDA


class PyActLearnClassifier(Classifier):
    def createmodel(self, inputsize, outputsize):
        raise NotImplementedError

    def train(self, trainset, trainlabel):
        raise NotImplementedError

    def evaluate(self, testset, testlabel):
        raise NotImplementedError

    def predict(self, testset):
        raise NotImplementedError

    def predict_classes(self, testset):
        raise NotImplementedError

    def save(self, desc):
        raise NotImplementedError

    def load(self, desc):
        raise NotImplementedError


class PAL_NN(Classifier):

    def createmodel(self, inputsize, outputsize):
        raise NotImplementedError

    def train(self, trainset, trainlabel):
        self.model.fit(trainset, trainlabel, iter_num=5000, batch_size=100,
                       criterion='monitor_based')  # summaries_dir=log_dir

    def evaluate(self, testset, testlabel):
        raise NotImplementedError

    def predict(self, testset):
        return self.model.predict_proba(testset)

    def predict_classes(self, testset):
        return self.model.predict(testset)

    def save(self, file):
        tf.saved_model.save(self.model.sess, file+'pyact.h5')

    def load(self, file):
        self.model = MLP(0, 0, [1000])
        self.model.sess = tf.saved_model.load(file+"pyact.h5")


class PAL_MLP(PAL_NN):

    def createmodel(self, inputsize, outputsize):
        self.model = MLP(inputsize, outputsize, [1000])
        return self.model


class PAL_LSTM(PAL_NN):

    def createmodel(self, inputsize, outputsize):
        self.model = lstm.LSTM(inputsize, outputsize, numhidden=1000,
                               num_units=300, num_skip=100)
        return self.model


class PAL_LSTM_Simple(PAL_NN):

    def createmodel(self, inputsize, outputsize):
        self.model = lstm.SimpleLSTM(inputsize, outputsize, numhidden=1000,
                                     num_units=300, num_skip=100)
        return self.model


class PAL_LSTM_Legacy(PAL_NN):

    def createmodel(self, inputsize, outputsize):
        self.model = lstm.LSTM_Legacy(
            inputsize, outputsize, num_units=300, num_steps=100)
        return self.model


class PAL_SDA(PAL_NN):
    """Stacked Auto-encoder
    """

    def createmodel(self, inputsize, outputsize):
        self.model = SDA(inputsize, outputsize, [300, 300, 300])
        return self.model
