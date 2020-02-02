from feature_extraction.feature_abstract import *
import pandas as pd


class RawFeatureExtraction(FeatureExtraction):
    sec_in_day = (60*60*24)
    sec1 = pd.to_timedelta("1s")

    def applyParams(self, params):
        self.normalized = params.get('normalized', False)
        self.per_sensor = params.get('per_sensor', False)
        return super().applyParams(params)

    def precompute(self, datasetdscr, windows):
        self.datasetdscr=datasetdscr
        self.scount = sum(1 for x in datasetdscr.sensor_id_map)
        self.max_windowsize=max([len(w) for w in windows])

        if self.per_sensor:
            self.len_per_event = 1 + len(self.scount)
        else:
            self.len_per_event = 2

    def featureExtract(self, win):
        window = win['window']

        f = np.ones(self.scount+3)*0 

        for j in range(0, min(self.max_windowsize, window.shape[0])):
            sid = self.datasetdscr.sensor_id_map_inverse[window.iat[j, 0]]
            timval = window.iat[j, 1]
            timval=timval.hour*60*60+timval.minute*60+timval.second
            if self.normalized:
                timval = timval/(24*3600)
            f[j*self.len_per_event] = timval

            if self.per_sensor:
                f[j*self.len_per_event+sid+1] = 1
            else:
                f[j*self.len_per_event+1] = sid

        return f
