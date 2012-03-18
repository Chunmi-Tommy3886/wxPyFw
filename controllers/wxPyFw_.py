__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"

import sys
import traceback

from views.wxPyFw import view_wxpyfw
from models.wxPyFw import model_wxpyfw

from globals import *

logger = _LOGGER_

class controller_wxpyfw (model_wxpyfw, view_wxpyfw):
    def __init__(self):
        try :
            view_wxpyfw.__init__(self)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
