from classifier.classifier_abstract import Classifier
import tensorflow as tf


class KerasClassifier(Classifier):
    def applyParams(self, params):
        self.epochs = params['epochs']
        return super().applyParams(params)

    def createmodel(self, inputsize, outputsize):
        model = self.getmodel(inputsize, outputsize)
        model.summary()
        model.compile(
            optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.model = model
        return model

    def getmodel(self, inputsize, outputsize):
        raise NotImplementedError

    def train(self, trainset, trainlabel):
       # trainset  =   np.reshape(trainset, (trainset.shape[0], 1, trainset.shape[1]))
        #self.model.fit(trainset, trainlabel, epochs=self.epochs)
        return self.model.fit(trainset, trainlabel, epochs=self.epochs)

    def evaluate(self, testset, testlabel):

        self.model.evaluate(testset, testlabel)

    def predict(self, testset):
        #testset  =   np.reshape(testset, (testset.shape[0], 1, testset.shape[1]))
        return self.model.predict(testset)

    def predict_classes(self, testset):
        #testset  =   np.reshape(testset, (testset.shape[0], 1, testset.shape[1]))
        return self.model.predict_classes(testset)

    def save(self, file):
        print('saving model to', file)
        self.model.save(file+'.h5')

    def load(self, file):
        print('loading model from', file)
        if not('.h5' in file):
            file = file+'.h5'
        self.model = tf.keras.models.load_model(file)


class LSTMTest(KerasClassifier):

    def getmodel(self, inputsize, outputsize):
        
        return tf.keras.models.Sequential([
            # tf.keras.layers.Dense(128,input_shape=(1,inputsize)),
            tf.keras.layers.LSTM(128, activation=tf.nn .relu),
            #tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(outputsize, activation=tf.nn.softmax)
        ], name=self.shortname()+" Main Classifier")


class SimpleKeras(KerasClassifier):

    def getmodel(self, inputsize, outputsize):
        return tf.keras.models.Sequential([
            tf.keras.layers.Dense(128, input_shape=[inputsize]),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(outputsize, activation=tf.nn.softmax)
        ], name=self.shortname()+" Main Classifier")


class WangMLP(KerasClassifier):
    from pyActLearn.learning.nn.mlp import MLP

    def getmodel(self, inputsize, outputsize):
        return MLP(inputsize, outputsize, [1000])
