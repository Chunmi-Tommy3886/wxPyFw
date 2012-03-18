__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"

import sys
import traceback

from views.wxpyfw import view_wxpyfw
from models.wxpyfw import model_wxpyfw

from globals import *

class controller_wxpyfw(model_wxpyfw, view_wxpyfw):
    def __init__(self, window):
        self.res = window.res
        self.window = window
        self.frame = window.frame
        self.panel = window.panel
        
        try :
            view_wxpyfw.__init__(self)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
