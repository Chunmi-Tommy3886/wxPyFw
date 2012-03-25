# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$16-mar-2012 15.03.06$"

# styled text using wxPython's
# wx.StyledTextCtrl(parent, id, pos, size, style, name)
# set up for folding and Python code highlighting
# source: Dietrich  16NOV2008

import wx
import os
import sys
import wx.stc
import keyword
import traceback

from globals.obj_cfg import o_cfg
from globals import *

syntax = o_cfg("publics\syntax.ini")

shortcuts = o_cfg("publics\shortcuts.ini")

if wx.Platform == '__WXMSW__':
    # for windows OS
    faces = syntax["Windows"]
else:
    faces = syntax["Other"]

EXT2LAN = {
    ".py"   :   "Python",
    ".xrc"   :   "XRC",
    ".xgt"   :   "XML"
}
  
LANGUAGES = {
                'container':wx.stc.STC_LEX_CONTAINER,
                '.py':wx.stc.STC_LEX_PYTHON,
                '.xml':wx.stc.STC_LEX_XML,
                '.xrc':wx.stc.STC_LEX_XML,
                '.xgt':wx.stc.STC_LEX_XML,
                'sql':wx.stc.STC_LEX_SQL,
                'properties':wx.stc.STC_LEX_PROPERTIES,
                'errorlist':wx.stc.STC_LEX_ERRORLIST,
                'batch':wx.stc.STC_LEX_BATCH,
                'xcode':wx.stc.STC_LEX_XCODE,
                'diff':wx.stc.STC_LEX_DIFF,
                'conf':wx.stc.STC_LEX_CONF,
                'css':wx.stc.STC_LEX_CSS,
                'nsis':wx.stc.STC_LEX_NSIS,
                'mssql':wx.stc.STC_LEX_MSSQL,
                'phpscript':wx.stc.STC_LEX_PHPSCRIPT,
                'automatic':wx.stc.STC_LEX_AUTOMATIC
}

KEYWORDS = {
                '.py'   :   keyword.kwlist,
                '.xrc'  :   ["canvas", "window", "view", "button", "edittext", "text", "form", "calendar", "dataset", "datapath", "textctrl"],
                '.xgt'  :   ["canvas", "window", "view", "button", "edittext", "text", "form", "calendar", "dataset", "datapath", "textctrl"],
                '.xml'  :   ["canvas", "window", "view", "button", "edittext", "text", "form", "calendar", "dataset", "datapath", "textctrl"],
}
                
                
faces["tabsize"] = int(faces["tabsize"])
faces["little"] = int(faces["little"])
faces["normal"] = int(faces["normal"])
faces["large"] = int(faces["large"])

def get_styles(model, word):
    result = dict()
    
    result["back"] = syntax[model]["DEFAULT"]["back"]
    result["size"] = faces[syntax[model]["DEFAULT"]["size"]]
    result["font"] = faces[syntax[model]["DEFAULT"]["font"]]
    result["color"] = syntax[model]["DEFAULT"]["color"]
    result["weight"] = syntax[model]["DEFAULT"]["weight"]
    
    if word in syntax[model] :
        if 'back' in syntax[model][word] :
            result["back"] = syntax[model][word]["back"]
        
        if 'size' in syntax[model][word] :
            result["size"] = faces[syntax[model][word]["size"]]
            
        if 'font' in syntax[model][word] :
            result["font"] = faces[syntax[model][word]["font"]]
            
        if 'color' in syntax[model][word] :
            result["color"] = syntax[model][word]["color"]
            
        if 'weight' in syntax[model][word] :
            if type(syntax[model][word]["weight"]) == str :
                result["weight"] = syntax[model][word]["weight"]
            else :
                result["weight"] = ",".join(syntax[model][word]["weight"])
    
    return result

