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
        projects = o_cfg("publics/projects.ini")
        return projects.configfile
    
    def list_file_dir(self, path, hidden=False) :
        result = list()
    
        for dirname in os.listdir(path) :

            if os.path.isdir(os.path.join(path, dirname)) :
                if dirname[0:1] != "." or hidden :
                    result.append( [ dirname, self.list_file_dir(os.path.join(path, dirname), hidden) ] )
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
            

