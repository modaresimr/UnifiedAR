from evaluation.evaluation_abstract import *


class Simple(Evaluation):
    def precompute(self):
        pass

    def evaluate(self, dataset, func):
        Train, Test = self.makeTrainTest(
            dataset.sensor_events, dataset.activity_events)
        return func(dataset, Train, Test)

    def makeTrainTest(self, sensor_events, activity_events):
        dataset_split = min(activity_events.StartTime) + \
            ((max(activity_events.EndTime)-min(activity_events.StartTime))*4/5)
        dataset_split = pd.to_datetime(dataset_split.date())  # day
        Train = Data('train')
        Test = Data('test')
        Train.s_events = sensor_events[sensor_events.time < dataset_split]
        Train.a_events = activity_events[activity_events.EndTime < dataset_split]

        Test.s_events = sensor_events[sensor_events.time >= dataset_split]
        Test.a_events = activity_events[activity_events.EndTime >= dataset_split]

        return [Train], [Test]
