from classifier.classifier_abstract import *
class KerasClassifier(Classifier):
    def applyParams(self,params):
        self.epochs=params['epochs']
        return super().applyParams(params);

    def createmodel(self,inputsize,outputsize):
        model = self.getmodel(inputsize,outputsize); 
        model.summary()
        model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
        self.model=model
        return model

    def getmodel(self,inputsize,outputsize) :
        pass

    def train(self,trainset,trainlabel):
       # trainset  =   np.reshape(trainset, (trainset.shape[0], 1, trainset.shape[1]))
        #self.model.fit(trainset, trainlabel, epochs=self.epochs)
        self.model.fit(trainset, trainlabel, epochs=self.epochs)

    def evaluate(self,testset,testlabel):
        
        self.model.evaluate(testset, testlabel)
    
    def predict(self,testset):
        #testset  =   np.reshape(testset, (testset.shape[0], 1, testset.shape[1]))
        return self.model.predict(testset)

    def predict_classes(self,testset):
        #testset  =   np.reshape(testset, (testset.shape[0], 1, testset.shape[1]))
        return self.model.predict_classes(testset)    

    def save(self,desc):
        print('saving ',desc)
        tf.contrib.saved_model.save_keras_model(model, "./saved_models/"+desc+"/")

    def loadmodel(self,desc): 
        print('loading ',desc)
        self.model=tf.contrib.saved_model.load_keras_model("./saved_models/"+desc+"/")