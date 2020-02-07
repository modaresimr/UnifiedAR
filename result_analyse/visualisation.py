import matplotlib.dates as mdates
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import sklearn.metrics
from matplotlib.pylab import plt
from wardmetrics.core_methods import eval_events, eval_segments
from wardmetrics.utils import *
from wardmetrics.visualisations import *

import metric.MyMetric as MyMetric
import result_analyse.dataset_viewer as dv
import result_analyse.SpiderChart as spiderchart
from metric.CMbasedMetric import CMbasedMetric
from metric.EventBasedMetric import time2int


def my_result_analyse(dataset,real_events,pred_events):
    # visualize(dataset)
    remove_gaps(real_events,pred_events)
    print('visualizing real and pred')
    plotJoinAct(dataset,real_events,pred_events)
    plotMyMetric(dataset,real_events,pred_events)
    plotWardMetric(dataset,real_events,pred_events)

def plotWardMetric(dataset,real_events,pred_events):
    # Calculate segment results:
    acts=[i for i in dataset.activities_map]
    revent = {}
    pevent = {}
    for act in acts:
        revent[act]=[]
        pevent[act]=[]
        
    for i,e in real_events.iterrows():
        revent[e.Activity].append((time2int(e.StartTime), time2int(e.EndTime)))
    for i,e in pred_events.iterrows():
        pevent[e.Activity].append((time2int(e.StartTime), time2int(e.EndTime)))

    result={}
    for act in acts:
        ground_truth_test=revent[act]
        detection_test=pevent[act]
        print(dataset.activities_map[act],"==================================")
        if(len(ground_truth_test)==0 or len(detection_test)==0):
            continue

        twoset_results, segments_with_scores, segment_counts, normed_segment_counts = eval_segments(ground_truth_test, detection_test)

        # Print results:
        print_detailed_segment_results(segment_counts)
        print_detailed_segment_results(normed_segment_counts)
        print_twoset_segment_metrics(twoset_results)

        # Access segment results in other formats:
        print("\nAbsolute values:")
        print("----------------")
        print(detailed_segment_results_to_list(segment_counts)) # segment scores as basic python list
        print(detailed_segment_results_to_string(segment_counts)) # segment scores as string line
        print(detailed_segment_results_to_string(segment_counts, separator=";", prefix="(", suffix=")\n")) # segment scores as string line

        print("Normed values:")
        print("--------------")
        print(detailed_segment_results_to_list(normed_segment_counts)) # segment scores as basic python list
        print(detailed_segment_results_to_string(normed_segment_counts)) # segment scores as string line
        print(detailed_segment_results_to_string(normed_segment_counts, separator=";", prefix="(", suffix=")\n")) # segment scores as string line

        # Access segment metrics in other formats:
        print("2SET metrics:")
        print("-------------")
        print(twoset_segment_metrics_to_list(twoset_results)) # twoset_results as basic python list
        print(twoset_segment_metrics_to_string(twoset_results)) # twoset_results as string line
        print(twoset_segment_metrics_to_string(twoset_results, separator=";", prefix="(", suffix=")\n")) # twoset_results as string line

        # Visualisations:
        plot_events_with_segment_scores(segments_with_scores, ground_truth_test, detection_test)
        plot_segment_counts(segment_counts)
        plot_twoset_metrics(twoset_results)


        # Run event-based evaluation:
        gt_event_scores, det_event_scores, detailed_scores, standard_scores = eval_events(ground_truth_test, detection_test)

        # Print results:
        print_standard_event_metrics(standard_scores)
        print_detailed_event_metrics(detailed_scores)

        # Access results in other formats:
        print(standard_event_metrics_to_list(standard_scores)) # standard scores as basic python list, order: p, r, p_w, r_w
        print(standard_event_metrics_to_string(standard_scores)) # standard scores as string line, order: p, r, p_w, r_w)
        print(standard_event_metrics_to_string(standard_scores, separator=";", prefix="(", suffix=")\n")) # standard scores as string line, order: p, r, p_w, r_w

        print(detailed_event_metrics_to_list(detailed_scores)) # detailed scores as basic python list
        print(detailed_event_metrics_to_string(detailed_scores)) # detailed scores as string line
        print(detailed_event_metrics_to_string(detailed_scores, separator=";", prefix="(", suffix=")\n")) # standard scores as string line


        # Show results:
        plot_events_with_event_scores(gt_event_scores, det_event_scores, ground_truth_test, detection_test, show=False)
        plot_event_analysis_diagram(detailed_scores)