class PyEditor(wx.stc.StyledTextCtrl):
    def __init__(self, parent):
        try :
            wx.stc.StyledTextCtrl.__init__(self, parent)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
            
        self.SetProperty("fold", "1")
        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(KEYWORDS[".py"]))


    def SetupColor(self):
        try :
            #Python Style
            self.StyleSetSpec(wx.stc.STC_P_DEFAULT, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python", "DEFAULT"))
            self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","COMMENTLINE"))
            self.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","NUMBER"))
            self.StyleSetSpec(wx.stc.STC_P_STRING, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","STRING"))
            self.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","CHARACTER"))
            self.StyleSetSpec(wx.stc.STC_P_WORD, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","WORD"))
            self.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","TRIPLE"))
            self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","TRIPLEDOUBLE"))
            self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","CLASSNAME"))
            self.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","DEFNAME"))
            self.StyleSetSpec(wx.stc.STC_P_OPERATOR, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","OPERATOR"))
            self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python", "IDENTIFIER"))
            self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python","COMMENTBLOCK"))
            self.StyleSetSpec(wx.stc.STC_P_STRINGEOL, "fore:%(color)s,face:%(font)s,eol,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Python", "STRINGEOL"))
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
            
    def AutoComplete(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN :
            if self.GetCharAt(self.GetLineEndPosition(self.GetCurrentLine()-1)-1) == 58 :
                self.SetLineIndentation(self.GetCurrentLine(), self.GetLineIndentation(self.GetCurrentLine())+self.GetTabWidth())
                self.LineEnd()
            else :
                self.SetLineIndentation(self.GetCurrentLine(), self.GetLineIndentation(self.GetCurrentLine()-1))
                self.LineEnd()
        
        if key == 306 and self.GetLine(self.GetCurrentLine()).find("def") != -1  :
            self.AddText("self) :")
            
        if (key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN) and self.GetLine(self.GetCurrentLine()-1).find("class") != -1  :
            self.AddText("def __init__(self) :")
            
    def onKeyPressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()
            # tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, 'show tip stuff')
            # code completion (needs more work)
            else:
                kw = KEYWORDS[".py"]
                # optionally add more ...
                kw.append("__init__?3")
                # Python sorts are case sensitive
                kw.sort()
                # so this needs to match 
                self.AutoCompSetIgnoreCase(False) 
                # registered images are specified with appended "?type"
                for i in range(len(kw)):
                    if kw[i] in keyword.kwlist:
                        kw[i] = kw[i] + "?1"
                self.AutoCompShow(0, " ".join(kw))
        else:
            event.Skip()

    def onUpdateUI(self, evt):
        """update the user interface"""
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)
        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1
        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos
        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)
        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

class XMLEditor(wx.stc.StyledTextCtrl):
    def __init__(self, parent, filename=None):
        try :
            wx.stc.StyledTextCtrl.__init__(self, parent)
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
        
        self.SetProperty("fold", "1")
        self.SetProperty("fold.html","1")
        self.SetKeyWords(wx.stc.STC_LEX_XML, " ".join(KEYWORDS[".xml"]))
        self.SetLexer(wx.stc.STC_LEX_XML)
        
    def SetupColor(self):
        try :
            # XML styles
            self.StyleSetSpec(wx.stc.STC_H_DEFAULT, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "DEFAULT"))
            self.StyleSetSpec(wx.stc.STC_H_COMMENT, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "COMMENT"))
            self.StyleSetSpec(wx.stc.STC_H_NUMBER, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "NUMBER"))
            self.StyleSetSpec(wx.stc.STC_H_SINGLESTRING, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "SINGLESTRING"))
            self.StyleSetSpec(wx.stc.STC_H_DOUBLESTRING, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "DOUBLESTRING"))
            self.StyleSetSpec(wx.stc.STC_H_XMLSTART, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "XMLSTART"))
            self.StyleSetSpec(wx.stc.STC_H_XMLEND, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "XMLEND"))
            self.StyleSetSpec(wx.stc.STC_H_TAG, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "TAG"))
            self.StyleSetSpec(wx.stc.STC_H_TAGEND, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "TAGEND"))
            self.StyleSetSpec(wx.stc.STC_H_ATTRIBUTE, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "ATTRIBUTE"))
            self.StyleSetSpec(wx.stc.STC_H_CDATA, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("XML", "CDATA"))
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
    
    def AutoComplete(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN :
            if self.GetCharAt(self.GetLineEndPosition(self.GetCurrentLine()-1)-1) == 58 :
                self.SetLineIndentation(self.GetCurrentLine(), self.GetLineIndentation(self.GetCurrentLine())+self.GetTabWidth())
                self.LineEnd()
            else :
                self.SetLineIndentation(self.GetCurrentLine(), self.GetLineIndentation(self.GetCurrentLine()-1))
                self.LineEnd()
        
        if key == 306 and self.GetLine(self.GetCurrentLine()).find("def") != -1  :
            self.AddText("self) :")
            
        if (key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN) and self.GetLine(self.GetCurrentLine()-1).find("class") != -1  :
            self.AddText("def __init__(self) :")
            
    
    def OnKeyPressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
        
        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()

            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\n'
                                 'show some suff, maybe parameters..\n\n'
                                 'fubar(param1, param2)')
            # Code completion
            else:
                pos = self.GetCurrentPos()
                start = self.WordStartPosition(pos, 1)
                end = self.WordEndPosition(pos, 1)
                
                kw = KEYWORDS[".xml"]
                # optionally add more ...
                #kw.append("__init__(self):?2")
                # Python sorts are case sensitive
                #kw.sort(key=self.StartsWith)
                kw.sort()
                # so this needs to match 
                self.AutoCompSetIgnoreCase(False) 
                # registered images are specified with appended "?type"
                for i in range(len(kw)):
                    if kw[i] in KEYWORDS[".xml"]:
                        kw[i] = kw[i] + "?1"
                        
                self.AutoCompShow((pos-start), " ". join(kw))
        else:
            event.Skip()

    def OnUpdateUI(self, evt):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "<>" and styleBefore == wx.stc.STC_H_TAG:
            braceAtCaret = caretPos - 1 
        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "<>" and styleAfter == wx.stc.STC_H_TAG:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)
        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

