import auto_profiler
import logging

from sklearn.metrics import confusion_matrix

from feature_extraction.feature_abstract import featureExtraction
from general.utils import Data, MyTask
import general.utils
from metric.CMbasedMetric import CMbasedMetric
from metric.event_confusion_matrix import event_confusion_matrix
# from metric.EventBasedMetric import EventBasedMetric
import ml_strategy.abstract
from optimizer.BruteForce import method_param_selector
from optimizer.OptLearn import OptLearn, ParamMaker
from segmentation.segmentation_abstract import prepare_segment,prepare_segment2

logger = logging.getLogger(__file__)

class SimpleStrategy(ml_strategy.abstract.MLStrategy):
    def train(self, datasetdscr, data, acts):
        self.datasetdscr=datasetdscr
        self.acts=acts
        self.traindata=self.justifySet(self.acts,data)
        bestOpt=method_param_selector(self.learning)
        self.functions=bestOpt.functions
        



    @auto_profiler.Profiler(depth=3, on_disable=general.utils.logProfile)
    def learning(self,func):
        result=self.pipeline(func,self.traindata,train=True)
        return result.quality['f1']
        

    def pipeline(self,func,data,train):
        func.acts=self.acts
        logger.debug('Starting .... %s' % (func.shortrunname))
        Tdata=func.preprocessor.process(self.datasetdscr, data)
        logger.debug('Preprocessing Finished %s' % (func.preprocessor.shortname()))
        Sdata=prepare_segment2(func,Tdata,self.datasetdscr)
        logger.debug('Segmentation Finished %d segment created %s' % (len(Sdata.set_window), func.segmentor.shortname()))
        Sdata.set=featureExtraction(func.featureExtractor,self.datasetdscr,Sdata,True)
        logger.debug('FeatureExtraction Finished shape %s , %s' % (str(Sdata.set.shape), func.featureExtractor.shortname()))
        if(train):
            func.classifier.createmodel(Sdata.set[0].shape,len(self.acts))
            logger.debug('Classifier model created  %s' % (func.classifier.shortname()))
            func.classifier.train(Sdata.set, Sdata.label) 
            logger.debug('Classifier model trained  %s' % (func.classifier.shortname()))

        logger.info("Evaluating....")
        result=Data('Result')
        result.shortrunname=func.shortrunname
        result.Sdata=Sdata
        result.functions={}
        for f in func.__dict__:
            obj = func.__dict__[f]
            if isinstance(obj, MyTask):              
                result.functions[f]=(obj.shortname(),obj.params)

        
        result.predicted        =func.classifier.predict(Sdata.set)
        result.predicted_classes=func.classifier.predict_classes(Sdata.set)    
        pred_events =func.combiner.combine(Sdata.s_event_list,Sdata.set_window,result.predicted)
        logger.debug('events merged  %s' % (func.combiner.shortname()))
        
        
        result.pred_events  =pred_events
        result.real_events  =data.a_events

        result.event_cm     =event_confusion_matrix(data.a_events,pred_events,self.acts)
        result.quality      =CMbasedMetric(result.event_cm,'macro')
        #eventeval=EventBasedMetric(Sdata.a_events,pred_events,self.acts)
        
        logger.debug('Evalution quality is %s'%result.quality)
        return result

    def test(self, data):
        func=self.functions
        data=self.justifySet(self.acts,data)
        func.acts=self.acts
        result=self.pipeline(func,data,train=False)
        return result

    
    