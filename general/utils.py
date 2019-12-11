
#Define a Data Object
class Data:
    def __init__(self, name):
        self.name=name
    def __str__(self):
        return '<'+self.name+'> '+str(self.__dict__);

	
# Arg Max in a Dic
def argmaxdic(dic):
    mx={'v':0,'i':0}
    for d in dic:
        tmp=dic[d]
        if(mx['v']<tmp):
            mx['v']=tmp
            mx['i']=d
    return mx['i']
	
	
class MyTask:
    def applyParams(self,params):
        self.params=params
        return True
    def reset(self):
        pass
    def __str__(self):
        return '<'+self.__class__.__name__+'> '+str(self.__dict__);

	#Defining Interval Tree from Activities.
def makeIntervalTree(acts):
  tree=IntervalTree()

  for act in acts:
    start=act['StartTime'].value;
    end=act['EndTime'].value;
    if(start==end):
      start=start-1
    tree[start:end]=act  
  return tree

def makeNonOverlapIntervalTree(acts):
    tree=makeIntervalTree(acts)
    tree.split_overlaps()
    tree.merge_equals(data_reducer=lambda x,y:y)
    return tree

# Find overlap between 2 event in Minutes
def findOverlap(a,b):
    return ((min(a['EndTime'],b['EndTime'])-max(a['StartTime'],b['StartTime'])).value)/pd.to_timedelta('60s').value



# Buffer data type for stacking stream
class Buffer:
  def __init__(self, input, minsize,maxsize):
    self.data=input
    self.times=input.time.tolist()
    self.minsize =  minsize
    self.maxsize = maxsize
    self.start_index=0

  def removeTop(self, idx):
    self.start_index=idx
        
  def getEventsInRange(self,starttime,endtime):
    sindex=self.searchTime(starttime,-1)    
    eindex=self.searchTime(endtime,+1)    
    if(sindex is None):
      return None
    if(eindex is None):
      return None
    return self.data.iloc[sindex:eindex+1];
        
  def searchTime(self, time, operator=0):
    times=self.times;
    n=len(times);
    L = self.start_index
    R = n
    
    if operator ==1 :
      while L < R:
          m = int((L + R) / 2)

          if times[m] <= time:
              L = m + 1 
          else:
              R = m
      return L-1 if L>self.start_index else None
    else :
        while L < R:
          m = int((L + R) / 2)

          if times[m] < time:
              L = m + 1 
          else:
              R = m
        return L if L<n else None
	
print('Utils loaded successfully!!')

def mytest():
	print('fffff');