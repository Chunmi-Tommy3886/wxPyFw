# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$18-mar-2012 23.55.05$"

__all__ = ["Directory"]

from globals.obj_cfg import o_cfg

cfg = o_cfg("publics\config.ini")

Directory = {}

for section in cfg :
    vars()["%s" % (section)]=cfg[section]

