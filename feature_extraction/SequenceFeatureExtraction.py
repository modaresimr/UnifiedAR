from feature_extraction.feature_abstract import *
class SequenceFeatureExtraction(FeatureExtraction):
    def featureExtract(self,win):
        window=win['window']
        f=[]
        for i in range(0,window.shape[0]):
            f.append(sensor_id_map_inverse[window.iat[i,0]])
        return f