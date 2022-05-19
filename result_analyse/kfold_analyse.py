import numpy as np

def mergeEvals(dataset,evalres,evalobj):
    if(evalobj.classical):
        return mergeEvalsClassic(dataset,evalres,evalobj)

    
    res={'avg':{}}
    
    for act in range(1,len(dataset.activities_map)):
        
        res[act]={'avg':{}}
        
        for fold in evalres:
            print('eval for act=%d fold=%d'%(act,fold),end ="\r")
            real_events=evalres[fold]['test'].real_events
            pred_events=evalres[fold]['test'].pred_events
            metr=evalobj.eval(real_events,pred_events,[act])
            # print(metr)
            # print('.',end='')
            res[act]['avg']=add2Avg(res[act]['avg'] ,metr,len(evalres))
            res[act][fold]=metr

        res['avg']=add2Avg(res['avg'],res[act]['avg'],len(dataset.activities_map))
        # print('.')
        # print(res);
    return res

def mergeEvalsClassic(dataset,evalres,evalobj):
    res={'avg':{}}
    
    for act in range(1,len(dataset.activities_map)):
        
        res[act]={'avg':{}}
        
        for fold in evalres:
            print('eval for act=%d fold=%d'%(act,fold),end ="\r")
            real_events=evalres[fold]['test'].Sdata.label
            pred_events=evalres[fold]['test'].predicted_classes
            metr=evalobj.eval(real_events,pred_events,[act])
            # print(metr)
            # print('.',end='')
            res[act]['avg']=add2Avg(res[act]['avg'] ,metr,len(evalres))
            res[act][fold]=metr

        res['avg']=add2Avg(res['avg'],res[act]['avg'],len(dataset.activities_map))
        # print('.')
        # print(res);
    return res




def add2Avg (oldd,newd,count):
    for item in newd:
        if type(newd[item])==type({}):
            oldd[item]=add2Avg(oldd[item] if item in oldd else {},newd[item],count)
        else:
            if not(item in oldd):oldd[item]=0

            oldd[item]+=np.array(newd[item])/count
    return oldd

if __name__ == "__main__":
            import general.utils as utils
            import metric.Metrics
            import result_analyse.kfold_analyse as an

            files=['200515_13-42-24-VanKasteren']
            titles='a,b,c'
            metric=metric.Metrics.Tatbul()
            run_info={}
            dataset={}
            evalres={}
            res={}
            titles=titles.split(',')
            if(len(titles)!=len(files)):
                print('Titles are not correct. use files names instead')
                titles=files
            print(files)
            for i, file in enumerate(files):
                print(i,file)
                t=titles[i]
                run_info[t],dataset[t],evalres[t]=utils.loadState(file)
    #             print(evalres[t])
#                 for i in evalres[t]:
#                     evalres[t][i]['test'].Sdata=None
                    
                dataset[t].sensor_events=None
                res[t]=an.mergeEvals(dataset[t],evalres[t],metric)
            res={t:res[t] for t in sorted(res.keys())}
            import pandas as pd
            
            actres={}
            for k in dataset[t].activities_map:
                if(k==0):continue
                actres[k]={m:res[m][k]['avg'] for m in res}    
                print('act=',k,'==============================')
                print(actres[k])
                if(len(actres[k])==0):
                    print('No Eval')
                else:
                    df2=pd.DataFrame([actres[k]])
                    print(df2)