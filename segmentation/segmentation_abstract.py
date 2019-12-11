from general.utils import MyTask



# Define segmentation 
def segment(s_events,segment_method): 
    buffer=Buffer(s_events,0,0)  
    w_history=[]; 
    segment_method.reset()
    while(1):
      window=segment_method.segment(w_history,buffer)
      if window is None:
        return
      w_history.append(window)  
      yield window
	
	
class Segmentation(MyTask):
    def precompute(self,s_events,a_events,acts):
        pass
    def segment(self,w_history,buffer):
        pass

