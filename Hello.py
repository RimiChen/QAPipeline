import sys
# regular expression
import re
import random

import os

####R improt Rensa part
# extract inforamrtion according to sentence frame
sys.path.insert(0, './src/src/')

from ConceptExtractor_new import *
from Brain import *


class Hello:
    __gui = None
    
    def __init__(self, gui):
        self.__gui = gui
 
    def run(self):
        #print 'Hello world!'
        test_rensa_functions()