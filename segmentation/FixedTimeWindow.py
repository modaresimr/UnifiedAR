from segmentation.segmentation_abstract import Segmentation
class FixedTimeWindow(Segmentation):
    def precompute(self,s_events,a_events,acts):
        pass
        
    def segment(self,w_history,buffer):
        params=self.params
        shift=pd.Timedelta(params['shift'],unit='s')
        size=pd.Timedelta(params['size'],unit='s')
        
        if len(w_history)==0 :
          lastStart=pd.to_datetime(0) 
        else :
          lastStart=w_history[len(w_history)-1]['start']

        lastStartshift=lastStart+shift;
        sindex=buffer.searchTime(lastStartshift,-1)

        if(sindex is None):
            return None
        #try:
        stime=lastStart+shift

        eindex=buffer.searchTime(stime+size,+1)
        if(eindex is None):
            eindex=sindex
        etime=buffer.times[eindex]

        window=buffer.data.iloc[sindex:eindex+1];
        buffer.removeTop(sindex)
        window.iat[0,1].value
        return {'window':window,'start':stime, 'end':etime}
    
    def applyParams(self,params):
        shift=pd.Timedelta(params['shift'],unit='s')
        size=pd.Timedelta(params['size'],unit='s')
        if(shift>size):
            return False;
        return super().applyParams(params);