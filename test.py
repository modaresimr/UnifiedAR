
from constants import methods
import importlib
import constants
importlib.reload(constants)
display(methods.classifier)
methods.classifier = []
display(methods.classifier)
