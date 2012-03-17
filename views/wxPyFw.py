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

TABS = {}

class create_text_editor :
    def __init__(self, panel, file):
        
        self.panel = panel
        self.file = file
        self.notebook_files = self.panel.GetParent()
        
        try :
            self.text_editor = code_editor(panel)
            self.text_editor.LoadFile(file)
            self.text_editor.EmptyUndoBuffer()

            self.text_editor.Bind(wx.EVT_KEY_DOWN, self.SetModifiedFile)

            # line numbers in the margin
            self.text_editor.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
            self.text_editor.SetMarginWidth(1, 25)
            self.text_editor.SetSTCFocus(True)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
        else :
            self.notebook_files.Bind(wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.CloseFile)
            
    def SetModifiedFile(self, event):
        idx = self.notebook_files.GetSelection()
        file = TABS[idx]

        if not file["modified"] :
#            file["modified"] = True
            self.notebook_files.SetPageText(idx, "* %s" % file["file"])
            #self.notebook_files.SetPageText(self.notebook_files.GetSelection(), "* %s" % self.notebook_files.GetPageText(self.notebook_files.GetSelection()))
        
        self.text_editor.onKeyPressed(event)
    
    def CloseFile(self, event):
        idx = self.notebook_files.GetSelection()
        file = TABS[idx]
        
        if file["modified"] :
            if(wx.MessageBox("File %s is modified. Save It?" % file["file"], "Save...", wx.YES_NO | wx.YES_DEFAULT, self.notebook_files)==wx.YES) :
                wx.BeginBusyCursor()
                
                try :
                    file["object"].text_editor.SaveFile(file["path"])
                except :
                    logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
                    
                else :
                    TABS.pop(idx)

                    self.notebook_files.DeletePage(idx)
                    event.Veto()

                wx.EndBusyCursor()

class wxpyfw_actions :
    def ToggleComment(self, event):
        idx = self.notebook_files.GetSelection()
        file = TABS[idx]
        lines = []
        if file["object"].text_editor.GetSelectionStart() == file["object"].text_editor.GetSelectionEnd() :
            lines.append(file["object"].text_editor.GetCurrentLine())
        else :
            for pos in range(file["object"].text_editor.GetSelectionStart(), file["object"].text_editor.GetSelectionEnd()) :
                if file["object"].text_editor.LineFromPosition(pos) not in lines :
                    lines.append(file["object"].text_editor.LineFromPosition(pos))
        for line in lines :
            file["object"].text_editor.GotoLine(line)
            
            file["object"].text_editor.Home()
            if file["object"].text_editor.GetCharAt(file["object"].text_editor.GetCurrentPos()) == 35 :
                file["object"].text_editor.CharRight()
                file["object"].text_editor.DeleteBack()
            else :
                file["object"].text_editor.AddText('#')
        lines = []
    
    def DeleteLine(self, event):
        idx = self.notebook_files.GetSelection()
        file = TABS[idx]
        file["object"].text_editor.LineDelete()

    def DuplicateUp(self, event):
        idx = self.notebook_files.GetSelection()
        file = TABS[idx]
        file["object"].text_editor.LineDuplicate()
    
    def DuplicateDw(self, event):
        idx = self.notebook_files.GetSelection()
        file = TABS[idx]
        file["object"].text_editor.LineDuplicate()
        file["object"].text_editor.LineDown()
        
        
    def OnOpen(self, event):
        filename = self.treectrl.GetItemText(event.GetItem())
        
        if self.treectrl.GetItemText(self.treectrl.GetItemParent(event.GetItem())) not in self.projects :
            path = self.files[self.treectrl.GetItemText(self.treectrl.GetItemParent(event.GetItem()))][filename]
        else :
            path = self.files[filename]
        
        if path not in TABS :
            panel = wx.Panel( self.notebook_files, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
            sizer = wx.BoxSizer( wx.VERTICAL )
            
            object = create_text_editor(panel, path)

            sizer.Add( object.text_editor , 1, wx.ALL|wx.EXPAND, 0 )

            sizer.Layout()
            panel.SetSizer( sizer )
            panel.Layout()
            sizer.Fit( panel )

            self.notebook_files.AddPage( panel, filename, True, wx.NullBitmap )

            TABS[self.notebook_files.GetSelection()] = {
                'path'  :   path,
                'file'  :   filename,
                'path'  :   path,
                'panel' :   panel,
                'sizer' :   sizer,
                'object' :   object,
                'modified':   False
            }
        else :
            self.notebook_files.SetSelection(TABS[path]["idx"])
    
            
class view_wxpyfw(wxpyfw_actions):
    def __init__(self):
        
        self.files = {}
        
        self.projects = self.get_projects()

        self.panel = self.frame.panel
        
        self.panel_left = wx.xrc.XRCCTRL(self.panel, 'panel_left')

        self.panel_right = wx.xrc.XRCCTRL(self.panel, 'panel_right')
        
        self.create_menubar()
        
        self.create_treectrl()
        
        self.create_notebook_widget()
        
        self.create_notebook_files()
    
    def create_menubar(self):
        #self.menuBar = self.res.LoadMenuBar("MenuBar")
        self.menuBar = self.frame.GetMenuBar()
        
        self.frame.Bind(wx.EVT_MENU, self.ToggleComment, id=wx.xrc.XRCID("comment"))
        self.frame.Bind(wx.EVT_MENU, self.DeleteLine, id=wx.xrc.XRCID("delete_line"))
        self.frame.Bind(wx.EVT_MENU, self.DuplicateUp, id=wx.xrc.XRCID("duplicate_up"))
        self.frame.Bind(wx.EVT_MENU, self.DuplicateDw, id=wx.xrc.XRCID("duplicate_dw"))
        
         #self.frame.SetMenuBar(self.menuBar)

    def create_treectrl(self):
        try :
            self.treectrl = wx.xrc.XRCCTRL(self.panel_left, "project_tree")
            self.treectrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnOpen)
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
        self.notebook_files = wx.lib.agw.aui.AuiNotebook( self.panel_right, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_CLOSE_ON_ALL_TABS|wx.aui.AUI_NB_DEFAULT_STYLE|wx.aui.AUI_NB_SCROLL_BUTTONS|wx.aui.AUI_NB_TAB_MOVE|wx.aui.AUI_NB_WINDOWLIST_BUTTON )
        self.panel_right.GetSizer().Add( self.notebook_files, 1, wx.EXPAND |wx.ALL, 0 )
        self.panel_right.Layout()
        self.panel_right.GetSizer().Fit( self.panel_right )