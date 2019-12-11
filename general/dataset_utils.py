def loadKaryoAdlNormalDataset():
    loadCASASDataset('https://drive.google.com/uc?id=1WY26Tmv9kBvdto4gy_YKnvc8KeknKB_i&authuser=0&export=download');

def loadHome1Dataset():
    loadCASASDataset('https://drive.google.com/uc?id=1RqhKY_kVKTCc1L5iXfQl2yKQVWgoXwok&authuser=0&export=download');

def loadHome2Dataset():
    loadCASASDataset('https://drive.google.com/uc?id=1mBXdg9-jdOmGVMdP0SVmGu0gWfBSSd41&authuser=0&export=download');

	
def loadCASASDataset(data_url):
    os.mkdir('dataset')
    datafile="dataset/data.txt"
    os.remove(datafile)
    print('Beginning downloading files')
    
    wget.download(data_url, datafile)  
    global sensor_events
    all=pd.read_csv(datafile,r"\s+",None,header=None,names=["date","time","SID","value","activity","hint"]);
    
    all.time=pd.to_datetime(all.date+" "+ all.time,format='%Y-%m-%d %H:%M:%S')
    all=all.drop(columns=['date'])
    
    
    sensor_events=all
    
    print('finish downloading files')
    global activity_events
    activity_events=pd.DataFrame(columns=["StartTime","EndTime","Activity",'Duration'])
    start={}
    for i,e in sensor_events[sensor_events.hint==sensor_events.hint].iterrows():
        
        if(e.hint=='begin'):
            start[e.activity]=e
            
        elif(e.hint=='end'):
            actevent={"StartTime":start[e.activity].time,	"EndTime":e.time,	"Activity":e.activity,'Duration':e.time-start[e.activity].time}
            #actevent=[start[splt[0]].time,e.time,splt[0]]
            # start[splt[0]]=None
            activity_events=activity_events.append(actevent,ignore_index=True)
            start[e.activity]=None
        
    global activities
    global activities_map_inverse
    global activities_map

    activities=activity_events['Activity'].unique()
    activities.sort()
    activities=np.insert(activities,0,'None')
    activities_map_inverse={k: v for v, k in enumerate(activities)}
    activities_map={v: k for v, k in enumerate(activities)}
    activity_events.Activity=activity_events.Activity.apply(lambda x:activities_map_inverse[x])
    global activity_events_tree
    activity_events_tree=IntervalTree()
    for i,act in activity_events.iterrows():
        activity_events_tree[act.StartTime.value:act.EndTime.value]=act  

    ############################################3
    #sensor_events=sensor_events.drop(columns=['activity_hint'])
    global sensor_desc
    global sensor_desc_map
    global sensor_desc_map_inverse
    global sensor_id_map
    global sensor_id_map_inverse
    sensor_events=sensor_events.drop(columns=['activity','hint']);
    sensor_events=sensor_events[["SID","time","value"]]
    sensor_desc=pd.DataFrame(columns=['ItemId','ItemName','Cumulative','Nominal','OnChange','ItemRange','Location','Object','SensorName'])
    tmp_sensors=sensor_events['SID'].unique()
    for s in tmp_sensors:
        item={'ItemId':s,'ItemName':s,'Cumulative':0,'Nominal':1,'OnChange':1,'ItemRange':{'range':['OFF','ON']},'Location':'None','Object':'None','SensorName':'None'}
        if(s[0]=='I'):
            item['ItemRange']={'range':['ABSENT','PRESENT']}
        if(s[0]=='D'):
            item['ItemRange']={'range':['CLOSE','OPEN']}
        if(s[0]=='E'):
            item['ItemRange']={'range':['STOP_INSTRUCT','START_INSTRUCT']}
        if(s=='asterisk'):
            item['ItemRange']={'range':['END','START']}
        if(s.startswith('AD1')):
            item['Nominal']=0
            item['ItemRange']={"max":3.0,"min":0.0}
        sensor_desc=sensor_desc.append(item,ignore_index=True)

    sensor_desc=sensor_desc.sort_values(by=['ItemName'])
    sensor_desc=sensor_desc.set_index('ItemId')

    sensor_desc_map_inverse={}
    sensor_desc_map={}
    #sensor_desc.ItemRange=sensor_desc.ItemRange.apply(lambda x: json.loads(x))
    for i,sd in sensor_desc[sensor_desc.Nominal==1].iterrows():
        sensor_desc_map_inverse[i]={k: v for v, k in enumerate(sd.ItemRange['range'])} 
        sensor_desc_map[i]={v: k for v, k in enumerate(sd.ItemRange['range'])} 
    sensor_events.value=sensor_events.apply(lambda x:float(x.value) if not(x.SID in sensor_desc_map_inverse) else sensor_desc_map_inverse[x.SID][str(int(x.value))] if type(x.value) is float else sensor_desc_map_inverse[x.SID][x.value],axis=1)
    sensor_id_map={v: k for v, k in enumerate(sensor_desc.index)} 
    sensor_id_map_inverse={k: v for v, k in enumerate(sensor_desc.index)} 
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
def loadVanKasterenDataset():
    os.mkdir('dataset')
    sensefile="dataset/mysensedata.txt"
    actfile="dataset/myactdata.txt"
    os.remove(sensefile)
    os.remove(actfile)
    print('Beginning downloading files')
    sense_url = 'https://drive.google.com/uc?id=1sESUFhqWKe7T74ETkBobI3im6P2hhZY_&authuser=0&export=download'
    act_url = 'https://drive.google.com/uc?id=13yULlF6uQVUvFHFS4og69VmmSQ4u613y&authuser=0&export=download'  
    wget.download(sense_url, sensefile)
    wget.download(act_url, actfile)

    all=pd.read_csv(sensefile,'\t',None,header=0,names=["StartTime","EndTime","SID","value"]);
    
    all.StartTime   =pd.to_datetime(all.StartTime,format='%d-%b-%Y %H:%M:%S')
    all.EndTime     =pd.to_datetime(all.EndTime,format='%d-%b-%Y %H:%M:%S')
    global sensor_events
    sensor_events=pd.DataFrame(columns=["time","SID","value"])
    for i,s in all.iterrows():
        sensor_events=sensor_events.append({'time':s.StartTime,'SID':s.SID,'value':s.value},ignore_index=True)
        sensor_events=sensor_events.append({'time':s.EndTime,'SID':s.SID,'value':0},ignore_index=True)
    
    global activity_events
    activity_events=pd.read_csv(actfile,'\t',None,header=0,names=["StartTime","EndTime","Activity"]);
    activity_events.StartTime   =pd.to_datetime(activity_events.StartTime,format='%d-%b-%Y %H:%M:%S')
    activity_events.EndTime     =pd.to_datetime(activity_events.EndTime,format='%d-%b-%Y %H:%M:%S')
    
    activity_events['Duration']=activity_events.EndTime-activity_events.StartTime
    print('finish downloading files')
    acts={
        0: 'None',
        1: 'leave house',
        4: 'use toilet',
        5: 'take shower',
        10:'go to bed',
        13:'prepare Breakfast',
        15:'prepare Dinner',
        17:'get drink'}

    sens={
        1:	'Microwave'         ,
        5:	'Hall-Toilet door'  ,
        6:	'Hall-Bathroom door',
        7:	'Cups cupboard'     ,
        8:	'Fridge'            ,
        9:	'Plates cupboard'   ,
        12:	'Frontdoor'         ,
        13:	'Dishwasher'        ,
        14:	'ToiletFlush'       ,
        17:	'Freezer'           ,
        18:	'Pans Cupboard'     ,
        20:	'Washingmachine'    ,
        23:	'Groceries Cupboard',
        24:	'Hall-Bedroom door' }

    global activities
    global activities_map_inverse
    global activities_map

    activities=[k for v, k in enumerate(acts)]
    activities_map_inverse={k: v for v, k in enumerate(acts)}
    activities_map={v: k for v, k in enumerate(acts)}
    
    global activity_events_tree
    activity_events_tree=IntervalTree()
    for i,act in activity_events.iterrows():
        activity_events_tree[act.StartTime.value:act.EndTime.value]=act  

    ############################################3
    #sensor_events=sensor_events.drop(columns=['activity_hint'])
    global sensor_desc
    global sensor_desc_map
    global sensor_desc_map_inverse
    global sensor_id_map
    global sensor_id_map_inverse
    
    sensor_desc=pd.DataFrame(columns=['ItemId','ItemName','Cumulative','Nominal','OnChange','ItemRange','Location','Object','SensorName'])
    tmp_sensors=sensor_events['SID'].unique()
    for k,s in enumerate(sens):
        item={'ItemId':k,'ItemName':s,'Cumulative':0,'Nominal':1,'OnChange':1,'ItemRange':{'range':['0','1']},'Location':'None','Object':'None','SensorName':'None'}
        sensor_desc=sensor_desc.append(item,ignore_index=True)

    sensor_desc=sensor_desc.sort_values(by=['ItemName'])
    sensor_desc=sensor_desc.set_index('ItemId')

    sensor_desc_map_inverse={}
    sensor_desc_map={}
    #sensor_desc.ItemRange=sensor_desc.ItemRange.apply(lambda x: json.loads(x))
    for i,sd in sensor_desc[sensor_desc.Nominal==1].iterrows():
        sensor_desc_map_inverse[i]={k: v for v, k in enumerate(sd.ItemRange['range'])} 
        sensor_desc_map[i]={v: k for v, k in enumerate(sd.ItemRange['range'])} 
