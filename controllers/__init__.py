
__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.03.26$"


import wx
import sys
import wx.xrc
import traceback

from wxPyFw import controller_wxpyfw

from globals import *

logger = _LOGGER_

class window(wx.App, controller_wxpyfw):
    def OnInit(self):
        self.res = wx.xrc.XmlResource('gui\wxPyFw.xrc')
        self.init_frame()
        return True

    def init_frame(self):
        try :
            self.frame = self.res.LoadFrame(None, 'main_frame')
            self.frame.panel = wx.xrc.XRCCTRL(self.frame, 'main_panel')
            
            self.sizer = wx.BoxSizer( wx.VERTICAL )
            self.sizer.Add( self.frame.panel, 1, wx.EXPAND | wx.ALL, 0 )
            self.frame.SetSizer( self.sizer )

            #self.init_menubar()
            
            controller_wxpyfw.__init__(self)
            
            self.frame.Layout()
            self.frame.Show()
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack())) 
    
    def init_menubar(self):
        self.menuBar = self.res.LoadMenuBar("MenuBar")
        self.frame.Bind(wx.EVT_MENU, self.client_list, id=wx.xrc.XRCID("m_clientlist"))
        #self.frame.SetMenuBar(self.menuBar)
    
        