# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.30.02$"

import os

from widget import *

class model_wxpyfw:
    def __init__(self):
        pass
    
    def widget(self):
        widget = widgets()
        widget.get_widget()
        return widget.widgets
            
    def list_dir_file(self):
        dirfile = {}
        for dirname, dirnames, filenames in os.walk('.'):
            
            if dirname not in dirfile :
                dirfile[dirname] = {}
                
            for subdirname in dirnames:
                if subdirname not  in dirfile[dirname] :
                    dirfile[dirname][subdirname] = list()
                
                #print os.path.join(dirname, subdirname)
            #for filename in filenames:
            #    if filename not in dirfile[dirname] :
            #        dirfile[dirname].append(filename)
                #print os.path.join(dirname, filename)
        
        return dirfile
        
