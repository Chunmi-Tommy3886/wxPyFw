__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"

import os
import wx
import sys
import wx.xrc
import wx.aui
import wx.lib.agw.aui
import wx.stc
import traceback

from widget import *

from globals import *

from views.editor import code_editor

logger = _LOGGER_

class view_options:
    def __init__(self):
        try :
            self.panel = self.res.LoadDialog(self.panel, 'options')

            self.panel.Show()

            self.create_dialog()
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))

        
    def create_dialog(self):
        pass
        