#    sensor_events.value=sensor_events.apply(lambda x:float(x.value) if not(x.SID in sensor_desc_map_inverse) else sensor_desc_map_inverse[x.SID][str(int(x.value))] if type(x.value) is float else sensor_desc_map_inverse[x.SID][x.value],axis=1)
    sensor_id_map={v: k for v, k in enumerate(sensor_desc.index)} 
    sensor_id_map_inverse={k: v for v, k in enumerate(sensor_desc.index)} 


#loadVanKasterenDataset()




















def loadA4HDataSet():
  os.mkdir('dataset')
  actfile="dataset/activities.csv"
  sensfile="dataset/sensor_events.csv"
  descfile="dataset/sensor_description.csv"
  # if not os.path.isfile(actfile) and os.path.isfile(sensfile):
  os.remove(actfile,sensfile,descfile)


  print('Beginning downloading files')

  activity_url = 'https://drive.google.com/uc?authuser=0&id=1cd_AQbHpK4LBHRyuAWQRP2nG4ilsfNMr&export=download'  
  wget.download(activity_url, actfile)  

  sensor_events_url = 'https://drive.google.com/uc?authuser=0&id=1n_ARZ90Ebo0VgS40RU-ycd_4tUhDdZs9&export=download'  
  wget.download(sensor_events_url, sensfile)  

  sensor_description_url = 'https://drive.google.com/uc?authuser=0&id=1QL7bdl8lRbyWdE5uSlMIS9LottgSvDja&export=download'  
  wget.download(sensor_description_url, descfile)  


  global sensor_events
  sensor_events = pd.read_csv(sensfile,)
  t=pd.to_datetime(sensor_events['time'],format='%Y-%m-%d %H:%M:%S')
  sensor_events.loc[:,'time']=t
  sensor_events = sensor_events.sort_values(['time'])
  sensor_events = sensor_events.reset_index()
  sensor_events = sensor_events.drop(columns=['index'])

  global activity_events
  activity_events = pd.read_csv(actfile,index_col='Id')
  
  activity_events = activity_events.sort_values(['StartTime','EndTime'])
  st=pd.to_datetime(activity_events['StartTime'],format='%Y-%m-%d %H:%M:%S')
  et=pd.to_datetime(activity_events['EndTime'],format='%Y-%m-%d %H:%M:%S')
  activity_events['StartTime']=st
  activity_events['EndTime']=et
  #activity_events['Interval']=pd.IntervalIndex.from_arrays(activity_events['StartTime'],activity_events['EndTime'],closed='both')
  activity_events['Duration']=et-st

  
  global activities
  global activities_map_inverse
  global activities_map
  
  activities=activity_events['Activity'].unique()
  activities=np.insert(activities,0,'None')
  activities_map_inverse={k: v for v, k in enumerate(activities)}
  activities_map={v: k for v, k in enumerate(activities)}
  activity_events.Activity=activity_events.Activity.apply(lambda x:activities_map_inverse[x])
  
  global activity_events_tree
  activity_events_tree=IntervalTree()
  for i,act in activity_events.iterrows():
    activity_events_tree[act.StartTime.value:act.EndTime.value]=act  

#############################
  global sensor_desc
  global sensor_desc_map
  global sensor_desc_map_inverse
  global sensor_id_map
  global sensor_id_map_inverse
  sensor_desc_map_inverse={}
  sensor_desc_map={}

  sensor_desc = pd.read_csv(descfile,index_col='ItemId')
  sensor_desc.ItemRange=sensor_desc.ItemRange.apply(lambda x: json.loads(x))
  
  for i,sd in sensor_desc[sensor_desc.Nominal==1].iterrows():
    sensor_desc_map_inverse[i]={k: v for v, k in enumerate(sd.ItemRange['range'])} 
    sensor_desc_map[i]={v: k for v, k in enumerate(sd.ItemRange['range'])} 
  sensor_events.value=sensor_events.apply(lambda x:float(x.value) if not(x.SID in sensor_desc_map_inverse) else sensor_desc_map_inverse[x.SID][str(int(x.value))] if type(x.value) is float else sensor_desc_map_inverse[x.SID][x.value],axis=1)
  sensor_id_map={v: k for v, k in enumerate(sensor_desc.index)} 
  sensor_id_map_inverse={k: v for v, k in enumerate(sensor_desc.index)} 
      
