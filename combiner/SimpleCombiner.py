from combiner.combiner_abstract import Combiner
from intervaltree.intervaltree import IntervalTree
import pandas as pd
import numpy as np
import logging
logger = logging.getLogger(__file__)

# print([p['start'] for p in sw[label==7]])
# pev.loc[pev.Activity==7]


class SimpleCombiner(Combiner):
    def combine2(self, times, act_data):
        predicted   = np.argmax(act_data, axis=1) 
        events      = []
        ptree       = {}
        epsilon=pd.to_timedelta('1s')
        
        for i in range(len(times)):   
            start   = times[i][0]
            end     = times[i][1]
            #pclass = np.argmax(predicted[i])
            pclass  = predicted[i]

            if not(pclass in ptree):
                ptree[pclass] = IntervalTree()
            ptree[pclass][start:end+epsilon] = {
                'Activity': pclass, 'StartTime': start, 'EndTime': end
            }
            if(i>0 and pclass>0 and predicted[i-1]==predicted[i] and False):
                #fix gap
                start   = times[i-1][1]
                end     = times[i][0]
                if(end>start):
                #pclass = np.argmax(predicted[i])
                    ptree[pclass][start:end] = {
                        'Activity': pclass, 'StartTime': start, 'EndTime': end
                    }                   

        tree = IntervalTree()

        def datamerger(x, y):
            start = min(x['StartTime'], y['StartTime'])
            end = max(x['EndTime'], y['EndTime'])
            return {'Activity': x['Activity'], 'StartTime': start, 'EndTime': end}

        for a in ptree:
            ptree[a].merge_overlaps(data_reducer=datamerger)
            tree |= ptree[a]

        tree.split_overlaps()

        def data_reducer(x, y):
            if(x['EndTime'] > y['EndTime']):
                return y
            return x

        tree.merge_equals(data_reducer=data_reducer)
        for inv in tree:
            events.append({'Activity': inv.data['Activity'], 'StartTime': inv.begin, 'EndTime': inv.end})

        events = pd.DataFrame(events)
        events = events.sort_values(['StartTime'])
        events = events.reset_index()
        events = events.drop(['index'], axis=1)
        return events

    # sw,label=fullevals.iloc[0]['model']['func'].Test.set_window,fullevals.iloc[0]['testlabel']
    # pev=convertAndMergeToEvent(sw,label)

    # sw=np.array(sw)



class EmptyCombiner(Combiner):



    def combine2(self, times, act_data):
        predicted   = np.argmax(act_data, axis=1) 
        events      = []
        ptree       = {}
        epsilon     = pd.to_timedelta('1s')
        
        for i in range(len(times)):
            
            start   = times[i]['begin']
            end     = times[i]['end']
            #pclass = np.argmax(predicted[i])
            pclass  = predicted[i]
            if(pclass==0):
                continue
            if len(events)>0:
                events[-1]['EndTime']      =   min(events[-1]['EndTime'],start)
                if events[-1]['StartTime'] >=  events[-1]['EndTime']:
                    events.pop()
            newe={'Activity': pclass, 'StartTime': start, 'EndTime': end}
            # if(len(events)>0 and events[-1]['Activity']==newe['Activity'] and events[-1]['EndTime']<newe['StartTime']):
            #     events.append({'Activity': pclass, 'StartTime': events[-1]['EndTime'], 'EndTime': newe['StartTime']})
            events.append(newe)
            

        events = pd.DataFrame(events)
        if(len(events)>0):
            events = events.sort_values(['StartTime'])
        events = events.reset_index()
        events = events.drop(['index'], axis=1)
        return events

