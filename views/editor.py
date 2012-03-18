# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Giuseppe Tripoli"
__date__ ="$16-mar-2012 15.03.06$"

# styled text using wxPython's
# wx.StyledTextCtrl(parent, id, pos, size, style, name)
# set up for folding and Python code highlighting
# source: Dietrich  16NOV2008

import wx
import wx.stc
import keyword

from globals.obj_cfg import o_cfg

syntax = o_cfg("publics\syntax.ini")

shortcuts = o_cfg("publics\shortcuts.ini")

if wx.Platform == '__WXMSW__':
    # for windows OS
    faces = syntax.configfile["Windows"]
else:
    faces = syntax.configfile["Other"]

faces["little"] = int(faces["little"])
faces["normal"] = int(faces["normal"])
faces["large"] = int(faces["large"])

def get_styles(word):
    result = dict()
    
    result["back"] = syntax.configfile["Python"]["Default"]["back"]
    result["size"] = faces[syntax.configfile["Python"]["Default"]["size"]]
    result["font"] = faces[syntax.configfile["Python"]["Default"]["font"]]
    result["color"] = syntax.configfile["Python"]["Default"]["color"]
    result["weight"] = syntax.configfile["Python"]["Default"]["weight"]
    
    if word in syntax.configfile["Python"] :
        if 'back' in syntax.configfile["Python"][word] :
            result["back"] = syntax.configfile["Python"][word]["back"]
        
        if 'size' in syntax.configfile["Python"][word] :
            result["size"] = faces[syntax.configfile["Python"][word]["size"]]
            
        if 'font' in syntax.configfile["Python"][word] :
            result["font"] = faces[syntax.configfile["Python"][word]["font"]]
            
        if 'color' in syntax.configfile["Python"][word] :
            result["color"] = syntax.configfile["Python"][word]["color"]
            
        if 'weight' in syntax.configfile["Python"][word] :
            if type(syntax.configfile["Python"][word]["weight"]) == str :
                result["weight"] = syntax.configfile["Python"][word]["weight"]
            else :
                result["weight"] = ",".join(syntax.configfile["Python"][word]["weight"])
    
    return result

class code_editor(wx.stc.StyledTextCtrl):
    """
    set up for folding and Python code highlighting
    """
    def __init__(self, parent):
        wx.stc.StyledTextCtrl.__init__(self, parent, wx.ID_ANY)
        # use Python code highlighting
        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        # set other options ...
        self.SetProperty("fold", "1")
        self.SetMargins(0, 0)
        self.SetViewWhiteSpace(False)
        #self.SetEdgeMode(wx.stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)
        self.SetCaretForeground("blue")

        # setup a margin to hold the fold markers
        self.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        # fold markers use square headers
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN,
            wx.stc.STC_MARK_BOXMINUS, "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER,
            wx.stc.STC_MARK_BOXPLUS, "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB,
            wx.stc.STC_MARK_VLINE, "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL,
            wx.stc.STC_MARK_LCORNER, "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND,
            wx.stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID,
            wx.stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL,
            wx.stc.STC_MARK_TCORNER, "white", "#808080")

        # bind some events ...
        self.Bind(wx.stc.EVT_STC_UPDATEUI, self.onUpdateUI)
        self.Bind(wx.stc.EVT_STC_MARGINCLICK, self.onMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPressed)

        # make some general styles ...
        # global default styles for all languages
        # set default font
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("Default"))
        # set default background color
        #beige = '#F5F5DC'
        #self.StyleSetBackground(style=wx.stc.STC_STYLE_DEFAULT)
        # reset all to be like the default
        self.StyleClearAll() 

        # more global default styles for all languages
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("LINENUMBER"))
        self.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("CONTRLCHAR"))
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("BRACELIGHT"))
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("BRACEBAD"))

        # make the Python styles ...
        # default
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("DEFAULT"))
        # comments
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("COMMENTLINE"))
        # number
        self.StyleSetSpec(wx.stc.STC_P_NUMBER,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("NUMBER"))
        # string
        self.StyleSetSpec(wx.stc.STC_P_STRING,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("STRING"))
        # single quoted string
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("CHARACTER"))
        # keyword
        self.StyleSetSpec(wx.stc.STC_P_WORD,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("WORD"))
        # triple quotes
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("TRIPLE"))

        # triple double quotes
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("TRIPLEDOUBLE"))

        # class name definition
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("CLASSNAME"))
            
        # function or method name definition
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("DEFNAME"))
        # operators
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("OPERATOR"))
        # identifiers
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("IDENTIFIER"))
        # comment-blocks
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("COMMENTBLOCK"))

        # end of line where string is not closed
        self.StyleSetSpec(wx.stc.STC_P_STRINGEOL,
            "fore:%(color)s,face:%(font)s,back:%(back)s,size:%(size)d,%(weight)s" % get_styles("STRINGEOL"))
        # register some images for use in the AutoComplete box
        self.RegisterImage(1,
            wx.ArtProvider.GetBitmap(wx.ART_TIP, size=(16,16)))
        self.RegisterImage(2,
            wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16,16)))
        self.RegisterImage(3,
            wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16,16)))

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
                kw = keyword.kwlist[:]
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
        if charBefore and chr(charBefore) in "[]{}()"\
                and styleBefore == wx.stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1
        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()"\
                    and styleAfter == wx.stc.STC_P_OPERATOR:
                braceAtCaret = caretPos
        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)
        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

    def onMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.foldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(lineClicked) &\
                        wx.stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldexpanded(lineClicked, True)
                        self.expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldexpanded(lineClicked):
                            self.SetFoldexpanded(lineClicked, False)
                            self.expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldexpanded(lineClicked, True)
                            self.expand(lineClicked, True, True, 100)
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


class MyFrame(wx.Frame):
    def __init__(self, parent, mytitle, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle, size=mysize)

        stc_edit = MySTC(self)

        # open a Python code file you have ...
        py_file = "wxstc_basics1.py"
        stc_edit.SetText(open(py_file).read())
        stc_edit.EmptyUndoBuffer()

        # line numbers in the margin
        stc_edit.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        stc_edit.SetMarginWidth(1, 25)