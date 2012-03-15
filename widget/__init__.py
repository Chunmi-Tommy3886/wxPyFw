__author__="Giuseppe Tripoli"
__date__ ="$15-mar-2012 10.56.17$"
__all__=["widgets"]

import os
import sys
import traceback

from globals.obj_log import o_log
from globals.obj_cfg  import o_cfg

logger = o_log("wxPyFw.log")

class widgets:
    def __init__(self):
        self.widgets = dict()
    
    def get_widget(self):
        try :
            for fname in os.listdir("widget"):
                if fname[-3:] in ["ini"] :
                    cfg = o_cfg("widget/%s" % fname)
                    self.widgets[fname[:-4]] = cfg.configfile
                    
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
        
    
    