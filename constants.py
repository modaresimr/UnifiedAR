no_memory_limit=True
import pandas as pd

import classifier.Keras
import classifier.PyActLearn
import classifier.sklearn
import classifier.libsvm
import datatool.a4h_handeler
import datatool.casas_handeler
import datatool.vankasteren_handeler
import activity_fetcher.CookActivityFetcher
import activity_fetcher.MaxActivityFetcher
from classifier.sklearn import UAR_DecisionTree
import combiner.SimpleCombiner
import evaluation.SimpleEval
import evaluation.KFoldEval
import feature_extraction.Simple
import feature_extraction.KHistory
import feature_extraction.DeepLearningFeatureExtraction
import feature_extraction.Cook
import feature_extraction.PAL_Features
import feature_extraction.Raw
# from general.libimport import *
from general.utils import Data
from metric import *
import ml_strategy.Simple
import ml_strategy.SeperateGroup
import preprocessing.SimplePreprocessing
import segmentation.Probabilistic
import segmentation.FixedEventWindow
import segmentation.FixedSlidingWindow
import segmentation.FixedTimeWindow

methods = Data('methods')

methods.segmentation = [
#     {'method': lambda: segmentation.Probabilistic.Probabilistic(), 'params': [], 'findopt':False},
#    {'method': lambda: segmentation.FixedEventWindow.FixedEventWindow(), 'params': [
#        {'var': 'size', 'min': 10, 'max': 30, 'type': 'int', 'init': 14},
#        {'var': 'shift', 'min': 2, 'max': 20, 'type': 'int', 'init': 12}
#           ], 'findopt': False},
    {'method': lambda: segmentation.FixedSlidingWindow.FixedSlidingWindow(), 'params': [
        {'var': 'size' , 'min': 60, 'max': 15*60, 'type': 'float', 'init': 120/2, 'range':list(range(30,180,60))},
        {'var': 'shift', 'min': 10, 'max': 7*60 , 'type': 'float', 'init': 60, 'range':list(range(30,180,60))}
    ], 'findopt': True}
    #   {'method': lambda:segmentation.FixedTimeWindow.FixedTimeWindow(), 'params':[
    #                  {'var':'size','min':pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(30, unit='m').total_seconds(), 'type':'float','init':pd.Timedelta(15, unit='s').total_seconds()},
    #                  {'var':'shift','min':pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(30, unit='m').total_seconds(), 'type':'float','init':pd.Timedelta(1, unit='s').total_seconds()}
    #              ],
    #   'findopt':False},
    
]


methods.preprocessing = [
    {'method': lambda: preprocessing.SimplePreprocessing.SimplePreprocessing()},
    ]
methods.classifier = [
    #     {'method': lambda:classifier.libsvm.LibSVM(), 'params':[],
    #  'findopt':False},
    # {'method': lambda: classifier.Keras.SimpleKeras(), 'params': [
    #     {'var': 'epochs', 'init': 3}
    # ]},
    {'method': lambda: classifier.Keras.LSTMTest(), 'params': [
        {'var': 'epochs', 'init': 3}
    ]},
    # {'method': lambda: classifier.PyActLearn.PAL_LSTM_Legacy(), 'params': [
    #     {'var': 'epochs', 'init': 3}
    # ]},
    # {'method': lambda: classifier.sklearn.UAR_RandomForest(), 'params': [
    #     {'var': 'n_estimators', 'init': 20},
    #     {'var':'random_state','init':0}
    # ]},
    # {'method': lambda: classifier.sklearn.UAR_KNN(), 'params': [
    #     {'var': 'k', 'init': 5},
    # ]},
    # {'method': lambda: classifier.sklearn.UAR_SVM(), 'params': [
    #     {'var': 'kernel', 'init': 'rbf'},
    #     {'var': 'gamma', 'init': 1},
    #     {'var': 'C', 'init': 100.},
    #     {'var':'decision_function_shape','init':'ovr'}
    # ]},
    # {'method': lambda: classifier.sklearn.UAR_SVM2(), 'params': [
    #     {'kernel': 'linear'},
    #     {'gamma': 1},
    #     {'C':100.},
    #     {'decision_function_shape':'ovr'}
    # ]},
    # #{'method': lambda: classifier.sklearn.UAR_DecisionTree(), 'params': [ ]},
    # {'method': lambda: classifier.Keras.LSTMTest(), 'params': [
    #     {'var': 'epochs',  'init': 3}
    # ]},
]


