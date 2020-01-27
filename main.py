

# from activity_fetcher import *
from constants import *
from general.utils import saveState

# from datatool import *
# from evaluation import *
# from feature_extraction import *
# from general import *
# from metric import *
# from preprocessing import *
# from segmentation import *

   
datasetdscr=methods.dataset[1]['method']().load()
strategy=methods.mlstrategy[0]['method']()
evalres=methods.evaluation[0]['method']().evaluate(datasetdscr,strategy)
# cm=confusion_matrix(Sdata.label,result.predictedclasses,self.acts)
#         event_cm=event_confusion_matrix(Sdata.a_events,pred_events,self.acts)
#         result.cm=cm
#         result.event_cm=event_cm
# result.eventeval=EventBasedMetric(Sdata.a_events,pred_events,Sdata.acts)

saveState([datasetdscr,evalres.real_events,evalres.pred_events],datasetdscr.shortname()+'r1')
# print(strategy.evaluate(evalres))
