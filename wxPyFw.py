# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 20.03.26$"


import wx
import sys

reload(sys)
sys.setdefaultencoding("latin-1")
del sys.setdefaultencoding

from controllers import window

if __name__ == '__main__':
    app = window(False)
    app.MainLoop()
