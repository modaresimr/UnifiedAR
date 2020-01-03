

# from activity_fetcher import *
# from classifier import *
# from combiner import *
from constants import *
# from datatool import *
# from evaluation import *
# from feature_extraction import *
# from general import *
# from metric import *
# from preprocessing import *
# from segmentation import *

   
datasetdscr=methods.dataset[0]['method']().load()
strategy=methods.mlstrategy[0]['method']()
evalres=methods.evaluation[0]['method']().evaluate(datasetdscr,strategy)

print(strategy.evaluate(evalres))
