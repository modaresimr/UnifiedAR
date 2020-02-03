
import  general.utils as utils
import  datatool.testdata as testdata
import result_analyse.visualisation as vs

result='CASASr1'
#result='A4Hr1'
# dataset,real_events,pred_events=utils.loadState(result)



# vs.my_result_analyse(dataset,real_events,pred_events)

utils.saveState(result,'a/b/c')