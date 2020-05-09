from combiner.combiner_abstract import Combiner
from intervaltree.intervaltree import IntervalTree
import pandas as pd
import numpy as np
import logging
logger = logging.getLogger(__file__)

# print([p['start'] for p in sw[label==7]])
# pev.loc[pev.Activity==7]


class EmptyCombiner(Combiner):
    def combine(self, s_event_list,set_window, act_data):
        predicted   = np.argmax(act_data, axis=1) 
        events      = []
        ptree       = {}
        epsilon=pd.to_timedelta('1s')
        old=None
        for i in range(0, len(set_window)):
            idx     = set_window[i]
            start   = s_event_list[idx[0],1]
            end     = s_event_list[idx[-1],1]
            #pclass = np.argmax(predicted[i])
            pclass  = predicted[i]
            if not(old is None):
                old['EndTime']      =   min(old['EndTime'],start)
                if old['StartTime'] >=  old['EndTime']:
                    events.pop()
            old={'Activity': pclass, 'StartTime': start, 'EndTime': end}
            events.append(old)


        events = pd.DataFrame(events)
        events = events.sort_values(['StartTime'])
        events = events.reset_index()
        events = events.drop(['index'], axis=1)
        return events

