
import numpy as np
import pandas as pd
from intervaltree.intervaltree import IntervalTree
from general.utils import Data

def event_confusion_matrix(r_activities,p_activities,labels):
    cm=np.zeros((len(labels),len(labels)))
    # begin=real0.StartTime.min()
    # end=real0.EndTime.max()
    
    #   predicted.append({'StartTime':begin,'EndTime':end,'Activity':0})
    #   real.append({'StartTime':begin,'EndTime':end,'Activity':0})
    events=merge_split_overlap_IntervalTree(p_activities,r_activities)
    #predictedtree=makeIntervalTree(labels)

    
    for eobj in events:
        e=eobj.data
        pact=e.P.Activity if not(e.P is None) else 0
        ract=e.R.Activity if not(e.R is None) else 0
        cm[ract][pact]+=max((eobj.end-eobj.begin)/pd.to_timedelta('60s').value,0.01)
            
    #for p in predicted:
    #  for q in realtree[p['StartTime'].value:p['EndTime'].value]:
    #      timeconfusion_matrix[p['Activity']][q.data['Activity']]+=findOverlap(p,q.data);
            
    return cm







def column_index(df, query_cols):
    cols = df.columns.values
    sidx = np.argsort(cols)
    return sidx[np.searchsorted(cols,query_cols,sorter=sidx)]

def merge_split_overlap_IntervalTree(p_acts,r_acts):
    tree=IntervalTree()

    PACT=column_index(p_acts,'Activity')
    PSTIME=column_index(p_acts,'StartTime')
    PETIME=column_index(p_acts,'EndTime')
    
    for row in p_acts.values:
        if(row[PACT]==0):
            continue
        start=row[PSTIME]
        end=row[PETIME]
        startv=start.value
        endv=end.value
        if(startv==endv):
            startv=startv-1
        #tree[start:end]={'P':{'Activitiy':act.Activity,'Type':'P','Data':act}]
        d=Data('P-act')
        d.P={'Activity':row[PACT],'StartTime':start,'EndTime':end}
        d.R=None
        tree[startv:endv]=d


    RACT=column_index(r_acts,'Activity')
    RSTIME=column_index(r_acts,'StartTime')
    RETIME=column_index(r_acts,'EndTime')

    for row in r_acts.values:
        if(row[RACT]==0):
            continue
        start=row[RSTIME]
        end=row[RETIME]
        startv=start.value
        endv=end.value
        if(startv==endv):
            startv=startv-1
        #tree[start:end]=[{'Activitiy':act.Activity,'Type':'R','Data':act}]
        d=Data('P-act')
        d.P=None
        d.R={'Activity':row[RACT],'StartTime':start,'EndTime':end}
        tree[startv:endv]=d

    tree.split_overlaps()
    def data_reducer(x,y):
        res=x
        if not(y.P is None):
            if (res.P is None) or y.P[PETIME]<res.P[PETIME]:
                res.P=y.P
        if not(y.R is None):
            if (res.R is None) or y.R[RETIME]<res.R[RETIME]:
                res.R=y.R
        return res
    
    tree.merge_equals(data_reducer=data_reducer)
            
    return tree