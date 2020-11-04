

import argparse
from datetime import datetime
import logging

import general.utils as utils

import auto_profiler
from constants import methods

import general.utils
@auto_profiler.Profiler(depth=8, on_disable=general.utils.logProfile)
def run(args):
    logger = logging.getLogger(__file__)
    logger.debug(f'args={args}')
    
    if(args.dataset<0):
        logger.error('Invalid dataset argument')
        return
    
    if(args.mlstrategy<0):
        logger.error('Invalid mlstrategy argument')
        return
        
    if(args.evaluation<0):
        logger.error('Invalid evaluation argument')
        return
    datasetdscr = methods.dataset[args.dataset]['method']().load()
    strategy = methods.mlstrategy[args.mlstrategy]['method']()
    evaluation=methods.evaluation[args.evaluation]['method']()
    
    if(args.feature_extraction>=0): methods.feature_extraction=[methods.feature_extraction[args.feature_extraction]]
    if(args.segmentation>=0): methods.segmentation=[methods.segmentation[args.segmentation]]
    if(args.classifier>=0): methods.classifier=[methods.classifier[args.classifier]]
    
    evalres = evaluation.evaluate(datasetdscr, strategy)

    run_date=datetime.now().strftime('%y%m%d_%H-%M-%S')
    run_info={'dataset':datasetdscr.shortname(),'run_date':run_date,'dataset_path':datasetdscr.data_path, 'strategy':strategy.shortname(),'evalution':evaluation.shortname()}
    compressdata={'run_info':run_info, 'folds':{k:{'quality':evalres[k]['test'].quality,'runname':evalres[k]['test'].shortrunname} for k in evalres}}
    
    utils.saveState([compressdata],'%s-%s/' % (run_date,datasetdscr.shortname()),'info')
    utils.saveState([run_info,datasetdscr, evalres],'%s-%s/' % (run_date,datasetdscr.shortname()))
    for i in range(len(evalres)):
        logger.debug(f'Evalution quality fold={i} is {evalres[i]["test"].quality}')

    logger.debug(f'run finished args={args}')


def Main(argv):
    strargs=str(argv)

    auto_profiler.Profiler.GlobalDisable=True
    parser = argparse.ArgumentParser(description='Run on datasets.')
    parser.add_argument( '--dataset','-d', help=' to original datasets',type=int, default=0)
    parser.add_argument( '--output','-o', help='Output folder', default='logs')
    parser.add_argument( '--mlstrategy','-st', help='Strategy',type=int, default=0)
    parser.add_argument( '--segmentation','-s', help='segmentation',type=int, default=-1)
    parser.add_argument( '--feature_extraction','-f',type=int, default=0)
    parser.add_argument( '--classifier',type=int,default=0)
    parser.add_argument('--evaluation', help='evaluation',type=int, default=0)
    parser.add_argument('--comment','-c',help='comment',default='')
    #parser.add_argument('--h5py', help='HDF5 dataset folder')
    args = parser.parse_args(argv)
    
    utils.configurelogger(__file__, args.output,strargs)
    import numpy
    import os
    os.system("taskset -p 0xff %d" % os.getpid())
    run(args)

if __name__ == '__main__':
    import sys
    strargs=str(sys.argv[1:])
    Main(sys.argv[1:])
# https://stackoverflow.com/questions/39063676/how-to-boost-a-keras-based-neural-network-using-adaboost
