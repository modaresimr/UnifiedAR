from classifier.classifier_abstract import *

class SVMClassifier(Classifier):
    def applyParams(self,params):
        
        return super().applyParams(params);

    def createmodel(self,inputsize,outputsize):
        from sklearn import svm
        model = svm.SVC(kernel='rbf',gamma=1, decision_function_shape='ovo',probability=True)
        self.model=model
        return model

    def train(self,trainset,trainlabel):
#         global svmc
#         svmc=self
#         self.trainset=trainset
#         self.trainlabel=trainlabel
        
        self.model.fit(trainset, trainlabel)

#     def evaluate(self,testset,testlabel):
#         plbl=self.predict_classes(testset)
        
#         self.model.evaluate(testset, testlabel)
    
    def predict(self,testset):
        return self.model.predict_proba(testset)

    def predict_classes(self,testset):
        return self.model.predict(testset)    

    def save(self,desc):
        print('saving ',desc)
        

    def loadmodel(self,desc): 
        print('loading ',desc)
        