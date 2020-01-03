from classifier.KerasClassifier import KerasClassifier
import tensorflow as tf

class SimpleKeras(KerasClassifier):
    
    def getmodel(self,inputsize,outputsize) :
         return tf.keras.models.Sequential([
            tf.keras.layers.Dense(128,input_shape=[inputsize]),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(outputsize, activation=tf.nn.softmax)
        ],name=self.shortname()+" Main Classifier")   
   