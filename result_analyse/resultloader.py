import general.utils as utils
from ipywidgets import interact, interactive, fixed, interact_manual
import logging
logger = logging.getLogger(__file__)
import os
import pandas as pd
import sklearn.metrics
from metric.CMbasedMetric import CMbasedMetric
from combiner.SimpleCombiner import SimpleCombiner
def getRunTable(run_info,dataset,evalres):
    df=pd.DataFrame(columns=['fold','type','accuracy','precision','recall','f1','runname'])
    combiner=SimpleCombiner()
    for i in range(len(evalres)):
        Sdata=evalres[i].Sdata
       # pred_events=combiner.combine(Sdata.s_event_list,Sdata.set_window,evalres[i].predicted)
        
        quality=evalres[i].quality
        #print('Evalution quality fold=%d is %s' % (i, quality))
        df=df.append({
            'dataset':run_info['dataset'],
            'date':run_info['run_date'], 
            'runname':evalres[i].shortrunname,
            'fold':i,
            'type':'event',
            'accuracy':quality['accuracy'],
            'precision':quality['precision'],
            'recall':quality['recall'],
            'f1':quality['f1'],
            'params':str(evalres[i].params['segmentor'])
        }, ignore_index=True)
        cm=sklearn.metrics.confusion_matrix(evalres[i].Sdata.label, evalres[i]. predicted_classes)
        quality=CMbasedMetric(cm,'macro')
        #print('classical quality:%s'%(quality))
        df=df.append({
            'dataset':run_info['dataset'],
            'date':run_info['run_date'], 
            'runname':evalres[i].shortrunname,
            'fold':i,
            'type':'classic',
            'accuracy':quality['accuracy'],
            'precision':quality['precision'],
            'recall':quality['recall'],
            'f1':quality['f1'],
            'params':str(evalres[i].params['segmentor'])
        }, ignore_index=True)
    return df

def get_all_runs_table():
    list=os.listdir('save_data/')
    list.sort(key=lambda f:os.path.getmtime('save_data/'+f),reverse=True)
    result=[]
	
    for item in list:
        # if not ('A4H' in item):continue
        try:
            res=utils.loadState(item)
            if(len(res)!=3):
                #raise Error
                logger.warn('File %s can not import'%item)
                continue
            [run_info,datasetdscr,evalres]=res
            result.append(getRunTable(run_info,datasetdscr,evalres))
        except Exception as e:
            logger.warn('File %s can not import error '%item)
            import sys
            import traceback
            print(e, file=sys.stderr)
            traceback.print_exc()

    return pd.concat(result)


def get_runs():
    list=os.listdir('save_data/')
    list.sort(key=lambda f:os.path.getmtime('save_data/'+f),reverse=True)
    result=[]
    for item in list:
        
        try:
            # res=utils.loadState(item)
            # if(len(res)!=3):
            #     raise Error
            # [run_info,datasetdscr,evalres]=res
            # disp_name='dataset:%s date:%s %s'%(run_info['dataset'],run_info['run_date'], evalres[0].shortrunname)
            disp_name=item
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
    get_all_runs_table()

