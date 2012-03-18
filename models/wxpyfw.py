# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"

import os
import wx
import sys
import traceback

from widget import *

from globals import *

from globals.obj_cfg import o_cfg


logger = _LOGGER_


class model_wxpyfw:    
    
    def CopyFile(self, event):
        print "copy"
    def CutFile(self, event):
        print "cut"
    def PasteFile(self, event):
        print "paste"
    def DeleteFile(self, event):
        select = self.treectrl.GetItemPyData(self.treectrl.GetSelections()[0])
        
        if(wx.MessageBox("Are you sure you want to delete %s?" % select["name"], "Delete...", wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT, self.notebook_files)==wx.YES) :
            wx.BeginBusyCursor()
            
            try :
                #os.remove(select["path"])
                
                print select["item"]
                print self.treectrl.GetItemPyData(self.treectrl.GetItem(self.treectrl.GetItemParent(select["item"])))["path"]
                self.refresh_treectrl(self.treectrl.GetItemPyData(self.treectrl.GetItem(self.treectrl.GetItemParent(select["item"])))["path"])

            except :
                logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
            
            
            wx.EndBusyCursor()

    def widget(self):
        widget = widgets()
        widget.get_widget()
        return widget.widgets
    
    def get_projects(self):
        projects = o_cfg("publics/projects.ini")
        return projects.configfile
    
    def list_file_dir(self, path, hidden=False) :
        result = list()
    
        for dirname in os.listdir(path) :

            if os.path.isdir(os.path.join(path, dirname)) :
                if dirname[0:1] != "." or hidden :
                    result.append( [ os.path.join(path, dirname), self.list_file_dir(os.path.join(path, dirname), hidden) ] )
            elif os.path.isfile(os.path.join(path, dirname)) :
                name, ext = os.path.splitext(os.path.join(path, dirname))
                if ext not in [ ".pyc" ] :
                    if dirname[0:1] != "." or hidden :
                        result.append(os.path.realpath(os.path.join(path, dirname)))

        result.sort()
        result.sort( key=mixed_order )

        return result
    
def mixed_order( a ):
    if type(a) == str :
        return True
    else:
        return False
            

