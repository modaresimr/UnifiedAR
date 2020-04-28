import ml_strategy.abstract
import ml_strategy.Simple
import result_analyse.visualisation as vs
import logging
import numpy as np
logger = logging.getLogger(__file__)

class SeperateGroupStrategy(ml_strategy.abstract.MLStrategy):
    def groupize(self,datasetdscr,acts):
        #gacts=[[a] for a in datasetdscr.activities_map]
        #gacts.append([a for a in datasetdscr.activities_map])
        gacts=[[a] for a in acts]
        gacts.append([a for a in acts])
        return gacts

    def train(self,datasetdscr,data,acts):        
        self.gacts=self.groupize(datasetdscr,acts)
        self.strategies ={}
        self.acts_name  ={}
        train_results   ={}
        

        # intree = IntervalTree()
        for indx,tacts in enumerate(self.gacts[1:]):
            logger.info("\n=======================working on activties "+tacts.__str__()+"=========")
            Tdata=self.justifySet(tacts,data,False)
            self.acts_name[indx]=datasetdscr.activities[tacts]
            self.strategies[indx]=ml_strategy.Simple.SimpleStrategy()
            self.strategies[indx].train(datasetdscr,Tdata,tacts)
            if('result' in self.strategies[indx].bestOpt.result):
                result=self.strategies[indx].bestOpt.result['result']
            else:
                result=self.strategies[indx].test(Tdata)
            train_results[indx]=result
            
            

            actnames=self.acts_name[indx]
            
            # vs.plotJoinAct2(res.real_events,res.pred_events,tacts[1:],actnames[1:])
            
            for i in range(0, len(result.Sdata.set_window)):
                idx     = result.Sdata.set_window[i]
                start   = result.Sdata.s_event_list[idx[0],1]
                end     = result.Sdata.s_event_list[idx[-1],1]
                rcls    = tacts[result.Sdata.label[i]]
                pcls    = tacts[result.predicted_classes[i]]

                prob    = result.predicted[i]
                fullprob=np.zeros(len(acts))
                for a in range(len(tacts)):
                    fullprob[tacts[a]]=prob[a]
                
                intree[start:end]={real:rcls,pred:pcls,pred_prob:fullprob}

        savedata=Data(tacts.__str__())
        savedata.intree=intree
        savedata.train_results=train_results
        savedata.acts_name=self.acts_name
        savedata.gacts=self.gacts[1:]

        intree.split_overlaps()
     
        utils.saveState(savedata,'intervaltree')
        from collections import defaultdict
        segments = defaultdict(list)
        for item in intree.items():
            # segments[item.begin<<32|item.end].append(item.data)
            segments[str(item.begin)+'-'+str(item.end)].append(item.data)



    

    def test(self,data):
        gacts=self.groupize(datasetdscr,acts)
        test_results={}
        for indx,tacts in enumerate(gacts):
            Tdata=self.justifySet(tacts,Tdata)
            #self.acts_name[indx]
            test_results[indx]=self.strategies[indx].test(Tdata)
            res=test_results[indx]
            actnames=self.acts_name[indx]
            
            vs.plotJoinAct2(res.real_acts,res.pred_acts,tacts,actnames)
            

            