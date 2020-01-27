
import result_analyse.visualisation as vs
import general.utils as utils


dataset, real_events, pred_events = utils.loadState('r1')

vs.my_result_analyse(dataset, real_events, pred_events)