class CodeEditor(PyEditor, XMLEditor):
    def __init__(self, parent, filename):
        name, ext = os.path.splitext(filename)
        
        if ext == ".py" :
            PyEditor.__init__(self, parent)
            PyEditor.SetupColor(self)
            self.AutoComp = PyEditor.AutoComplete
        else :
            XMLEditor.__init__(self, parent)
            XMLEditor.SetupColor(self)
            self.AutoComp = XMLEditor.AutoComplete
        
        self.ext = ext
            
        self.SetupDefault()
        
        self.SetupEvent()
        
        self.SetupEvent()
        
        self.LoadFile(filename)
    
    def SetupDefault(self):
        try :
            # set other options ...
            self.SetMargins(0, 0)
            #self.SetViewWhiteSpace(False)
            #self.SetViewWhiteSpace(True)

            self.SetEdgeMode(wx.stc.STC_EDGE_LINE)

            self.SetEdgeColumn(81)
            self.SetCaretForeground("black")
            self.SetCaretWidth(2)
            self.SetCaretLineVisible(True)
            self.SetCaretLineBack('#eeeed1')
            self.SetTabWidth(faces["tabsize"])

            self.SetViewEOL(False)


            self.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
            self.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
            self.SetMarginSensitive(2, True)
            self.SetMarginWidth(2, 12)

            self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS, "white", "#808080")
            self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS, "white", "#808080")
            self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_VLINE, "white", "#808080")
            self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_LCORNER, "white", "#808080")
            self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080")
            self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER, "white", "#808080")

            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("DEFAULT", "DEFAULT"))

            # more global default styles for all languages
            self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("DEFAULT", "LINENUMBER"))
            self.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("DEFAULT", "CONTRLCHAR"))
            self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("DEFAULT", "BRACELIGHT"))
            self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("DEFAULT", "BRACEBAD"))
            self.StyleSetSpec(wx.stc.STC_STYLE_LASTPREDEFINED,  "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("DEFAULT", "LASTPREDEFINED"))

            # register some images for use in the AutoComplete box
            self.RegisterImage(1, wx.ArtProvider.GetBitmap(wx.ART_TIP, size=(16,16)))
            self.RegisterImage(2, wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16,16)))
            self.RegisterImage(3, wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16,16)))
        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
            
    
    def SetupEvent(self):
        try :
            self.Bind(wx.EVT_KEY_UP, self.AutoIndent)
            self.Bind(wx.stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
            self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
            self.Bind(wx.stc.EVT_STC_UPDATEUI, self.OnUpdateUI)

        except :
            logger.write(sys.exc_value, "ERROR", (self, traceback.extract_stack()))
    
    def AutoIndent(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_NUMPAD_ENTER or key == wx.WXK_RETURN :
            
            if self.GetCharAt(self.GetLineEndPosition(self.GetCurrentLine()-1)-1) == 58 :   #char :        
                
                self.SetLineIndentation(self.GetCurrentLine(), int(self.GetLineIndentation(self.GetCurrentLine()-1)))
                
                self.LineEnd()
            elif self.GetCharAt(self.GetLineEndPosition(self.GetCurrentLine()-1)-1) == 62 : #char >
                if self.GetCharAt(self.GetLineEndPosition(self.GetCurrentLine()-1)-2) != 47 : #char /
                    #print "Line:", self.GetCurrentLine()-1, " Text:", self.GetLine(self.GetCurrentLine()-1), " Ident:", self.GetLineIndentation(self.GetCurrentLine()-1), " Tab:", self.GetTabWidth()

                    self.SetLineIndentation(self.GetCurrentLine(), int(self.GetLineIndentation(self.GetCurrentLine()-1)))

                    #print "Line:", self.GetCurrentLine(), " Text:", self.GetLine(self.GetCurrentLine()), " Ident:", self.GetLineIndentation(self.GetCurrentLine()), " Tab:", self.GetTabWidth()

                    self.LineEnd()
            else :
                self.SetLineIndentation(self.GetCurrentLine(), self.GetLineIndentation(self.GetCurrentLine()-1))
                self.LineEnd()
                
            self.AutoComp(self, event)
            
        if event.ControlDown() :
            if key == wx.WXK_TAB :
                if self.GetLine(self.GetCurrentLine()).find("{") != -1 :
                    event.StopPropagation()
                    self.SetSelection(self.FindText(0, self.GetTextLength(), "{", 0), self.FindText(0, self.GetTextLength(), "}", 0)+1)
                

    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & wx.stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)
                        
                        

    def foldAll(self):
        """folding folds, marker - to +"""
        lineCount = self.GetLineCount()
        expanding = True
        # find out if folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) &\
                    wx.stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldexpanded(lineNum)
                break;
        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & wx.stc.STC_FOLDLEVELHEADERFLAG and \
                (level & wx.stc.STC_FOLDLEVELNUMBERMASK) ==\
                    wx.stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldexpanded(lineNum, True)
                    lineNum = self.expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldexpanded(lineNum, False)
                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)
            lineNum = lineNum + 1

    def expand(self, line, doexpand, force=False, visLevels=0, level=-1):
        """expanding folds, marker + to -"""
        lastChild = self.GetLastChild(line, level)
        line = line + 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doexpand:
                    self.ShowLines(line, line)
            if level == -1:
                level = self.GetFoldLevel(line)
            if level & wx.stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldexpanded(line, True)
                    else:
                        self.SetFoldexpanded(line, False)
                    line = self.expand(line, doexpand, force, visLevels-1)
                else:
                    if doexpand and self.GetFoldexpanded(line):
                        line = self.expand(line, True, force, visLevels-1)
                    else:
                        line = self.expand(line, False, force, visLevels-1)
            else:
                line = line + 1;
        return line

    def DoPrettyPrint(self):
        doc = etree.parse(StringIO(self.GetText()))
        self.SetText(etree.tostring(doc, pretty_print=True))
    
    def DoUndo(self):
        pass
    
    def Redo(self):
        pass