__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"


import os
import wx
import sys
import wx.xrc
import traceback

from globals import *

logger = _LOGGER_

PROJECT_NAME = "PROJECT NAME"

class view_wxpyfw():
    def __init__(self):
        
        self.panel = self.frame.panel
        
        self.popolate_treectrl()
    
    def popolate_treectrl(self):
        try :
            #self.treectrl = wx.xrc.XRCCTRL(self.panel, "treectrl")
            self.dirctrl = wx.xrc.XRCCTRL(self.panel, "dirctrl")
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
            raise NameError("qui1")
        else :
            try :
                #self.treectrl.AddRoot(PROJECT_NAME)
                self.dirctrl.SetPath(os.walk('.'))
                self.dirctrl.SetDefaultPath(os.walk('.'))

                
                #print self.list_dir_file()
            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
                raise NameError("qui")
            
