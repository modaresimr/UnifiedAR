

import argparse
from datetime import datetime
import logging

import general.utils as utils
# from activity_fetcher import *
import auto_profiler
from constants import methods

# from datatool import *
# from evaluation import *
# from feature_extraction import *
# from general import *
# from metric import *
# from preprocessing import *
# from segmentation import *
import general.utils
@auto_profiler.Profiler(depth=8, on_disable=general.utils.logProfile)
def run(args):
    
    logger.debug(f'args={args}')
    datasetdscr = methods.dataset[args.dataset]['method']().load()
 
    strategy = methods.mlstrategy[args.strategy]['method']()
    evaluation=methods.evaluation[0]['method']()
    evalres = evaluation.evaluate(datasetdscr, strategy)

    run_date=datetime.now().strftime('%y%m%d_%H-%M-%S')
    run_info={'dataset':datasetdscr.shortname(),'run_date':run_date,'dataset_path':datasetdscr.data_path, 'strategy':strategy.shortname(),'evalution':evaluation.shortname()}
    compressdata={'run_info':run_info, 'folds':{k:{'quality':evalres[k].quality,'runname':evalres[k].shortrunname} for k in evalres}}
    utils.saveState([compressdata],'%s-%s/' % (run_date,datasetdscr.shortname()),'info')
    utils.saveState([run_info,datasetdscr, evalres],'%s-%s/' % (run_date,datasetdscr.shortname()))
    for i in range(len(evalres)):
        quality=evalres[i].quality
        logger.debug('Evalution quality fold=%d is %s' % (i, quality))
        
    logger.debug(f'args={args}')


if __name__ == '__main__':
    args_ok = False
    auto_profiler.Profiler.GlobalDisable=False
    parser = argparse.ArgumentParser(description='Run on datasets.')
    parser.add_argument('-d', '--dataset', help=' to original datasets',type=int, default=1)
    parser.add_argument('-o', '--output', help='Output folder', default='logs')
    parser.add_argument('-s', '--strategy', help='Strategy',type=int, default=0)
    #parser.add_argument('--h5py', help='HDF5 dataset folder')
    args = parser.parse_args()
    utils.configurelogger(__file__, args.output)
    logger = logging.getLogger(__file__)
    run(args)


#https://stackoverflow.com/questions/39063676/how-to-boost-a-keras-based-neural-network-using-adaboost