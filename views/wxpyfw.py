__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"

import os
import wx
import sys
import wx.stc
import wx.xrc
import wx.aui
import wx.wizard
import traceback
import wx.lib.agw.aui

from widget import *

from globals import *

from publics import *

from views.editor import code_editor

TAB = list()

Icons = {
    '16'    :   {
        'list'      :   wx.ImageList(16,16)
    },
    'nb'    :   {
        'list'      :   wx.ImageList(16,16)
    },
    '32'    :   {
        'list'      :   wx.ImageList(32,32),
    }
}

Icons["16"].update({
    'folder'    :   Icons["16"]["list"].Add(wx.Bitmap("images/16x16/folder.png", wx.BITMAP_TYPE_ANY)),
    'project'   :   Icons["16"]["list"].Add(wx.Bitmap("images/16x16/python.png", wx.BITMAP_TYPE_ANY)),
    '.py'       :   Icons["16"]["list"].Add(wx.Bitmap("images/16x16/py.png", wx.BITMAP_TYPE_ANY)),
    '.ini'      :   Icons["16"]["list"].Add(wx.Bitmap("images/16x16/ini.png", wx.BITMAP_TYPE_ANY)),
    '*'         :   Icons["16"]["list"].Add(wx.Bitmap("images/16x16/file.png", wx.BITMAP_TYPE_ANY))
})
Icons["32"].update({
    'empty_project'   :   Icons["32"]["list"].Add(wx.Bitmap("images/32x32/python.png", wx.BITMAP_TYPE_ANY)),
    'mvc_project'   :   Icons["32"]["list"].Add(wx.Bitmap("images/32x32/package.png", wx.BITMAP_TYPE_ANY)),
    'python_file'  :   Icons["32"]["list"].Add(wx.Bitmap("images/32x32/py.png", wx.BITMAP_TYPE_ANY)),
    'empty_file'  :   Icons["32"]["list"].Add(wx.Bitmap("images/32x32/new_file.png", wx.BITMAP_TYPE_ANY)),
})

class create_text_editor :
    def __init__(self, window, panel, file):
        
        self.panel = panel
        self.file = file
        self.notebook_files = window.notebook_files
        self.treectrl = window.treectrl
        
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
        file = TAB[idx]

        if not file["modified"] :
            file["modified"] = file["object"].text_editor.GetModify()
            if file["object"].text_editor.GetModify() :
                self.notebook_files.SetPageText(idx, "* %s" % file["name"])
                #self.notebook_files.SetPageText(self.notebook_files.GetSelection(), "* %s" % self.notebook_files.GetPageText(self.notebook_files.GetSelection()))
        
        self.text_editor.onKeyPressed(event)
    
    def CloseFile(self, event):
        idx = self.notebook_files.GetSelection()
        file = TAB[idx]
        
        if file["object"].text_editor.GetModify() :
            if(wx.MessageBox("File %s is modified. Save It?" % file["name"], "Save...", wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT, self.notebook_files)==wx.YES) :
                wx.BeginBusyCursor()
                
                try :
                    file["object"].text_editor.SaveFile(file["path"])
                except :
                    logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
                    
                else :
                    info = self.treectrl.GetItemPyData(TAB[idx]["item"])
                    info["idx"] = None
                    
                    self.treectrl.SetItemPyData(TAB[idx]["item"], info)
                    
                    del TAB[idx]

                    self.notebook_files.DeletePage(idx)
                    
                    event.Veto()

                wx.EndBusyCursor()
    
