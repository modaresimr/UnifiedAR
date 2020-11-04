import numpy as np

def mergeEvals(dataset,evalres,evalobj):
    res={'avg':{}}
    
    for act in range(1,len(dataset.activities_map)):
        
        res[act]={'avg':{}}
        
        for fold in evalres:
            print('eval for act=%d fold=%d'%(act,fold),end ="\r")
            real_events=evalres[fold]['test'].real_events
            pred_events=evalres[fold]['test'].pred_events
            metr=evalobj.eval(real_events,pred_events,[act])
            # print(metr)
            print('.',end='')
            res[act]['avg']=add2Avg(res[act]['avg'] ,metr,len(evalres))
            res[act][fold]=metr

        res['avg']=add2Avg(res['avg'],res[act]['avg'],len(dataset.activities_map))
        print('.')
    return res




def add2Avg (oldd,newd,count):
    for item in newd:
        if type(newd[item])==type({}):
            oldd[item]=add2Avg(oldd[item] if item in oldd else {},newd[item],count)
        else:
            if not(item in oldd):oldd[item]=0

            oldd[item]+=np.array(newd[item])/count
    return oldd