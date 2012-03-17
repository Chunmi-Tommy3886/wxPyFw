__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"

import sys
import traceback

from views.options import view_options
from models.options import model_options

from globals import *

logger = _LOGGER_

class controller_options(model_options, view_options):
    def __init__(self, window):
        self.window = window
        self.res = window.res
        self.frame = window.frame
        self.panel = window.panel
        
        try :
            view_options.__init__(self)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
