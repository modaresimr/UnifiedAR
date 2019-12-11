from general.utils import MyTask

def featureExtraction(windows,feat,train):
    method=feat
    
    if(train):
        method.precompute(windows)
    result=[];
    
    for w in windows:
        result.append(method.featureExtract(w));

    result  =   np.array(result)
    
    return result

class FeatureExtraction(MyTask):
    def precompute(self,windows):
        pass
    def featureExtract(self,window):
        pass
