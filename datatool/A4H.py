from datatool.dataset_abstract import Dataset


class A4H(Dataset):
    def load(self):
        self.dataset = self.loadA4HDataSet()

    def loadA4HDataSet(self):
        os.mkdir('dataset')
        actfile = "dataset/activities.csv"
        sensfile = "dataset/sensor_events.csv"
        descfile = "dataset/sensor_description.csv"
        # if not os.path.isfile(actfile) and os.path.isfile(sensfile):
        os.remove(actfile, sensfile, descfile)

        print('Beginning downloading files')

        activity_url = 'https://drive.google.com/uc?authuser=0&id=1cd_AQbHpK4LBHRyuAWQRP2nG4ilsfNMr&export=download'
        wget.download(activity_url, actfile)

        sensor_events_url = 'https://drive.google.com/uc?authuser=0&id=1n_ARZ90Ebo0VgS40RU-ycd_4tUhDdZs9&export=download'
        wget.download(sensor_events_url, sensfile)

        sensor_description_url = 'https://drive.google.com/uc?authuser=0&id=1QL7bdl8lRbyWdE5uSlMIS9LottgSvDja&export=download'
        wget.download(sensor_description_url, descfile)

        sensor_events = pd.read_csv(sensfile,)
        t = pd.to_datetime(sensor_events['time'], format='%Y-%m-%d %H:%M:%S')
        sensor_events.loc[:, 'time'] = t
        sensor_events = sensor_events.sort_values(['time'])
        sensor_events = sensor_events.reset_index()
        sensor_events = sensor_events.drop(columns=['index'])

        activity_events = pd.read_csv(actfile, index_col='Id')

        activity_events = activity_events.sort_values(['StartTime', 'EndTime'])
        st = pd.to_datetime(
            activity_events['StartTime'], format='%Y-%m-%d %H:%M:%S')
        et = pd.to_datetime(
            activity_events['EndTime'], format='%Y-%m-%d %H:%M:%S')
        activity_events['StartTime'] = st
        activity_events['EndTime'] = et
        # activity_events['Interval']=pd.IntervalIndex.from_arrays(activity_events['StartTime'],activity_events['EndTime'],closed='both')
        activity_events['Duration'] = et-st

        activities = activity_events['Activity'].unique()
        activities = np.insert(activities, 0, 'None')
        activities_map_inverse = {k: v for v, k in enumerate(activities)}
        activities_map = {v: k for v, k in enumerate(activities)}
        activity_events.Activity = activity_events.Activity.apply(
            lambda x: activities_map_inverse[x])

        activity_events_tree = IntervalTree()
        for i, act in activity_events.iterrows():
            activity_events_tree[act.StartTime.value:act.EndTime.value] = act

            #############################

        sensor_desc_map_inverse = {}
        sensor_desc_map = {}

        sensor_desc = pd.read_csv(descfile, index_col='ItemId')
        sensor_desc.ItemRange = sensor_desc.ItemRange.apply(
            lambda x: json.loads(x))

        for i, sd in sensor_desc[sensor_desc.Nominal == 1].iterrows():
            sensor_desc_map_inverse[i] = {k: v for v,
                                          k in enumerate(sd.ItemRange['range'])}
            sensor_desc_map[i] = {v: k for v,
                                  k in enumerate(sd.ItemRange['range'])}
        sensor_events.value = sensor_events.apply(lambda x: float(x.value) if not(x.SID in sensor_desc_map_inverse) else sensor_desc_map_inverse[x.SID][str(
            int(x.value))] if type(x.value) is float else sensor_desc_map_inverse[x.SID][x.value], axis=1)
        sensor_id_map = {v: k for v, k in enumerate(sensor_desc.index)}
        sensor_id_map_inverse = {k: v for v, k in enumerate(sensor_desc.index)}

        dataset = Data('dataset'+'A4H')
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