methods.classifier_metric = [
    {'method': lambda: classical.Accuracy()},
    #{'method': lambda: Accuracy()},
]

methods.event_metric = [
    {'method': lambda: Accuracy()},
    #{'method': lambda: Accuracy()},
]

methods.activity_fetcher = [
    # {'method': lambda: activity_fetcher.CookActivityFetcher.CookActivityFetcher()}
    {'method': lambda: activity_fetcher.MaxActivityFetcher.MaxActivityFetcher()}
    ]
methods.combiner = [
    # {'method':lambda: combiner.SimpleCombiner.SimpleCombiner()},
    {'method':lambda: combiner.SimpleCombiner.EmptyCombiner()}
    ]
methods.evaluation = [
     {'method': lambda: evaluation.SimpleEval.SimpleEval()},
    # {'method': lambda: evaluation.KFoldEval.KFoldEval(5)},
]


methods.feature_extraction = [
    # {'method': lambda:feature_extraction.Simple.Simple(), 'params':[], 'findopt':False},
    # {'method': lambda:feature_extraction.KHistory.KHistory(), 'params':[{'k':3},{'method':feature_extraction.Cook.Cook1()}],'findopt':False},
    {'method': lambda:feature_extraction.KHistory.KHistory(), 'params':[{'k':2},{'method':feature_extraction.Simple.Simple()}],'findopt':False},
    # {'method': lambda:feature_extraction.KHistory.KHistory(), 'params':[{'k':1},{'method':feature_extraction.Simple.Simple()}],'findopt':False},
    #  {'method': lambda:feature_extraction.DeepLearningFeatureExtraction.DeepLearningFeatureExtraction(), 'params':[
    #             {'var':'size','min':10, 'max': 20, 'type':tf.int8,'init':50},
    #             {'var':'layers','min':1, 'max': 3, 'type':tf.int8,'init':pd.Timedelta(20, unit='s').total_seconds()}
    #         ],
    #  'findopt':False},
    # {'method': lambda: feature_extraction.Cook.Cook1(), 'params': [],     'findopt':False},
    #  {'method': lambda: feature_extraction.PAL_Features.PAL_Features(), 'params': [],  'findopt':False},
    #  {'method': lambda:feature_extraction.Raw.Classic(), 'params': [ {'var':'normalized','init':True}  ],'findopt':False},
    # {'method': lambda:feature_extraction.Raw.Sequence(), 'params': [ {'var':'normalized','init':True},{'var':'per_sensor','init':True}   ],'findopt':False},
]


methods.dataset = [
    {'method': lambda: datatool.casas_handeler.CASAS('datasetfiles/CASAS/KaryoAdlNormal/','KaryoAdlNormal')},
    {'method': lambda: datatool.casas_handeler.CASAS('datasetfiles/CASAS/Home1/','Home1')},
    {'method': lambda: datatool.casas_handeler.CASAS('datasetfiles/CASAS/Home2/','Home2')},
    {'method': lambda: datatool.a4h_handeler.A4H('datasetfiles/A4H/','A4H')},
    {'method': lambda: datatool.vankasteren_handeler.VanKasteren('datasetfiles/VanKasteren/','VanKasteren')},
]

methods.mlstrategy = [
    #{'method': lambda: ml_strategy.Simple.SimpleStrategy()},
    {'method': lambda: ml_strategy.SeperateGroup.SeperateGroupStrategy()},
    
]
