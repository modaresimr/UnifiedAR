from segmentation.segmentation_abstract import Segmentation

class FixedEventWindow(Segmentation):
    def precompute(self,s_events,a_events,acts):
        pass
        
    def segment(self,w_history,buffer):
        params=self.params
        shift=params['shift']
        size=params['size']
        
        if len(w_history)==0 :
          lastStart=pd.to_datetime(0) 
        else :
          lastStart=w_history[len(w_history)-1]['start']

        
        sindex=buffer.searchTime(lastStart,-1)

        if(sindex is None):
            return None
        sindex=sindex+shift
        if(len(buffer.times)<=sindex):
            return None
        
        
        eindex=min(len(buffer.times)-1,sindex+size)
        if(eindex-sindex<size):
            return None
        etime=buffer.times[eindex]
        stime=buffer.times[sindex]
        window=buffer.data.iloc[sindex:eindex+1];
        buffer.removeTop(sindex)
        window.iat[0,1].value
        return {'window':window,'start':stime, 'end':etime}
    
    def applyParams(self,params):
        shift=params['shift']
        size=params['size']
        if(shift>size):
            return False;
        return super().applyParams(params);