
__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.03.26$"


import wx
import sys
import wx.xrc
import traceback

from globals import *

logger = _LOGGER_

class window(wx.App):
    def OnInit(self):
        self.res = wx.xrc.XmlResource('gui\wxPyFw.xrc')
        self.LoadFrame()
        return True

    def LoadFrame(self):
        try :
            self.frame = self.res.LoadFrame(None, 'main_frame')
            self.panel = wx.xrc.XRCCTRL(self.frame, 'main_panel')
            
            self.sizer = wx.BoxSizer( wx.VERTICAL )
            self.sizer.Add( self.panel, 1, wx.EXPAND | wx.ALL, 0 )
            self.frame.SetSizer( self.sizer )

            self.LoadController('wxpyfw')
            
            self.frame.Layout()
            self.frame.Show()
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
        
    def LoadController(self, controller):
        try :
            module = __import__('controllers.%s' % controller, globals(), locals(), ["controller_%s" % controller], -1)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
        else :
            init = getattr(module, "controller_%s" % (controller))
            return init(self)
            
        