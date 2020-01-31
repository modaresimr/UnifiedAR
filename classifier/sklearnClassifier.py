from classifier.classifier_abstract import Classifier
import sklearn.ensemble
import sklearn.neighbors
import sklearn.svm
import sklearn.tree

class sklearnClassifier(Classifier):
    def applyParams(self, params):
        return super().applyParams(params)

    def createmodel(self, inputsize, outputsize):
        self.model = self.createmodel(inputsize, outputsize)
        return self.model

    def getmodel(self, inputsize, outputsize):
        raise NotImplementedError

    def train(self, trainset, trainlabel):
        return self.model.fit(trainset, trainlabel, self.params)

    def evaluate(self, testset, testlabel):
        self.model.evaluate(testset, testlabel)

    def predict(self, testset):
        return self.model.predict_proba(testset)

    def predict_classes(self, testset):
        return self.model.predict(testset)


class UAR_KNN(sklearnClassifier):
    def applyParams(self, params):
        self.k = params.get('k', 5)
        return super().applyParams(params)

    def getmodel(self, inputsize, outputsize):
        return sklearn.neighbors.KNeighborsClassifier(n_neighbors=self.k)


class UAR_RandomForest(sklearnClassifier):
    def applyParams(self, params):
        self.n_estimators = params.get('n_estimators', 20)
        self.random_state = params.get('random_state', 0)
        return super.applyParams(params)

    def getmodel(self, inputsize, outputsize):
        return sklearn.ensemble.RandomForestClassifier(self.n_estimators, self.random_state)


class UAR_SVM(sklearnClassifier):
    def applyParams(self, params):
        self.kernel = params.get('kernel', 'rbf')
        return super.applyParams(params)

    def getmodel(self, inputsize, outputsize):
        return sklearn.svm.SVC(kernel=self.kernel)

class UAR_DecisionTree(sklearnClassifier):
    def applyParams(self, params):
        return super.applyParams(params)
        
    def getmodel(self, inputsize, outputsize):
        return sklearn.tree.DecisionTreeClassifier()
