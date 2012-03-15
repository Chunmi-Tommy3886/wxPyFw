__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"


import os
import wx
import sys
import wx.xrc
import traceback

from widget import *

from globals import *

logger = _LOGGER_

PROJECT_NAME = "PROJECT NAME"

class view_wxpyfw():
    def __init__(self):
        
        self.panel = self.frame.panel
        
        #self.popolate_treectrl()
        
        self.popolate_widget_ctrl()
    
    def popolate_widget_ctrl(self):
        try :
            self.notebook = wx.xrc.XRCCTRL(self.panel, "widget_notebook")
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
        
        else :
            try :
                widget = self.widget()
                for obj in widget :
                    self.notebook.AddPage( self.create_notebook_panel(widget[obj]), widget[obj]["Default"]["name"], False )
                    
            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
        
    def create_notebook_panel(self, widget):
        panel = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer( wx.VERTICAL )
        toolbar = wx.ToolBar( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
        
        for tools in widget :
            print tools, widget[tools]
            if tools not in ["Default"] :
                if "image" in widget[tools] :
                    icon = wx.Bitmap( "images/%s/%s" % (widget["Default"]["icons"], widget[tools]["image"]), wx.BITMAP_TYPE_ANY )
                elif os.path.isfile("images/%s/%s.xpm" % (widget["Default"]["icons"], tools)) :
                    icon = wx.Bitmap( "images/%s/%s.xpm" % (widget["Default"]["icons"], tools), wx.BITMAP_TYPE_ANY )
                else :
                    icon = wx.Bitmap( "images/%s/custom.xpm" % (widget["Default"]["icons"]), wx.BITMAP_TYPE_ANY )
                        
                toolbar.AddLabelTool( wx.ID_ANY, tools, icon , wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        
        toolbar.Realize() 
        sizer.Add( toolbar, 0, wx.EXPAND, 5 )
        
        panel.SetSizer( sizer )
        panel.Layout()
        sizer.Fit( panel )
        
        return panel
    
        
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
            
