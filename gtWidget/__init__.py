# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$22-mar-2012 11.24.18$"


import wx

import xml.dom

class gtWidget:
    def __init__(self, app, xgt):
        self.app = app
        self.xgt = xgt
        
        self.CreateWindow()
    
    def ParseXGT(self):
        self.parsed = xml.dom.minidom.parse(self.xgt)
    
    def GetAttribute(self, object):
        result = {
            "id"    : wx.NewId(),
            "parent": None,
        }
        if len(object.getElementsByTagName('id')) > 1 :
            result["id"] = int(object.getElementsByTagName('id')[0].firstChild.nodeValue)
            
        if len(object.getElementsByTagName('parent')) > 1 :
            result["parent"] = int(object.getElementsByTagName('parent')[0].firstChild.nodeValue)
            
        if len(object.getElementsByTagName('style')) > 1 :
            result["style"] = eval(object.getElementsByTagName('style')[0].firstChild.nodeValue)

        if len(object.getElementsByTagName('size')) > 1 :
            result["size"] = eval(object.getElementsByTagName('size')[0].firstChild.nodeValue)

        if len(object.getElementsByTagName('title')) > 1 :
            result["title"] = object.getElementsByTagName('tile')[0].firstChild.nodeValue
            
        if len(object.getElementsByTagName('flag')) > 1 :
            result["flag"] = eval(object.getElementsByTagName('flag')[0].firstChild.nodeValue)
            
        return result
    
    def GetFrame(self, name=None):
        
        frame = None
        frames = self.parsed.getElementsByTagName('frame')
        
        if name is not None :
            for n in frames :
                if frames[n].getAttribute('name') == name :
                    frame = frames[n]
        else :
            frame = frames[n]
        
        if frame is not None :
            return wx.Frame(**self.GetAttribute())
  
  
    def CreateWindow(self):
        frame = self.GetFrame()