class wxpyfw_actions :
    def LoadOptions(self, event):
        self.window.LoadController('options')
        
    def ToggleComment(self, event):
        idx = self.notebook_files.GetSelection()
        file = TAB[idx]
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
        file = TAB[idx]
        file["object"].text_editor.LineDelete()
        
    def CutLine(self, event):
        idx = self.notebook_files.GetSelection()
        file = TAB[idx]
        
        if file["object"].text_editor.GetSelectionStart() == file["object"].text_editor.GetSelectionEnd() :
            file["object"].text_editor.LineCut()
        else :
            file["object"].text_editor.Cut()

    def CopyLine(self, event):
        idx = self.notebook_files.GetSelection()
        file = TAB[idx]
        
        if file["object"].text_editor.GetSelectionStart() == file["object"].text_editor.GetSelectionEnd() :
            file["object"].text_editor.LineCopy()
        else :
            file["object"].text_editor.Copy()
    
    def PasteLine(self, event):
        idx = self.notebook_files.GetSelection()
        file = TAB[idx]
        file["object"].text_editor.Paste()
            
    def DuplicateUp(self, event):
        idx = self.notebook_files.GetSelection()
        file = TAB[idx]
        file["object"].text_editor.LineDuplicate()
    
    def DuplicateDw(self, event):
        idx = self.notebook_files.GetSelection()
        file = TAB[idx]
        file["object"].text_editor.LineDuplicate()
        file["object"].text_editor.LineDown()
        
    def OpenFile(self, event,):
        select = self.treectrl.GetItemPyData(self.treectrl.GetSelections()[0])
        
        if select["idx"] is None and select["type"] == "File":
            panel = wx.Panel( self.notebook_files, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
            sizer = wx.BoxSizer( wx.VERTICAL )

            object = create_text_editor(self, panel, select["path"])

            sizer.Add( object.text_editor , 1, wx.ALL|wx.EXPAND, 0 )

            sizer.Layout()
            panel.SetSizer( sizer )
            panel.Layout()
            sizer.Fit( panel )

            self.notebook_files.AddPage( panel, os.path.basename(select["path"]), True, wx.NullBitmap )
            
            select["idx"] = self.notebook_files.GetSelection()
            
            TAB.append({
                'name'  :   select["name"],
                'path'  :   select["path"],
                'item'  :   select["item"],
                'panel' :   panel,
                'sizer' :   sizer,
                'object' :  object,
                'modified'  : False
            })
                                    
            self.treectrl.SetItemPyData(self.treectrl.GetSelections()[0], select)
        else :
            self.notebook_files.SetSelection(select["idx"])
        
    def SaveFile(self, event):
        idx = self.notebook_files.GetSelection()
        file = TAB[idx]
        
        wx.BeginBusyCursor()
        try :
            file["object"].text_editor.SaveFile(file["path"])
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
        else :
            self.notebook_files.SetPageText(idx, "%s" % file["name"])

        wx.EndBusyCursor()
        
    def SetMain(self, event):
        select = self.treectrl.GetItemPyData(self.treectrl.GetSelections()[0])
        for project in self.projects :
            self.projects[project]["main"] = False

        self.projects[select["name"]]["main"] = True
                    
        self.projects.write()
        
        self.treectrl.SetItemBold(select["item"], True)

        #self.treectrl.CollapseAllChildren(self.treectrl.GetRootItem())
                
        self.treectrl.UnselectAll()
                
        self.treectrl.Expand(select["item"])

        self.treectrl.SelectItem(select["item"], True)
        
    def UnsetMain(self, event):
        select = self.treectrl.GetItemPyData(self.treectrl.GetSelections()[0])
        
        self.projects[select["name"]]["main"] = False
                    
        self.projects.write()
    
    def NewProject(self, event):
        try :
            wizard = self.window.res.LoadObject(None, 'new_project', 'wxWizard')

            page1 = wx.xrc.XRCCTRL(wizard, 'FirstPage')
    
            listctrl = wx.xrc.XRCCTRL(wizard, 'listctrl')
            listctrl.AssignImageList(Icons["32"]["list"], wx.IMAGE_LIST_NORMAL)
            listctrl.InsertImageStringItem(0, "Empty Project", Icons["32"]["empty_project"])
            listctrl.InsertImageStringItem(1, "MVC Project", Icons["32"]["mvc_project"])
            listctrl.InsertImageStringItem(2, "Python File", Icons["32"]["python_file"])
            listctrl.InsertImageStringItem(3, "Empty File", Icons["32"]["empty_file"])

            wx.xrc.XRCCTRL(wizard, 'path').SetPath(Directory["default"])
            
            wizard.RunWizard(page1)
            
            wizard.Destroy()
            
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
        
        try :
            name = wx.xrc.XRCCTRL(wizard, 'project_name').GetValue()
            path = os.path.join(wx.xrc.XRCCTRL(wizard, 'path').GetPath(), wx.xrc.XRCCTRL(wizard, 'project_name').GetValue())
            open = wx.xrc.XRCCTRL(wizard, 'opener').IsChecked()
            main = wx.xrc.XRCCTRL(wizard, 'set_main').IsChecked()

            if wx.xrc.XRCCTRL(wizard, 'create_dir').IsChecked():
                if not os.path.exists(path) :
                    os.makedirs(path)
                    
            newItem = self.treectrl.AppendItem(self.treectrl.GetRootItem(), name)
            self.treectrl.SetItemPyData(newItem, {'item' : newItem, 'path' : path,  'name' : name, 'idx' : None, "type" : "Project"} )
            self.treectrl.SetItemImage(newItem, Icons["16"]["project"], wx.TreeItemIcon_Normal)
            
            tree_data = self.list_file_dir(path, False)
            
            self.popolate_treectrl(newItem, tree_data, True)

            if main:
                for project in self.projects :
                    self.projects[project]["main"] = False
                    
                self.projects.write()
                
                self.treectrl.SetItemBold(newItem, True)
                    
            if open :
                #self.treectrl.CollapseAllChildren(self.treectrl.GetRootItem())
                
                self.treectrl.UnselectAll()
                
                self.treectrl.Expand(newItem)

                self.treectrl.SelectItem(newItem, True)
            
            else :
                self.treectrl.Collapse(newItem)
                self.treectrl.CollapseAllChildren(newItem)
                
            self.CreateProject(name, path, open, main)

        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
    
    def NewFile(self, event):
        select = self.treectrl.GetItemPyData(self.treectrl.GetSelections()[0])
        
        wildcard = "Python source (*.py)|*.py|" \
                    "Configuration File (*.ini)|*.ini|" \
                    "Other files (*.*)|*.*"
        try :
            self.dialog = wx.FileDialog(None, "Save File a file", select["path"],  "", wildcard , wx.SAVE)
            if self.dialog.ShowModal() == wx.ID_OK:
                
                f = open(self.dialog.GetPath(), 'a')
                f.close()
                
                newItem = self.treectrl.AppendItem(select["item"], os.path.basename(self.dialog.GetPath()))
                self.treectrl.SetItemPyData(newItem, {'item' : newItem, 'path' : self.dialog.GetPath(),  'name' : os.path.basename(self.dialog.GetPath()), 'idx' : None, "type" : "File"} )

                name, ext = os.path.splitext(self.dialog.GetPath())
                if ext not in Icons["16"] :
                    self.treectrl.SetItemImage(newItem, Icons["16"]["*"], wx.TreeItemIcon_Normal)
                else :
                    self.treectrl.SetItemImage(newItem, Icons["16"][ext], wx.TreeItemIcon_Normal)
                
                #self.refresh_treectrl(select["path"])
                
                self.treectrl.SelectItem(newItem)
                self.OpenFile(None)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
            
    def NewFolder(self, event):
        select = self.treectrl.GetItemPyData(self.treectrl.GetSelections()[0])
        try :
            self.dialog = wx.DirDialog(None, "Directory", select["path"], wx.SAVE)
            if self.dialog.ShowModal() == wx.ID_OK:
#                
#                f = open(self.dialog.GetPath(), 'a')
#                f.close()
#                
                newItem = self.treectrl.AppendItem(select["item"], os.path.basename(self.dialog.GetPath()))
                self.treectrl.SetItemPyData(newItem, {'item' : newItem, 'path' : self.dialog.GetPath(),  'name' : os.path.basename(self.dialog.GetPath()), 'idx' : None, "type" : "Folder"} )
#
#                name, ext = os.path.splitext(self.dialog.GetPath())
#                if ext not in Icons["16"] :
#                    self.treectrl.SetItemImage(newItem, Icons["16"]["*"], wx.TreeItemIcon_Normal)
#                else :
                self.treectrl.SetItemImage(newItem, Icons["16"]["folder"], wx.TreeItemIcon_Normal)
#                
#                #self.refresh_treectrl(select["path"])
#                
                self.treectrl.SelectItem(newItem)
#                self.OpenFile(None)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
        
    
    def OpenMenu(self, event):
        select = self.treectrl.GetItemPyData(event.GetItem())
        self.treectrl.SelectItem(event.GetItem(), True)
        
        try :
            menu = self.res.LoadMenu("menu_tree")
            
            if select["type"] == "File" :
                menu.Remove(wx.xrc.XRCID("set_main"))
                menu.Remove(wx.xrc.XRCID("unset_main"))
                menu.Remove(wx.xrc.XRCID("tree_find"))
                menu.Remove(wx.xrc.XRCID("tree_paste"))
                
                #menu.Remove(wx.xrc.XRCID("sep3"))
                #menu.Remove(wx.xrc.XRCID("sep4"))
                
                menu.Bind(wx.EVT_MENU, self.OpenFile, id=wx.xrc.XRCID("tree_open"))
                menu.Bind(wx.EVT_MENU, self.CutFile, id=wx.xrc.XRCID("tree_cut"))
                menu.Bind(wx.EVT_MENU, self.CopyFile, id=wx.xrc.XRCID("tree_copy"))
                #wx.xrc.XRCID("open").Enabled(False)
            elif select["type"] == "Folder" :
                #wx.xrc.XRCID("insert").Enabled(False)
                menu.Remove(wx.xrc.XRCID("set_main"))
                menu.Remove(wx.xrc.XRCID("unset_main"))
                menu.Remove(wx.xrc.XRCID("tree_open"))
                
                menu.Bind(wx.EVT_MENU, self.NewFile, id=wx.xrc.XRCID("new_file"))
                menu.Bind(wx.EVT_MENU, self.NewFolder, id=wx.xrc.XRCID("new_folder"))
                menu.Bind(wx.EVT_MENU, self.PasteFile, id=wx.xrc.XRCID("tree_paste"))
            else :
                menu.Remove(wx.xrc.XRCID("tree_cut"))
                menu.Remove(wx.xrc.XRCID("tree_copy"))
                menu.Remove(wx.xrc.XRCID("tree_open"))
                
                menu.Bind(wx.EVT_MENU, self.SetMain, id=wx.xrc.XRCID("set_main"))
                menu.Bind(wx.EVT_MENU, self.UnsetMain, id=wx.xrc.XRCID("unset_main"))
                
                menu.Bind(wx.EVT_MENU, self.NewFile, id=wx.xrc.XRCID("new_file"))
                menu.Bind(wx.EVT_MENU, self.NewFolder, id=wx.xrc.XRCID("new_folder"))
                menu.Bind(wx.EVT_MENU, self.PasteFile, id=wx.xrc.XRCID("tree_paste"))
                
            menu.Bind(wx.EVT_MENU, self.TreeDelete, id=wx.xrc.XRCID("tree_delete"))

        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
        else :
            x,y = event.GetPoint()
            self.frame.PopupMenu( menu, wx.Point(x - 10, y + 45))
    
            
class view_wxpyfw(wxpyfw_actions):
    def __init__(self):
    
        self.files = {}
        
        self.projects = self.get_projects()

        self.panel_left = wx.xrc.XRCCTRL(self.panel, 'panel_left')

        self.panel_right = wx.xrc.XRCCTRL(self.panel, 'panel_right')
        
        self.create_menubar()
        
        self.create_treectrl()
        
        self.create_notebook_widget()
        
        self.create_notebook_files()
    
    def create_menubar(self):
        #self.menuBar = self.res.LoadMenuBar("MenuBar")
        self.menuBar = self.frame.GetMenuBar()
        
        self.frame.Bind(wx.EVT_MENU, self.NewProject, id=wx.xrc.XRCID("new_project"))
        self.frame.Bind(wx.EVT_MENU, self.SaveFile, id=wx.xrc.XRCID("save"))


        self.frame.Bind(wx.EVT_MENU, self.CutLine, id=wx.xrc.XRCID("cut"))
        self.frame.Bind(wx.EVT_MENU, self.CopyLine, id=wx.xrc.XRCID("copy"))
        self.frame.Bind(wx.EVT_MENU, self.PasteLine, id=wx.xrc.XRCID("paste"))
        self.frame.Bind(wx.EVT_MENU, self.DeleteLine, id=wx.xrc.XRCID("delete"))

        
        self.frame.Bind(wx.EVT_MENU, self.ToggleComment, id=wx.xrc.XRCID("comment"))
        self.frame.Bind(wx.EVT_MENU, self.DuplicateUp, id=wx.xrc.XRCID("duplicate_up"))
        self.frame.Bind(wx.EVT_MENU, self.DuplicateDw, id=wx.xrc.XRCID("duplicate_dw"))
        
        self.frame.Bind(wx.EVT_MENU, self.LoadOptions, id=wx.xrc.XRCID("options"))
        
         #self.frame.SetMenuBar(self.menuBar)

    def create_treectrl(self):
        try :
            self.treectrl = wx.xrc.XRCCTRL(self.panel_left, "project_tree")
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))    
        else :
            try :
                self.treectrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OpenFile)
                self.treectrl.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OpenMenu)
            
                self.treectrl.AssignImageList(Icons["16"]["list"])
                
                root = self.treectrl.AddRoot("Progetti")

            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
            
            try :
                for project in self.projects :
                    newItem = self.treectrl.AppendItem(root, project)
                    self.treectrl.SetItemPyData(newItem, {'item' : newItem, 'path' : self.projects[project]["path"],  'name' : project, 'idx' : None, "type" : "Project"} )

                    self.treectrl.SetItemImage(newItem, Icons["16"]["project"], wx.TreeItemIcon_Normal)
                    tree_data = self.list_file_dir(self.projects[project]["path"], eval(self.projects[project]["hidden"]))
                    
                    self.popolate_treectrl(newItem, tree_data, True)

                    if eval(self.projects[project]["main"]):
                        self.treectrl.SetItemBold(newItem, eval(self.projects[project]["main"]))
                        self.treectrl.Expand(newItem)
                    else :
                        self.treectrl.Collapse(newItem)
                        self.treectrl.CollapseAllChildren(newItem)
            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
    
    def refresh_treectrl(self, path):
        self.treectrl.DeleteChildren(self.treectrl.GetSelections()[0])
        
        self.popolate_treectrl(self.treectrl.GetSelections()[0], self.list_file_dir(path))
        
    
    def popolate_treectrl(self, parent, trees, project=False):
        try :
            for item in trees :
                if type(item) == str:
                    newItem = self.treectrl.AppendItem(parent, os.path.basename(item))
                    self.treectrl.SetItemPyData(newItem, {'item' : newItem, 'path' : item,  'name' : os.path.basename(item), 'idx' : None, "type" : "File"} )
                    
                    name, ext = os.path.splitext(item)
                    if ext not in Icons["16"] :
                        self.treectrl.SetItemImage(newItem, Icons["16"]["*"], wx.TreeItemIcon_Normal)
                    else :
                        self.treectrl.SetItemImage(newItem, Icons["16"][ext], wx.TreeItemIcon_Normal)
                else:
                    newItem = self.treectrl.AppendItem(parent, os.path.basename(item[0]))
                    self.treectrl.SetItemPyData(newItem, {'item' : newItem, 'path' : item[0],  'name' : os.path.basename(item[0]), 'idx' : None, "type" : "Folder"} )
                    self.treectrl.SetItemImage(newItem, Icons["16"]["folder"], wx.TreeItemIcon_Normal)
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
        self.notebook_widget.AssignImageList( Icons["nb"]["list"] )
        
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
                        Icons["nb"].update({
                            '%s' % (widget[inifile][tabs]["icon"]) : Icons["nb"]["list"].Add( wx.Bitmap( "images/%s/%s" % (widget[inifile]["Default"]["icons"], widget[inifile][tabs]["icon"]), wx.BITMAP_TYPE_ANY ))
                        })
                        self.notebook_widget.SetPageImage( x, Icons["nb"][widget[inifile][tabs]["icon"]])
                    x += 1

    
    def create_notebook_files(self):
        self.notebook_files = wx.lib.agw.aui.AuiNotebook( self.panel_right, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_CLOSE_ON_ALL_TABS|wx.aui.AUI_NB_DEFAULT_STYLE|wx.aui.AUI_NB_SCROLL_BUTTONS|wx.aui.AUI_NB_TAB_MOVE|wx.aui.AUI_NB_WINDOWLIST_BUTTON )
        self.panel_right.GetSizer().Add( self.notebook_files, 1, wx.EXPAND |wx.ALL, 0 )
        self.panel_right.Layout()
        self.panel_right.GetSizer().Fit( self.panel_right )