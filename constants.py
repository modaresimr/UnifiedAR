from general.utils import Data
from general.libimport import *
from datatool import *


methods = Data('methods')

methods.segmentation = [{'method': lambda: FixedEventWindow(), 'params': [
    {'var': 'size', 'min': 10, 'max': 30, 'type': 'int', 'init': 20},
    {'var': 'shift', 'min': 1, 'max': 20, 'type': 'int', 'init': 1}
], 'findopt': False},
    {'method': lambda: FixedSlidingWindow(), 'params': [
        {'var': 'size', 'min': pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(
            30, unit='m').total_seconds(), 'type': 'float', 'init': pd.Timedelta(15, unit='s').total_seconds()},
        {'var': 'shift', 'min': pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(
            30, unit='m').total_seconds(), 'type': 'float', 'init': pd.Timedelta(1, unit='s').total_seconds()}
    ], 'findopt': False},
    #   {'method': lambda:FixedTimeWindow(), 'params':[
    #                  {'var':'size','min':pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(30, unit='m').total_seconds(), 'type':'float','init':pd.Timedelta(15, unit='s').total_seconds()},
    #                  {'var':'shift','min':pd.Timedelta(1, unit='s').total_seconds(), 'max': pd.Timedelta(30, unit='m').total_seconds(), 'type':'float','init':pd.Timedelta(1, unit='s').total_seconds()}
    #              ],
    #   'findopt':False},
    {'method': lambda: Probabilistic(), 'params': [], 'findopt':False}
]


methods.preprocessing = []
methods.classifier = [
    #     {'method': lambda:SVMClassifier(), 'params':[],
    #  'findopt':False},
    {'method': lambda: LSTMTest(), 'params': [
        {'var': 'epochs', 'min': 10, 'max': 20, 'type': tf.int8, 'init': 3}
    ], 'findopt': False},
]

methods.activity_fetcher = []
methods.combiner = []
methods.evalution = []


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
    {'method': lambda: CASAS.KaryoAdlNormal(), 'params': [], 'findopt':False},
    {'method': lambda: CASAS.Home1(), 'params': [], 'findopt':False},
    {'method': lambda: CASAS.Home2(), 'params': [], 'findopt':False},
    {'method': lambda: A4H(), 'params': [], 'findopt':False},
    {'method': lambda: VanKasteren(), 'params': [], 'findopt':False},
]
