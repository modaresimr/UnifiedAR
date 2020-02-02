
from sklearn.metrics import confusion_matrix

from feature_extraction.feature_abstract import featureExtraction
from general.utils import Data, MyTask
from metric.CMbasedMetric import CMbasedMetric
from metric.event_confusion_matrix import event_confusion_matrix
from metric.EventBasedMetric import EventBasedMetric
from ml_strategy import MLStrategy
from optimizer.BruteForce import method_param_selector
from optimizer.OptLearn import OptLearn, ParamMaker
from segmentation.segmentation_abstract import prepare_segment


class SimpleStrategy(MLStrategy):
    def train(self, datasetdscr, data, acts):
        self.datasetdscr=datasetdscr
        self.acts=acts
        self.traindata=self.justifySet(self.acts,data)
        bestOpt=method_param_selector(self.learning)
        self.functions=bestOpt.functions
        




    def learning(self,func):
        func.acts=self.acts
        Tdata=func.preprocessor.process(self.datasetdscr, self.traindata)
        Sdata=prepare_segment(func,Tdata,self.datasetdscr)
        Sdata.set=featureExtraction(func.featureExtractor,self.datasetdscr,Sdata.set_window,True)
        # import pickle
        # with open('objs1.pkl', 'wb') as f: 
        #     pickle.dump([Sdata.set,Sdata.label, func], f)
        
        func.classifier.createmodel(Sdata.set[0].shape,len(self.acts))
        func.classifier.train(Sdata.set, Sdata.label) 
        
        predicted=func.classifier.predict(Sdata.set)
        pred_events=func.combiner.combine(Sdata.set_window,predicted)
        #eventeval=EventBasedMetric(Sdata.a_events,pred_events,self.acts)
        event_cm=event_confusion_matrix(Sdata.a_events,pred_events,self.acts)
        quality=CMbasedMetric(event_cm,'macro')
        return quality.f1
        
        
    def test(self, data):
        func=self.functions
        data=self.justifySet(self.acts,data)
        func.acts=self.acts

        Tdata=func.preprocessor.process(self.datasetdscr, data)
        Sdata=prepare_segment(func,Tdata,self.datasetdscr)
        Sdata.set=featureExtraction(func.featureExtractor,None,Sdata.set_window,False)
        result=Data('TestResult')
        result.Sdata=Sdata
        result.predicted=func.classifier.predict(Sdata.set)
        result.predictedclasses=func.classifier.predict_classes(Sdata.set)    

        pred_events=self.functions.combiner.combine(Sdata.set_window,result.predicted)
        
        result.pred_events=pred_events
        result.real_events=data.a_events
        
        return result

    