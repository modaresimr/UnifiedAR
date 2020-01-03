
import numpy as np
from general.utils import Data

def CMbasedMetric(cm,average=None):
    TP,FP,FN,TN=get_tp_fp_fn_tn(cm)
    
    accuracy = TP.sum()/cm.sum()
    precision= TP/(TP+FP)
    recall= TP/(TP+FN)
    f1=2*recall*precision/(recall+precision)

    result=Data('CMMetric')

    result.accuracy=accuracy
    if(average is None):   
        result.precision=precision
        result.recall=recall
        result.f1=f1
        return result

    result.precision=np.average(precision[~np.isnan(precision)])
    result.recall=np.average(recall[~np.isnan(recall)])
    result.f1=np.average(f1[~np.isnan(f1)])

    return result



def get_tp_fp_fn_tn(cm):
    cm=np.array(cm)
    np.seterr(divide='ignore', invalid='ignore')
    TP = np.diag(cm)
    FP = np.sum(cm, axis=0) - TP
    FN = np.sum(cm, axis=1).T - TP
    num_classes = len(cm)
    TN = []
    for i in range(num_classes):
        temp = np.delete(cm, i, 0)    # delete ith row
        temp = np.delete(temp, i, 1)  # delete ith column
        TN.append(temp.sum())
    return TP,FP,FN,TN