def remove_gaps(real_events,pred_events):
    pc=0
    removdur=pd.to_timedelta('0s')
    for rc in range(1,len(real_events)):
        lasttime=real_events.iloc[rc]['EndTime']
        real_events.iloc[rc]['EndTime']-=removdur
        real_events.iloc[rc]['StartTime']-=removdur
        
        while (pc<len(pred_events) and pred_events.iloc[pc]['StartTime']-removdur<lasttime):
            pred_events.iloc[pc]['EndTime']-=removdur
            pred_events.iloc[pc]['StartTime']-=removdur
            pc+=1
        
        if(pc>0):
            lasttime=max(lasttime,pred_events.iloc[pc-1]['EndTime'])

        dur=max(real_events.iloc[rc]['Duration'],pd.to_timedelta('5m'))
        
        if(rc+1>=len(real_events)):break
        elif pc>=len(pred_events):
            inittime=real_events.iloc[rc+1]['StartTime']
        else:
            inittime=min(real_events.iloc[rc+1]['StartTime'],pred_events.iloc[pc]['StartTime'])
        
        removdur+=inittime-lasttime- dur
    
    for i in range(pc,len(pred_events)):
        pred_events.iloc[i]['EndTime']-=removdur
        pred_events.iloc[i]['StartTime']-=removdur


        



    

def plotMyMetric(dataset,real_events,pred_events):
    res=MyMetric.eval(real_events,pred_events,[i for i in dataset.activities_map],debug=0)

    for i in range(len(res)):
        metrics=res[i]
        plotJoinAct(dataset,real_events,pred_events,onlyAct=i)
        df=pd.DataFrame(metrics)
        print(dataset.activities_map[i],"========")
        print(df)
        df=df.drop(['tp','fp','fn'])
        spiderchart.plot(df,[0.25,.5,.75])


def visualize(dataset):
    dv.displaycontent(dataset)
    dv.view(dataset,1)
    dv.plotAct(dataset,dataset.activity_events)

#from general.utils import loadState
#dataset,real_events,pred_events=loadState('r1')
#my_result_analyse(dataset,real_events,pred_events)

def plotJoinAct(dataset, real_acts, pred_acts,label=None,onlyAct=None):
  from pandas.plotting import register_matplotlib_converters
  register_matplotlib_converters()
  size=0.45
  if not(onlyAct is None):
      real_acts=real_acts.loc[real_acts.Activity==onlyAct]
      pred_acts=pred_acts.loc[pred_acts.Activity==onlyAct]

  if(len(real_acts)==0):
    return
  ft=real_acts.StartTime.iloc[0]
  dur=ft+pd.to_timedelta('12h')
  real_acts=real_acts.loc[real_acts.StartTime<dur]
  pred_acts=pred_acts.loc[pred_acts.StartTime<dur]
  # apply(lambda x:dataset.activities_map[x.Activity], axis=1).tolist()
  ract = (real_acts.Activity+(size/2)).tolist()
  rstart = real_acts.StartTime.tolist()
  rend = real_acts.EndTime.tolist()
  # .apply(lambda x:dataset.activities_map[x.Activity], axis=1).tolist()
  pact = (pred_acts.Activity-(size/2)).tolist()
  pstart = pred_acts.StartTime.tolist()
  pend = pred_acts.EndTime.tolist()
  if(onlyAct):
      fig, ax = plt.subplots(figsize=(10, 2))
  else:
      fig, ax = plt.subplots()
  ax.set_title(label)
  _plotActs(ax,ract, rstart, rend,
                      linewidth=1,edgecolor='k',facecolor='g', size=size, alpha=.6)
  _plotActs(ax,pact, pstart, pend,
                      linewidth=1,edgecolor='k',facecolor='r', size=size, alpha=.6)
