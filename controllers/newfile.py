__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"

import sys
import traceback

from views.newfile import view_newfile
from models.newfile import model_newfile

from globals import *

logger = _LOGGER_

class controller_newfile(model_newfile, view_newfile):
    def __init__(self, window):
        self.window = window
        self.res = window.res
        self.frame = window.frame
        self.panel = window.panel
        
        self.infofile = None
        
        try :
            view_newfile.__init__(self)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
