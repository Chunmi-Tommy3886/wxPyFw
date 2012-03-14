# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$14-mar-2012 21.22.18$"
__all__ = [ "_WIDGET_", "_LOGGER_" ]


from obj_cfg import o_cfg
from obj_log import o_log

_WIDGET_ = o_cfg("widget/wx_widget.ini")
_LOGGER_ = o_log("wxPyFw.log")