from general.utils import MyTask
import numpy as np

def featureExtraction(feat,datasetdscr,windows,istrain):
    method=feat
    
    if(istrain):
        method.precompute(datasetdscr,windows)
    result=[]
    
    for w in windows:
        result.append(method.featureExtract(w))

    result  =   np.array(result)
    
    return result

class FeatureExtraction(MyTask):
    def precompute(self,datasetdscr,windows):
        self.datasetdscr=datasetdscr
        pass
    def featureExtract(self,window):
        pass
