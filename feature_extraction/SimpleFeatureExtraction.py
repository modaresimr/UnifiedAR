from feature_extraction.feature_abstract import *
class SimpleFeatureExtraction(FeatureExtraction):
    def featureExtract(self,win):
        window=win['window']
        f=np.zeros(sum(1 for x in sensor_id_map))  
        for i in range(0,window.shape[0]):
            f[sensor_id_map_inverse[window.iat[i,0]]]=1   #f[sensor_id_map_inverse[x.SID]]=1
        return f
