"""
WxGrepDialog is a small GUI utility for testing regular expressions 
on specified text in main console window, allowing iterative
development of working regular expressions.

Instructions
============
* Copy text to be grepped to the clipboard.
* Launch WxGrepDialog.
* Paste clipboard text into console window.
* Construct regular expressions in Search and Replace fields.
* Click Replace button to see result of regular expressions.
* If result in console window is undesired, click Undo button.
* Try again.

Notes
=====
* Performs multiple levels of undo.
* Regular expression strings are assumed to be in raw form.
* Replace performs re.sub on a line-by-line basis of text.
* Errors caused by malformed regular expressions print to stderr.
* Requires wxPython -- download from http://www.wxpython.org/download.php.

Jack Trainor 2008
"""
import sys
import os, os.path
import re
import wx
#import Clipboard

DialogWidth = 1000
DialogHeight = 800

def CreateMenuBar(frame):
    menuBar = wx.MenuBar()
    frame.SetMenuBar(menuBar)
    return menuBar

def CreateMenu(menuBar, menuTitle):
    menu = wx.Menu()
    menuBar.Append(menu, menuTitle)
    return menu

def CreateMenuItem(frame, menu, id, itemTitle, statusMsg, method):
    menu.Append(id, itemTitle, statusMsg)
    frame.Bind(wx.EVT_MENU, method, id=id)
    
def CreateButton(frame, panel, buttonTitle, method, id=wx.ID_ANY):
    button = wx.Button(panel, id, buttonTitle)
    frame.Bind(wx.EVT_BUTTON, method, button)
    return button

def CreateLabeledTextSizer(staticText, textCtrl, proportion=0, flag=wx.ALL, border=5):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(staticText, 0, wx.ALL, 5 )
    sizer.Add(textCtrl, 0, wx.ALL, 5 )
    return sizer
 
 
class GrepPanel(wx.Panel):
    LABEL_WIDTH = 50
    ENTRY_WIDTH = DialogWidth-100
    def __init__(self, parent, id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)

        self.editText = wx.TextCtrl(self, -1, "", size=(DialogWidth-20, DialogHeight-220), style=wx.TE_MULTILINE)       

        searchLabel = wx.StaticText(self, -1, "Search:", size=(GrepPanel.LABEL_WIDTH, -1), style=wx.ALIGN_RIGHT)
        self.searchEntry = wx.TextCtrl(self, -1, "(.*)" , wx.DefaultPosition, wx.Size(GrepPanel.ENTRY_WIDTH, -1))
        self.searchEntry.SetFont(wx.Font(-1, -1, wx.NORMAL, wx.BOLD))

        replaceLabel = wx.StaticText(self, -1, "Replace:", size=(GrepPanel.LABEL_WIDTH, -1), style=wx.ALIGN_RIGHT)
        self.replaceEntry = wx.TextCtrl(self, -1, r"[\1]" , wx.DefaultPosition, wx.Size(GrepPanel.ENTRY_WIDTH, -1))
        self.replaceEntry.SetFont(wx.Font(-1, -1, wx.NORMAL, wx.BOLD))

        self.replaceButton = CreateButton(parent, self, "Replace", parent.OnReplace)
        self.undoButton = CreateButton(parent, self, "Undo", parent.OnUndo)
        self.quitButton = CreateButton(parent, self, "Quit", parent.OnTimeToClose)
        
        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )
        buttonSizer.Add(self.replaceButton, 0, wx.ALL, 5 )
        buttonSizer.Add(self.undoButton, 0, wx.ALL, 5 )
        buttonSizer.Add(self.quitButton, 0, wx.ALL, 5 )        
        
        sizer = wx.BoxSizer( wx.VERTICAL )
        sizer.Add(self.editText, 0, wx.ALL, 5 )
        sizer.Add(CreateLabeledTextSizer(searchLabel, self.searchEntry), 0, wx.ALIGN_LEFT) 
        sizer.Add(CreateLabeledTextSizer(replaceLabel, self.replaceEntry), 0, wx.ALIGN_LEFT) 
        sizer.Add(buttonSizer, 0, wx.ALL, 5 )
        
        self.SetSizer(sizer)
        self.Layout()        

    def GetText(self):
        return self.editText.GetValue()

    def GetSearchText(self):
        return self.searchEntry.GetValue()

    def GetReplaceText(self):
        return self.replaceEntry.GetValue()

    def GetFlagsText(self):
        return self.flagsEntry.GetValue()

    def SetText(self, text):
        self.editText.SetValue(text)
        self.editText.SetSelection(0, 0)


class GrepFrame(wx.Frame):
    def __init__(self, app, parent, title):
        self.app = app
        wx.Frame.__init__(self, parent, -1, title, pos=(0, 0), size=(DialogWidth, DialogHeight))
        self.CreateStatusBar()

        menuBar = CreateMenuBar(self)
        fileMenu = CreateMenu(menuBar, "&File")
        CreateMenuItem(self, fileMenu, wx.ID_EXIT, "Q&uit\tCtrl-Q", "Exit", self.OnTimeToClose)
        self.panel = GrepPanel(self)
    
    def OnInit(self):
        self.frame = frame = GrepFrame(self, None, "Grep Dialog")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

    def OnReplace(self, evt):
        text = self.panel.GetText()
        searchPat = self.panel.GetSearchText()
        replacePat = self.panel.GetReplaceText()
        self.app.Replace(text, searchPat, replacePat, "")        

    def OnUndo(self, evt):
        self.app.Undo()
    
    def OnTimeToClose(self, evt):
        self.Close()

    def GetText(self):
        return self.panel.GetText()

    def SetText(self, text):
        self.panel.SetText(text)

class GrepApp(wx.App):
    def __init__(self, redirect=True, fileName=None):
        wx.App.__init__(self, redirect, fileName)
        
    def OnInit(self):
        self.frame = frame = GrepFrame(self, None, "Grep Dialog")
        self.SetTopWindow(frame)
        frame.Show(True)
        self.undoStack = []
        self.PushUndoText(self.frame.GetText())
        text = ""
        self.frame.SetText(text)
        return True
        
    def PushUndoText(self, text):
        self.undoStack.append(text)
        
    def PopUndoText(self):
        text = None
        if len(self.undoStack):
            text = self.undoStack.pop()
        return text
        
    def Replace(self, text, searchPat, replacePat, flags):
        try:
            self.PushUndoText(text)
            if flags:
                flags = ', ' + flags
    
            command = 'text = re.sub( r\'%s\', r\'%s\', text%s )' % ( searchPat, replacePat, flags )
            print command
            exec command        
            self.frame.SetText(text)
        except Exception, e:
            sys.stderr.write("%s %s\n" % ("GrepApp#Replace", e))
        
    def Undo(self):
        text = self.PopUndoText()
        if text:
            self.frame.SetText(text)
    
def main():
    app = GrepApp(redirect=False)
    app.MainLoop()

if __name__ == '__main__':
    main()
    
