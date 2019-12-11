from general.utils import MyTask

class Classifier(MyTask):
    def createmodel(self,inputsize,outputsize):
        pass
    def train(self,trainset,trainlabel):
        pass
    def evaluate(self,testset,testlabel):
        pass
    def predict(self,testset):
        pass
    def predict_classes(self,testset):
        pass
    def save(self,desc):
        pass
    def load(self,desc):
        pass