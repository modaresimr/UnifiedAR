def displaycontent():
    print('sensor events:');
    print(sensor_events.iloc[20:25])
    print('activity_events:');
    print(activity_events.loc[1:1])
    print('sensor_desc:');
    print(sensor_desc.iloc[1:3])
    print("Activites: ",activities)
    for a,v in activities_map.items():
        items=activity_events.loc[activity_events['Activity']==a]['Duration']
        print (a,v,'\t--> count=',items.count(), ' avg duration=',str(items.mean()))
#loadA4HDataSet()
#loadVanKasterenDataset()
#loadKaryoAdlNormalDataset();
#display()


def view(i):
  tmp_act_evants=activity_events.loc[activity_events['Activity']==i]
  print(activities_map[i])
  print(tmp_act_evants['Duration'].describe())



  fig = plt.figure()

  tmp_act_evants['StartTime'].iloc[0]
  all=pd.DataFrame()
  for index, row in tmp_act_evants.iterrows():
    myse=sensor_events.loc[(sensor_events['time']>=row['StartTime']) & (sensor_events['time']<=row['EndTime'])].copy()
    myse['relative']=sensor_events['time']-row['StartTime']
    myse['tpercent']=myse['relative']/row['Duration']
    all=pd.concat([all,myse[['tpercent','SID']]])
    #plt.scatter(myse['tpercent'],myse['SID'])

  tmp=all.copy()

  tmp['tpercent']=(tmp['tpercent']*2).round(0)/2
  fig = plt.figure(figsize=(10,5))
  a=pd.pivot_table(tmp,columns='tpercent',index='SID',aggfunc=np.count_nonzero,fill_value=0)
  a=a/a.max();
  #plt.imshow(a, cmap='hot', interpolation='nearest')

  sns.heatmap(a/a.max(),cmap=sns.cm.rocket_r);
  global ali
  ali=tmp
#view(5)