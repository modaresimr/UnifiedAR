from datatool.dataset_abstract import Dataset


class VanKasteren(Dataset):
    def load(self):
        self.dataset = self.loadVanKasterenDataset()

    def loadVanKasterenDataset(self):
        os.mkdir('dataset')
        sensefile = "dataset/mysensedata.txt"
        actfile = "dataset/myactdata.txt"
        os.remove(sensefile)
        os.remove(actfile)
        print('Beginning downloading files')
        sense_url = 'https://drive.google.com/uc?id=1sESUFhqWKe7T74ETkBobI3im6P2hhZY_&authuser=0&export=download'
        act_url = 'https://drive.google.com/uc?id=13yULlF6uQVUvFHFS4og69VmmSQ4u613y&authuser=0&export=download'
        wget.download(sense_url, sensefile)
        wget.download(act_url, actfile)

        all = pd.read_csv(sensefile, '\t', None, header=0, names=[
            "StartTime", "EndTime", "SID", "value"])

        all.StartTime = pd.to_datetime(
            all.StartTime, format='%d-%b-%Y %H:%M:%S')
        all.EndTime = pd.to_datetime(all.EndTime, format='%d-%b-%Y %H:%M:%S')

        sensor_events = pd.DataFrame(columns=["time", "SID", "value"])
        for i, s in all.iterrows():
            sensor_events = sensor_events.append(
                {'time': s.StartTime, 'SID': s.SID, 'value': s.value}, ignore_index=True)
            sensor_events = sensor_events.append(
                {'time': s.EndTime, 'SID': s.SID, 'value': 0}, ignore_index=True)

        activity_events = pd.read_csv(actfile, '\t', None, header=0, names=[
            "StartTime", "EndTime", "Activity"])
        activity_events.StartTime = pd.to_datetime(
            activity_events.StartTime, format='%d-%b-%Y %H:%M:%S')
        activity_events.EndTime = pd.to_datetime(
            activity_events.EndTime, format='%d-%b-%Y %H:%M:%S')

        activity_events['Duration'] = activity_events.EndTime - \
            activity_events.StartTime
        print('finish downloading files')
        acts = {
            0: 'None',
            1: 'leave house',
            4: 'use toilet',
            5: 'take shower',
            10: 'go to bed',
            13: 'prepare Breakfast',
            15: 'prepare Dinner',
            17: 'get drink'}

        sens = {
            1:	'Microwave',
            5:	'Hall-Toilet door',
            6:	'Hall-Bathroom door',
            7:	'Cups cupboard',
            8:	'Fridge',
            9:	'Plates cupboard',
            12:	'Frontdoor',
            13:	'Dishwasher',
            14:	'ToiletFlush',
            17:	'Freezer',
            18:	'Pans Cupboard',
            20:	'Washingmachine',
            23:	'Groceries Cupboard',
            24:	'Hall-Bedroom door'}

        activities = [k for v, k in enumerate(acts)]
        activities_map_inverse = {k: v for v, k in enumerate(acts)}
        activities_map = {v: k for v, k in enumerate(acts)}

        activity_events_tree = IntervalTree()
        for i, act in activity_events.iterrows():
            activity_events_tree[act.StartTime.value:act.EndTime.value] = act

        # 3
        # sensor_events=sensor_events.drop(columns=['activity_hint'])

        sensor_desc = pd.DataFrame(columns=['ItemId', 'ItemName', 'Cumulative',
                                            'Nominal', 'OnChange', 'ItemRange', 'Location', 'Object', 'SensorName'])
        tmp_sensors = sensor_events['SID'].unique()
        for k, s in enumerate(sens):
            item = {'ItemId': k, 'ItemName': s, 'Cumulative': 0, 'Nominal': 1, 'OnChange': 1, 'ItemRange': {
                'range': ['0', '1']}, 'Location': 'None', 'Object': 'None', 'SensorName': 'None'}
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
    #    sensor_events.value=sensor_events.apply(lambda x:float(x.value) if not(x.SID in sensor_desc_map_inverse) else sensor_desc_map_inverse[x.SID][str(int(x.value))] if type(x.value) is float else sensor_desc_map_inverse[x.SID][x.value],axis=1)
        sensor_id_map = {v: k for v, k in enumerate(sensor_desc.index)}
        sensor_id_map_inverse = {k: v for v, k in enumerate(sensor_desc.index)}

        dataset = Data('dataset'+'VanKasteren')
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
    # loadVanKasterenDataset()
