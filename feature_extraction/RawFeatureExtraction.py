from feature_extraction.feature_abstract import *
import pandas as pd


class RawFeatureExtraction(FeatureExtraction):
    sec_in_day = (60*60*24)
    sec1 = pd.to_timedelta("1s")

    def applyParams(self, params):
        self.normalized = params.get('normalized', False)
        self.per_sensor = params.get('per_sensor', False)
        self.event_per_window = params.get('event_per_window', 30)
        return super().applyParams(params)

    def precompute():
        self.scount = sum(1 for x in self.datasetdscr.sensor_id_map)
        if self.per_sensor:
            self.len_per_event = 1 + len(self.scount)
        else:
            self.len_per_event = 2

    def featureExtract(self, win):
        window = win['window']

        f = np.ones(self.scount+3)*-1

        for j in range(0, min(self.event_per_window, window.shape[0])):
            sid = self.datasetdscr.sensor_id_map_inverse[window.iat[j, 0]]
            timval = window.iat[j, 1].values/self.sec1.values
            if self.normalized:
                timval = timval/(24*3600)
            f[j*self.len_per_event] = timval

            if self.per_sensor:
                f[j*self.len_per_event+sid+1] = 1
            else:
                f[j*self.len_per_event+1] = sid

        return f
