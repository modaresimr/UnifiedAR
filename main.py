

import argparse
from datetime import datetime
import logging

import general.utils as utils
# from activity_fetcher import *
from constants import methods
import auto_profiler

# from datatool import *
# from evaluation import *
# from feature_extraction import *
# from general import *
# from metric import *
# from preprocessing import *
# from segmentation import *
if __name__ == '__main__':
    args_ok = False
    auto_profiler.Profiler.GlobalDisable=True
    parser = argparse.ArgumentParser(description='Run on datasets.')
    parser.add_argument('-d', '--dataset', help=' to original datasets', default=1)
    parser.add_argument('-o', '--output', help='Output folder', default='logs')
    #parser.add_argument('--h5py', help='HDF5 dataset folder')
    args = parser.parse_args()
    utils.configurelogger(__file__, args.output)
    logger = logging.getLogger(__file__)
    
    datasetdscr = methods.dataset[int(args.dataset)]['method']().load()
 
    strategy = methods.mlstrategy[0]['method']()
    evaluation=methods.evaluation[0]['method']()
    evalres = evaluation.evaluate(datasetdscr, strategy)

    run_date=datetime.now().strftime('%y%m%d_%H-%M-%S')
    run_info={'dataset':datasetdscr.shortname(),'run_date':run_date,'dataset_path':datasetdscr.data_path, 'strategy':strategy.shortname(),'evalution':evaluation.shortname()}

    utils.saveState([run_info,datasetdscr, evalres],'%s-%s/' % (run_date,datasetdscr.shortname()))
    for i in range(len(evalres)):
        quality=evalres[i].quality
        logger.debug('Evalution quality fold=%d is %s' % (i, quality))
        
