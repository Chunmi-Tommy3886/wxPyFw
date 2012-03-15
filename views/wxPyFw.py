__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"


import os
import wx
import sys
import wx.xrc
import wx.aui
import traceback

from widget import *

from globals import *

logger = _LOGGER_

class view_wxpyfw():
    def __init__(self):
        
        self.files = {}
        
        self.projects = self.get_projects()

        self.panel = self.frame.panel
        
        self.panel_left = wx.xrc.XRCCTRL(self.panel, 'panel_left')

        self.panel_right = wx.xrc.XRCCTRL(self.panel, 'panel_right')
        
        self.create_treectrl()
        
        self.create_notebook_widget()
        
        self.create_notebook_files()
        
        print self.files
        
    def OpenFile(self, event):
        if self.treectrl.GetItemText(self.treectrl.GetItemParent(event.GetItem())) not in self.projects :
            files = self.files[self.treectrl.GetItemText(self.treectrl.GetItemParent(event.GetItem()))][self.treectrl.GetItemText(event.GetItem())]
        else :
            files = self.files[self.treectrl.GetItemText(event.GetItem())]
        
        panel = wx.Panel( self.notebook_files, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer( wx.VERTICAL )
        input = wx.TextCtrl( panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        input.LoadFile(files)
	sizer.Add( input, 1, wx.ALL|wx.EXPAND, 0 )
        
        sizer.Layout()
        panel.SetSizer( sizer )
        panel.Layout()
        sizer.Fit( panel )
        
        self.notebook_files.AddPage( panel, self.treectrl.GetItemText(event.GetItem()), True, wx.NullBitmap )
        
    
    def create_treectrl(self):
        try :
            self.treectrl = wx.xrc.XRCCTRL(self.panel_left, "project_tree")
            self.treectrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OpenFile)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
        else :
            try :
                self.treectrl_il = wx.ImageList(16,16)
                self.treectrl.AssignImageList(self.treectrl_il)

                prj_py = self.treectrl_il.Add(wx.Bitmap( "images/16x16/python.png", wx.BITMAP_TYPE_ANY ))
                
                root = self.treectrl.AddRoot("Progetti")

            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
            
            try :
                for project in self.projects :
                    newItem = self.treectrl.AppendItem(root, project)
                    
                    self.treectrl.SetItemImage(newItem, prj_py, wx.TreeItemIcon_Normal)
                    tree_data = self.list_dir_file(self.projects[project]["path"], eval(self.projects[project]["show_hidden"]))
                    
                    self.popolate_treectrl(newItem, tree_data, True)

                    if eval(self.projects[project]["last"]):
                        self.treectrl.SetItemBold(newItem, eval(self.projects[project]["last"]))
                        self.treectrl.Expand(newItem)
                    else :
                        self.treectrl.Collapse(newItem)
                        self.treectrl.CollapseAllChildren(newItem)
            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
                
    
    def popolate_treectrl(self, parent, trees, project=False):
        py = self.treectrl_il.Add(wx.Bitmap( "images/16x16/py.png", wx.BITMAP_TYPE_ANY ))
                
        folder = self.treectrl_il.Add(wx.Bitmap( "images/16x16/folder.png", wx.BITMAP_TYPE_ANY ))
        
        try :
            for item in trees:
                if type(item) == str:
                    newItem = self.treectrl.AppendItem(parent, os.path.basename(item))
                    self.treectrl.SetItemImage(newItem, py, wx.TreeItemIcon_Normal)
                    
                    if not project :
                        self.files[self.treectrl.GetItemText(parent)][os.path.basename(item)] = item
                    else :
                        self.files[os.path.basename(item)] = item
                else:
                    newItem = self.treectrl.AppendItem(parent, item[0])
                    self.files[item[0]] = dict()
                    self.treectrl.SetItemImage(newItem, folder, wx.TreeItemIcon_Normal)
                    if len(item)> 1 :
                        self.popolate_treectrl(newItem, item[1])
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))            
    
    def create_notebook_widget(self):
        try :
            self.notebook_widget = wx.xrc.XRCCTRL(self.panel, "widget_notebook")
            self.notebook_widget.DeleteAllPages()
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
        
        else :
            try :
                self.popolate_notebook_widget(self.widget())
            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
        
    def popolate_notebook_widget(self, widget):
        notebook_icons = wx.ImageList(16, 16)
        self.notebook_widget.AssignImageList( notebook_icons )
        
        x = 0
        for inifile in widget :
            for tabs in widget[inifile] :
                if tabs not in ["Default"] :
                    panel = wx.Panel( self.notebook_widget, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
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

                    self.notebook_widget.AddPage(panel, tabs, False )
                    
                    if "icon" in widget[inifile][tabs] :
                        notebook_icons.Add( wx.Bitmap( "images/%s/%s" % (widget[inifile]["Default"]["icons"], widget[inifile][tabs]["icon"]), wx.BITMAP_TYPE_ANY ))
                        self.notebook_widget.SetPageImage( x, x)
                    x += 1

    
    def create_notebook_files(self):
        self.notebook_files = wx.aui.AuiNotebook( self.panel_right, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_BOTTOM|wx.aui.AUI_NB_CLOSE_ON_ALL_TABS|wx.aui.AUI_NB_DEFAULT_STYLE|wx.aui.AUI_NB_SCROLL_BUTTONS|wx.aui.AUI_NB_TAB_MOVE|wx.aui.AUI_NB_WINDOWLIST_BUTTON )
        self.panel_right.GetSizer().Add( self.notebook_files, 1, wx.EXPAND |wx.ALL, 0 )
        self.panel_right.Layout()
        self.panel_right.GetSizer().Fit( self.panel_right )