from ml_strategy.ml_strategy_abstract import *

class SeperateGroupStrategy(MLStrategy):
    def groupize(self,datasetdscr):
        gacts=[[a] for a in datasetdscr.activities_map]
        gacts.append([a for a in datasetdscr.activities_map])
        return gacts

    def train(self,datasetdscr,data,func):
        

        gacts=self.groupize(datasetdscr)
        for indx,acts in enumerate(gacts):
            Tdata=self.justifySet(acts,Tdata)
            acts_name=datasetdscr.activities[acts]

            



    def test(self,datasetdscr,data,func):

        gacts=self.groupize(datasetdscr)
        for indx,acts in enumerate(gacts):
            Tdata=self.justifySet(acts,Tdata)
            acts_name=datasetdscr.activities[acts]
