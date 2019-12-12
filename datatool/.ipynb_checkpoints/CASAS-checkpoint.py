from datatool.dataset_abstract import Dataset


class AbstractCASAS(Dataset):
    def load(self):
        pass

    def loadCASASDataset(self, data_url):
        os.mkdir('datasetfiles')
        datafile = "datasetfiles/data.txt"
        os.remove(datafile)
        print('Beginning downloading files')

        wget.download(data_url, datafile)

        all = pd.read_csv(datafile, r"\s+", None, header=None,
                          names=["date", "time", "SID", "value", "activity", "hint"])
        all.time = pd.to_datetime(all.date+" " + all.time,
                                  format='%Y-%m-%d %H:%M:%S')
        all = all.drop(columns=['date'])

        sensor_events = all

        print('finish downloading files')

        activity_events = pd.DataFrame(
            columns=["StartTime", "EndTime", "Activity", 'Duration'])
        start = {}
        for i, e in sensor_events[sensor_events.hint == sensor_events.hint].iterrows():

            if(e.hint == 'begin'):
                start[e.activity] = e

            elif(e.hint == 'end'):
                actevent = {"StartTime": start[e.activity].time,	"EndTime": e.time,
                            "Activity": e.activity, 'Duration': e.time-start[e.activity].time}
                # actevent=[start[splt[0]].time,e.time,splt[0]]
                # start[splt[0]]=None
                activity_events = activity_events.append(
                    actevent, ignore_index=True)
                start[e.activity] = None

        activities = activity_events['Activity'].unique()
        activities.sort()
        activities = np.insert(activities, 0, 'None')
        activities_map_inverse = {k: v for v, k in enumerate(activities)}
        activities_map = {v: k for v, k in enumerate(activities)}
        activity_events.Activity = activity_events.Activity.apply(
            lambda x: activities_map_inverse[x])

        activity_events_tree = IntervalTree()
        for i, act in activity_events.iterrows():
            activity_events_tree[act.StartTime.value:act.EndTime.value] = act

        # 3
        # sensor_events=sensor_events.drop(columns=['activity_hint'])

        sensor_events = sensor_events.drop(columns=['activity', 'hint'])
        sensor_events = sensor_events[["SID", "time", "value"]]
        sensor_desc = pd.DataFrame(columns=['ItemId', 'ItemName', 'Cumulative',
                                            'Nominal', 'OnChange', 'ItemRange', 'Location', 'Object', 'SensorName'])
        tmp_sensors = sensor_events['SID'].unique()
        for s in tmp_sensors:
            item = {'ItemId': s, 'ItemName': s, 'Cumulative': 0, 'Nominal': 1, 'OnChange': 1, 'ItemRange': {
                'range': ['OFF', 'ON']}, 'Location': 'None', 'Object': 'None', 'SensorName': 'None'}
            if(s[0] == 'I'):
                item['ItemRange'] = {'range': ['ABSENT', 'PRESENT']}
            if(s[0] == 'D'):
                item['ItemRange'] = {'range': ['CLOSE', 'OPEN']}
            if(s[0] == 'E'):
                item['ItemRange'] = {
                    'range': ['STOP_INSTRUCT', 'START_INSTRUCT']}
            if(s == 'asterisk'):
                item['ItemRange'] = {'range': ['END', 'START']}
            if(s.startswith('AD1')):
                item['Nominal'] = 0
                item['ItemRange'] = {"max": 3.0, "min": 0.0}
            sensor_desc = sensor_desc.append(item, ignore_index=True)

        sensor_desc = sensor_desc.sort_values(by=['ItemName'])
        sensor_desc = sensor_desc.set_index('ItemId')

        sensor_desc_map_inverse = {}
        sensor_desc_map = {}
        #sensor_desc.ItemRange=sensor_desc.ItemRange.apply(lambda x: json.loads(x))
        for i, sd in sensor_desc[sensor_desc.Nominal == 1].iterrows():
            sensor_desc_map_inverse[i] = {k: v for v,
                                          k in enumerate(sd.ItemRange['range'])}
            sensor_desc_map[i] = {v: k for v,
                                  k in enumerate(sd.ItemRange['range'])}
        sensor_events.value = sensor_events.apply(lambda x: float(x.value) if not(x.SID in sensor_desc_map_inverse) else sensor_desc_map_inverse[x.SID][str(
            int(x.value))] if type(x.value) is float else sensor_desc_map_inverse[x.SID][x.value], axis=1)
        sensor_id_map = {v: k for v, k in enumerate(sensor_desc.index)}
        sensor_id_map_inverse = {k: v for v, k in enumerate(sensor_desc.index)}

        dataset = Data('dataset'+'CASAS')
        dataset.activity_events = activity_events
        dataset.sensor_events = sensor_events
        dataset.activities = activities
        dataset.activities_map_inverse = activities_map_inverse
        dataset.activities_map = activities_map
        dataset.activity_events_tree = activity_events_tree
        dataset.sensor_desc = sensor_desc
        dataset.sensor_desc_map = sensor_desc_map
        dataset.sensor_desc_map_inverse = sensor_desc_map_inverse
        dataset.sensor_id_map = sensor_id_map
        dataset.sensor_id_map_inverse = sensor_id_map_inverse
        return dataset


class KaryoAdlNormal(AbstractCASAS):
    def load(self):
        self.dataset = self.loadCASASDataset(
            'https://drive.google.com/uc?id=1WY26Tmv9kBvdto4gy_YKnvc8KeknKB_i&authuser=0&export=download')


class Home1(AbstractCASAS):
    def load(self):
        self.dataset = self.loadCASASDataset(
            'https://drive.google.com/uc?id=1RqhKY_kVKTCc1L5iXfQl2yKQVWgoXwok&authuser=0&export=download')


class Home2(AbstractCASAS):
    def load(self):
        self.dataset = self.loadCASASDataset(
            'https://drive.google.com/uc?id=1mBXdg9-jdOmGVMdP0SVmGu0gWfBSSd41&authuser=0&export=download')
