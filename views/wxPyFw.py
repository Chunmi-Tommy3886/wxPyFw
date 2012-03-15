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
            self.notebook.DeleteAllPages()
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
        
        else :
            try :
                self.create_notebook_widget(self.widget())
            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
        
    def create_notebook_widget(self, widget):
        notebook_icons = wx.ImageList(16, 16)
        self.notebook.AssignImageList( notebook_icons )
        
        x = 0
        for inifile in widget :
            for tabs in widget[inifile] :
                if tabs not in ["Default"] :
                    panel = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
                    sizer = wx.BoxSizer( wx.VERTICAL )
                    toolbar = wx.ToolBar( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
                    
                    for tool in widget[inifile][tabs] :
                        
                        if type(widget[inifile][tabs][tool]) is not str :
                            if "icon" in widget[inifile][tabs][tool] :
                                icon = wx.Bitmap( "images/%s/%s" % (widget[inifile]["Default"]["icons"], widget[inifile][tabs][tool]["icon"]), wx.BITMAP_TYPE_ANY )
                            elif os.path.isfile("images/%s/%s.xpm" % (widget[inifile]["Default"]["icons"], tool)) :
                                icon = wx.Bitmap( "images/%s/%s.xpm" % (widget[inifile]["Default"]["icons"], tool), wx.BITMAP_TYPE_ANY )
                            else :
                                icon = wx.Bitmap( "images/%s/custom.xpm" % (widget[inifile]["Default"]["icons"]), wx.BITMAP_TYPE_ANY )

                            label = tool
                            tooltip = statusbar = wx.EmptyString

                            if "label" in widget[inifile][tabs][tool] :
                                label = widget[inifile][tabs][tool]["label"]


                            if "tooltip" in widget[inifile][tabs][tool] :
                                tooltip = widget[inifile][tabs][tool]["tooltip"]

                            if "statusbar" in widget[inifile][tabs][tool] :
                                statusbar = widget[inifile][tabs][tool]["statusbar"]

                            toolbar.AddLabelTool( wx.ID_ANY, label, icon , wx.NullBitmap, wx.ITEM_NORMAL, tooltip, statusbar, None ) 

                            if "separator" in widget[inifile][tabs][tool] :
                                toolbar.AddSeparator()    

                    toolbar.Realize() 
                    sizer.Add( toolbar, 0, wx.EXPAND, 0 )

                    panel.SetSizer( sizer )
                    panel.Layout()
                    sizer.Fit( panel )


                    self.notebook.AddPage(panel, tabs, False )
                    
                    if "icon" in widget[inifile][tabs] :
                        notebook_icons.Add( wx.Bitmap( "images/%s/%s" % (widget[inifile]["Default"]["icons"], widget[inifile][tabs]["icon"]), wx.BITMAP_TYPE_ANY ))
                        self.notebook.SetPageImage( x, x)
                    x += 1

    
        
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

            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
                raise NameError("qui")
            
