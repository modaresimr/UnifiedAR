import general.utils as utils
from ipywidgets import interact, interactive, fixed, interact_manual
import logging
logger = logging.getLogger(__file__)
import os

def get_runs():
    list=os.listdir('save_data/')
    list.sort(key=lambda f:os.path.getmtime('save_data/'+f))
    result=[]
    for item in list:
        try:
            res=utils.loadState(item)
            if(len(res)!=3):
                raise Error
            [run_info,datasetdscr,evalres]=res
            disp_name='dataset:%s date:%s %s'%(run_info['dataset'],run_info['run_date'], evalres[0].shortrunname)
            result.append((disp_name,item))
        except:
            logger.warn('File %s can not import'%item)
    return result


def display_result(file):
    [run_info,datasetdscr,evalres]=utils.loadState(file)
    for i in range(len(evalres)):
        quality=evalres[i].quality
        logger.debug('Evalution quality fold=%d is f1=%.2f acc=%.2f precision=%.2f recall=%.2f' % (i, quality.f1,quality.accuracy,quality.precision,quality.recall))

if __name__ == '__main__':
    get_runs()

