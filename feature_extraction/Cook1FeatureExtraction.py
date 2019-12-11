from feature_extraction.feature_abstract import *

class Cook1FeatureExtraction(FeatureExtraction):
    sec_in_day=(60*60*24)
    def featureExtract(self,win):
        window=win['window']
        scount=sum(1 for x in sensor_id_map);
        f=np.ones(scount+3)*-1
        for i in range(0,window.shape[0]):
            f[sensor_id_map_inverse[window.iat[i,0]]]=window.iat[i,2]   #f[sensor_id_map_inverse[x.SID]]=1
        stime=window.iat[0,1]#startdatetime
        etime=window.iat[-1,1]#enddatetime
        ts=(stime-pd.to_datetime(stime.date())).total_seconds()
        f[scount+0]=ts/self.sec_in_day
        f[scount+1]=(etime-stime).total_seconds()/self.sec_in_day
        f[scount+2]=len(window)
        return f        