#   data_linewidth_plot(pact, pstart, pend, ax=ax,
#                       colors="red", alpha=1, linewidth=.3)
  # plt.hlines(ract, rstart, rend, colors=(0,.5,0,.2), linewidth=1)
  # plt.hlines(pact, pstart, pend, colors="red", lw=2)
  loc = mdates.HourLocator(interval=2)
  ax.xaxis.set_major_locator(loc)
  ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

  ax.set_yticks([i for i in dataset.activities_map])
  ax.yaxis.grid(True)

  ax.set_yticklabels([l for l in dataset.activities_map_inverse])
  if(onlyAct):
    ax.set_ylim(onlyAct-size,onlyAct+size)
  else:
    ax.set_ylim(-1+size,len(dataset.activities)-size)
  plt.margins(0.1)
  plt.show()


def _plotActs(ax, x, s, e, **kwargs):
          size = kwargs.pop("size", 1)
          for i in range(len(x)):
               ax.add_patch(patches.Rectangle((s[i],x[i]-size/2), e[i]-s[i],size, **kwargs))

               # 




def plot_CM(dataset,evalres):
    sumcm=evalres[0].event_cm
    for i in range(1,len(evalres)):
        cm=evalres[i].event_cm
        sumcm+=cm
    #plot_confusion_matrix(sumcm,evalres[0].Sdata.acts,figsize=[25,12])
    tmp2(sumcm,dataset.activities)

def tmp(cm,acts):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.imshow(cm, interpolation='nearest')
    plt.xticks(np.arange(0,len(acts)), acts)
    plt.yticks(np.arange(0,len(acts)), acts)

    plt.show()

def tmp2(cm,acts):
	import numpy as np
	import matplotlib.pyplot as plt

	conf_arr = cm

	norm_conf = []
	for i in conf_arr:
		a = 0
		tmp_arr = []
		a = sum(i, 0)
		for j in i:
			tmp_arr.append(0 if a==0 else float(j)/float(a))
		norm_conf.append(tmp_arr)

	fig = plt.figure()
	plt.clf()
	ax = fig.add_subplot(111)
	ax.set_aspect(1)
	res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet, 
					interpolation='nearest')

	width, height = conf_arr.shape

	# for x in range(width):
	# 	for y in range(height):
	# 		ax.annotate(str(conf_arr[x][y]), xy=(y, x), 
	# 					horizontalalignment='center',
	# 					verticalalignment='center')

	cb = fig.colorbar(res)
	# alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	plt.xticks(range(width), acts,rotation=-90)
	plt.yticks(range(height), acts)
	plt.show()

def plot_pre_act(dataset,myevalres):
    activities=dataset.activities
    summycm={}
    sumcm={}
    for p in myevalres:
        evalres=myevalres[p]
        summycm[p]=np.zeros((len(activities),len(activities)))
        for i in range(len(evalres)):
            cm=evalres[i].event_cm
            summycm[p]+=cm

        sumcm[p]=np.zeros((len(activities),len(activities)))
        for i in range(0,len(myevalres)):
            cm=sklearn.metrics.confusion_matrix(evalres[i].Sdata.label, evalres[i]. predicted_classes,labels=range(len(activities)))
            sumcm[p]+=cm
    import matplotlib.pyplot as plt
    def get_new_fig(fn, figsize=[12,9]):
        """ Init graphics """
        fig1 = plt.figure(fn, figsize)
        ax1 = fig1.gca()   #Get Current Axis
        ax1.cla() # clear existing plot
        return fig1, ax1


    bar_count=len(myevalres)
    x = np.arange(len(activities))  # the label locations

    fig, ax = get_new_fig(',',[20,5])#plt.subplots()
    rects=[]
    width=.7/(bar_count*2)
    for i,p in enumerate(myevalres):
        e2=(100*CMbasedMetric(sumcm[p],average=None)['f1']).round()
        rects.append(ax.bar(x - 1.2*width*(i+.5), e2, width, label=p))
        e3=(100*CMbasedMetric(summycm[p],average=None)['f1']).round()        
        rects.append(ax.bar(x + (1.2*width*(i+.5)), e3, width, label='MY '+p))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    name='F1 score'
    ax.set_ylabel(name)
    ax.set_title(dataset.data_dscr)
    ax.set_xticks(x)
    ax.set_xticklabels(dataset.activities_map_inverse,rotation=-60)

    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    #for rect in rects:
        #autolabel(rect)

    fig.tight_layout()
    fig.patch.set_facecolor('white')
    plt.show()
