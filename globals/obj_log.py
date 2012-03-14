# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.50.06$"
__all__ = ["obj_log"]

import time
import os.path

def joinlist(string, list):
    return str(string).join(list)

class obj_log :
    def __init__(self, log_file):
        self.logfile = log_file
        
    def write(self, string, content="NOTICE", object=None) :
        """
        Funzione che logga le diverse azioni.
        """
        log_file=open('./%s' % self.logfile, 'a')
        data = time.strftime("%d/%m/%Y %H:%M:%S")

        str_out = str(string).replace("\n", " ")
        str_out = str(str_out).replace("\t", " ")

        if(object is not None) :
            log_file.write("%s [%s][%s]: %s \n" % (data, content, (object[0].__class__, os.path.basename(object[1][-1][0]), object[1][-1][1]), str_out ) )
        else :
            log_file.write("%s [%s][%s]: %s \n" % (data, content, '', str_out))

        log_file.close()