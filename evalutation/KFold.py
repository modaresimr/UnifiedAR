from evalutation.evalution_abstract import *

class KFold(Evalutation):
    def precompute(self,dataset):
        pass
    def evaluate(self):
        pass


    def makeFoldTrainTest(sensor_events,activity_events,fold):
        sdate=sensor_events.time.apply(lambda x:x.date())
        adate=activity_events.StartTime.apply(lambda x:x.date())
        days=adate.unique()
        kf = KFold(n_splits=fold)
        kf.get_n_splits(days)

        for j,(train_index, test_index) in enumerate(kf.split(days)):
            Train0=Data('train_fold_'+str(j))
            Train0.s_events=sensor_events.loc[sdate.isin(days[train_index])]
            Train0.a_events=activity_events.loc[adate.isin(days[train_index])]
            Test0=Data('test_fold_'+str(j))
            Test0.s_events=sensor_events.loc[sdate.isin(days[test_index])]
            Test0.a_events=activity_events.loc[adate.isin(days[test_index])]
            yield Train0,Test0
