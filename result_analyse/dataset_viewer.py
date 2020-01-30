from matplotlib.pylab import plt
import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.patches as patches

import plotly.figure_factory as ff


import matplotlib._color_data as mcd
import matplotlib.dates as mdates


def displaycontent(dataset):
    if not(hasattr(dataset,'sensor_events')):
          return
    print('sensor events:');
    print(dataset.sensor_events.iloc[20:25])
    print('activity_events:');
    print(dataset.activity_events.loc[1:1])
    print('sensor_desc:');
    print(dataset.sensor_desc.iloc[1:3])
    print("Activites: ", dataset.activities)
    for a, v in dataset.activities_map.items():
        items = dataset.activity_events.loc[dataset.activity_events['Activity']
            == a]['Duration']
        print(a, v, '\t--> count=', items.count(),
              ' avg duration=', str(items.mean()))
# loadA4HDataSet()
# loadVanKasterenDataset()
# loadKaryoAdlNormalDataset();
# display()


def view(dataset, i):
  if not(hasattr(dataset,'sensor_events')):
          return
  tmp_act_evants = dataset.activity_events.loc[dataset.activity_events['Activity'] == i]
  print(dataset.activities_map[i])
  print(tmp_act_evants['Duration'].describe())

  fig = plt.figure()

  tmp_act_evants['StartTime'].iloc[0]
  all = pd.DataFrame()
  for index, row in tmp_act_evants.iterrows():
    myse = dataset.sensor_events.loc[(dataset.sensor_events['time'] >= row['StartTime']) & (
        dataset.sensor_events['time'] <= row['EndTime'])].copy()
    myse['relative'] = dataset.sensor_events['time']-row['StartTime']
    myse['tpercent'] = myse['relative']/row['Duration']
    all = pd.concat([all, myse[['tpercent', 'SID']]])
    # plt.scatter(myse['tpercent'],myse['SID'])

  tmp = all.copy()

  tmp['tpercent'] = (tmp['tpercent']*2).round(0)/2
  fig = plt.figure(figsize=(10, 5))
  a = pd.pivot_table(tmp, columns='tpercent', index='SID',
                     aggfunc=np.count_nonzero, fill_value=0)
  a = a/a.max();
  # plt.imshow(a, cmap='hot', interpolation='nearest')

  sns.heatmap(a/a.max(), cmap=sns.cm.rocket_r);

# view(5)


def plotAct(dataset, acts):
  firstacts = acts.iloc[0];
  lastact = acts.iloc[-1];
  lastactinDay = acts.loc[acts['StartTime'] <
      firstacts['StartTime']+pd.Timedelta('20h')].iloc[-1];

  acts=acts.loc[acts['StartTime']<firstacts['StartTime']+pd.Timedelta('7d')]
  for a in dataset.activities:
    acts = acts.append(
        {'Activity': dataset.activities_map_inverse[a], 'StartTime': firstacts['StartTime'], 'EndTime': firstacts['StartTime']}, ignore_index=True)

  acts = acts.sort_values(by='Activity')

  df2 = acts.apply(lambda x: dict(
      Task=dataset.activities_map[x.Activity], Color=0, Start=x.StartTime, Finish=x.EndTime), axis=1).tolist()
  # configure_plotly_browser_state()
  # init_notebook_mode(connected=False)
  # fig=ff.create_gantt(df2, index_col='Color', group_tasks=True)
  

  fig = ff.create_gantt(df2, group_tasks=True)
  fig['layout'].update(margin=dict(l=150))
  fig['layout'].update(xaxis=dict(
        range=[firstacts['StartTime'], lastactinDay['EndTime']],
        rangeselector=dict(
            buttons=list([
                dict(count=4,
                     label='4h',
                     step='hour',
                     stepmode='backward'),
                dict(count=6,
                     label='6h',
                     step='hour',
                     stepmode='backward'),
                dict(count=8,
                     label='8h',
                     step='hour',
                     stepmode='backward'),
                dict(count=10,
                     label='10h',
                     step='hour',
                     stepmode='backward'),
                dict(count=12,
                     label='12h',
                     step='hour',
                     stepmode='backward'),
                dict(count=1,
                     label='1d',
                     step='day',
                     stepmode='backward'),
                dict(count=5,
                     label='5d',
                     step='day',
                     stepmode='backward'),

                dict(step='all')
            ])
        ), rangeslider=dict(
            visible=True,
            range=[firstacts['StartTime'], lastact['EndTime']],
        )))
  fig.show()


