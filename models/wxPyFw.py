# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"

import os

from widget import *
from globals.obj_cfg import o_cfg


class model_wxpyfw:
    def widget(self):
        widget = widgets()
        widget.get_widget()
        return widget.widgets
    
    def get_projects(self):
        projects = o_cfg("projects.ini")
        return projects.configfile
        
        
    def list_dir_file(self, path, show_hidden=False):
        
        list_dir_files = list()
        
        for dirname in os.listdir(path) :
            if os.path.isdir(dirname) :
                if dirname[0:1] != "." or show_hidden :
                    #print os.path.join(path, dirname)
                    list_dir_files.append( [ dirname, self.list_dir_file(os.path.join(path, dirname), show_hidden)])
                    
            #print os.path.isfile(dirname)
            if os.path.isfile(dirname) :
                list_dir_files.append(dirname)
        
#        
#        for dirname, dirnames, filenames in os.walk(path):
#            #print dirname, filenames 
#            #if show_hidden :
#            #    if dirname[::-1] != "."
#            #    list_dir_files[dirname] = filenames
#            list_dir_files[dirname] = filenames
#            #for filename in filenames :
#            #    list_dir_files.append(dirname)
#        
        #print list_dir_files
#        
#        dirfile = {}
#        print self.GetItemPyData(item2)
#        for dirname, dirnames, filenames in os.walk(path):
#            if dirname not in dirfile :
#                dirfile[dirname] = {}
#                
#            for subdirname in dirnames:
#                if subdirname not  in dirfile[dirname] :
#                    dirfile[dirname][subdirname] = list()
#                
#                #print os.path.join(dirname, subdirname)
#            #for filename in filenames:
#            #    if filename not in dirfile[dirname] :
#            #        dirfile[dirname].append(filename)
#                #print os.path.join(dirname, filename)
#        
        list_dir_files.sort( key=mixed_order )
        
        return list_dir_files
    
def mixed_order( a ):
    if type(a) == str :
        return True
    else:
        return False
            

