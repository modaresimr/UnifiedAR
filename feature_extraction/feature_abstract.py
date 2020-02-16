from general.utils import MyTask
import numpy as np
from general.sparray import sparray
import tempfile

def featureExtraction(feat, datasetdscr, Sdata, istrain):

    if(istrain):
        feat.precompute(datasetdscr, Sdata.set_window)

    shape = feat.getShape()
    
    filename=tempfile.mktemp('featureExtract') 
    if(len(shape)==1):
        result= np.memmap(filename,shape=(len(Sdata.set_window),shape[0]),mode='w+',dtype=np.float)
    else:
        result= np.memmap(filename,shape=(len(Sdata.set_window),shape[0],shape[1]),mode='w+', dtype=np.float)
        # result= np.zeros((len(windows),shape[0],shape[1]), dtype=np.float)
        #result=np.zeros((len(windows),fw.shape[0],fw.shape[1]))
    
    for i in range(len(Sdata.set_window)):
        result[i]=feat.featureExtract2(Sdata.s_event_list,Sdata.set_window[i])

    return result


def featureExtraction2(feat, datasetdscr, Sdata, istrain):
    if(istrain):
        feat.precompute(datasetdscr, Sdata.set_window)
    
    for i in range(len(Sdata.set_window)):
        yield (feat.featureExtract2(Sdata.s_event_list,Sdata.set_window[i]),Sdata.label[i])
    return 1
    

class FeatureExtraction(MyTask):
    def getShape(self):
        return self.shape
    def precompute(self, datasetdscr, windows):
        self.datasetdscr=datasetdscr
        pass
    def featureExtract(self, window):
        pass
