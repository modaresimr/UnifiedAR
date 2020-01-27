no_memory_limit=True
from activity_fetcher import *
from classifier import *
from combiner import *
from datatool import *
from evaluation import *
from feature_extraction import *
from general.libimport import *
from general.utils import Data
from metric import *
from ml_strategy import *
from preprocessing import *
from segmentation import *
import pandas as pd

methods = Data('methods')

methods.segmentation = [
    #{'method': lambda: Probabilistic(), 'params': [], 'findopt':False},
    # {'method': lambda: FixedEventWindow(), 'params': [
    #     {'var': 'size', 'min': 10, 'max': 30, 'type': 'int', 'init': 20},
    #     {'var': 'shift', 'min': 1, 'max': 20, 'type': 'int', 'init': 1}
    #        ], 'findopt': False},
    {'method': lambda: FixedSlidingWindow(), 'params': [
        {'var': 'size', 'min': pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(
            30, unit='m').total_seconds(), 'type': 'float', 'init': pd.Timedelta(60, unit='s').total_seconds()},
        {'var': 'shift', 'min': pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(
            30, unit='m').total_seconds(), 'type': 'float', 'init': pd.Timedelta(50, unit='s').total_seconds()}
    ], 'findopt': False}
    #   {'method': lambda:FixedTimeWindow(), 'params':[
    #                  {'var':'size','min':pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(30, unit='m').total_seconds(), 'type':'float','init':pd.Timedelta(15, unit='s').total_seconds()},
    #                  {'var':'shift','min':pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(30, unit='m').total_seconds(), 'type':'float','init':pd.Timedelta(1, unit='s').total_seconds()}
    #              ],
    #   'findopt':False},
    
]


methods.preprocessing = [
    {'method': lambda: SimplePreprocessing()},
    ]
methods.classifier = [
    #     {'method': lambda:SVMClassifier(), 'params':[],
    #  'findopt':False},
    {'method': lambda: SimpleKeras(), 'params': [
        {'var': 'epochs', 'init': 3}
    ]},
    # {'method': lambda: LSTMTest(), 'params': [
    #     {'var': 'epochs', 'min': 10, 'max': 20, 'type': tf.int8, 'init': 3}
    # ], 'findopt': False},
]


methods.classifier_metric = [
    {'method': lambda: classical.Accuracy()},
    #{'method': lambda: Accuracy()},
]

methods.event_metric = [
    {'method': lambda: Accuracy()},
    #{'method': lambda: Accuracy()},
]

methods.activity_fetcher = [{'method': lambda: CookActivityFetcher()}]
methods.combiner = [{'method':lambda: SimpleCombiner()}]
methods.evaluation = [
    {'method': lambda: SimpleEval()},
    {'method': lambda: KFoldEval(5)},
]


methods.feature_extraction = [
    # {'method': lambda:SimpleFeatureExtraction(), 'params':[],
    #  'findopt':False},
    #  {'method': lambda:DeepLearningFeatureExtraction(), 'params':[
    #             {'var':'size','min':10, 'max': 20, 'type':tf.int8,'init':50},
    #             {'var':'layers','min':1, 'max': 3, 'type':tf.int8,'init':pd.Timedelta(20, unit='s').total_seconds()}
    #         ],
    #  'findopt':False},
    {'method': lambda: Cook1FeatureExtraction(), 'params': [],
     'findopt':False},
]


methods.dataset = [
    {'method': lambda: CASAS.KaryoAdlNormal()},
    {'method': lambda: CASAS.Home1()},
    {'method': lambda: CASAS.Home2()},
    {'method': lambda: A4H()},
    {'method': lambda: VanKasteren()},
]

methods.mlstrategy = [
    {'method': lambda: SimpleStrategy()},
    {'method': lambda: SeperateGroupStrategy()},
    
]
