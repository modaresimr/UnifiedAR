
def convertAndMergeToEvent(set_window,predictedclasses):
    events=[]
    ptree={}
    for i in range(0,len(set_window)):
        start=set_window[i]['start'];
        end=set_window[i]['end'];
        pclass=predictedclasses[i]

        if not(pclass in ptree):
            ptree[pclass]=IntervalTree()
        ptree[pclass][start:end]={'Activity':pclass, 'StartTime':start, 'EndTime':end}

    tree=IntervalTree()
    def datamerger(x,y):
        start=min(x['StartTime'],y['StartTime'])
        end=max(x['EndTime'],y['EndTime'])
        return {'Activity':x['Activity'], 'StartTime':start, 'EndTime':end}
        
    for a in ptree:
        ptree[a].merge_overlaps(data_reducer=datamerger)
        tree|=ptree[a]
    
    tree.split_overlaps()
    def data_reducer(x,y):
        res=x
        if(x['EndTime']>y['EndTime']):
            res=y
        return res
    
    tree.merge_equals(data_reducer=data_reducer)
    for inv in tree:
        events.append({'Activity':inv.data['Activity'], 'StartTime':inv.begin, 'EndTime':inv.end});
    
    events= pd.DataFrame(events)
    events=events.sort_values(['StartTime'])
    events=events.reset_index()
    events=events.drop(['index'],axis=1)
    return events

# sw,label=fullevals.iloc[0]['model']['func'].Test.set_window,fullevals.iloc[0]['testlabel']
# pev=convertAndMergeToEvent(sw,label)

# sw=np.array(sw)

# print([p['start'] for p in sw[label==7]])
# pev.loc[pev.Activity==7]