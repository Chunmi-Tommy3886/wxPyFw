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

class view_newfile:
    def __init__(self):
        try :
            self.panel = self.res.LoadDialog(self.panel, 'newfile')
            
            #wx.xrc.XRCCTRL(self.panel, 'path').SetPath(self.infofile["path"])
        
            wx.xrc.XRCCTRL(self.panel, 'create').Bind(wx.EVT_BUTTON, self.CreateAndOpenFile)

            self.panel.Show()
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
    
    def CreateAndOpenFile(self, event):
        f = os.open(wx.xrc.XRCCTRL(self.panel, 'path').GetPath(), 'a')
        f.close()
        
        