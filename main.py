

# from activity_fetcher import *
from constants import methods
import general.utils as utils
import logging
import argparse
logger = logging.getLogger(__file__)
# from datatool import *
# from evaluation import *
# from feature_extraction import *
# from general import *
# from metric import *
# from preprocessing import *
# from segmentation import *
if __name__ == '__main__':
    args_ok = False
    parser = argparse.ArgumentParser(description='Run on datasets.')
    #parser.add_argument('-d', '--dataset', help=' to original datasets')
    parser.add_argument('-o', '--output', help='Output folder')
    #parser.add_argument('--h5py', help='HDF5 dataset folder')
    args = parser.parse_args()
    utils.configurelogger(logging, args.output)

    datasetdscr = methods.dataset[0]['method']().load()
    strategy = methods.mlstrategy[0]['method']()
    evalres = methods.evaluation[0]['method']().evaluate(datasetdscr, strategy)
    # cm=confusion_matrix(Sdata.label,result.predictedclasses,self.acts)
    #         event_cm=event_confusion_matrix(Sdata.a_events,pred_events,self.acts)
    #         result.cm=cm
    #         result.event_cm=event_cm
    # result.eventeval=EventBasedMetric(Sdata.a_events,pred_events,Sdata.acts)

    utils.saveState([datasetdscr, evalres.real_events, evalres.pred_events],
                    datasetdscr.shortname()+'r1')
    # print(strategy.evaluate(evalres))
