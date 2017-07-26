"""
WxFileRenamer is a small GUI utility for renaming files in a directory
with regular expressions. The dialog consists of a console window for
text feedback followed by the three text fields: Dir, Search, and Replace
plus buttons for Simulate, Execute, and Quit.

Instructions:

* Use the command line or drag'n'drop to run WxFileRenamer with the path 
to a file whose name is to be changed.

* The directory path will appear in the Dir text field. The filename will
appear in the Search and Replace fields.

* Modify the Search and Replace regular expressions as desired.

* Click "Simulate" button to view effects of current Search and Replace
expressions on directory files without actually renaming files.

* Click "Execute" button to rename files according to Search and Replace
expressions.

* Click "Quit" button or select File\Quit from menu to exit application.

Requires wxPython -- download from http://www.wxpython.org/download.php.

Jack Trainor 2008
"""
import sys
import os, os.path
import re
import wx

DialogWidth = 1000
DialogHeight = 800

""" Utility class for renaming files and displaying results to output. """
class FileRenamer(object):
    def __init__(self, dir, matchRe, replaceRe, output, simulate=True):
        self.dir = dir
        self.output = output
        self.matchPat = re.compile(matchRe)
        self.replaceRe = replaceRe
        self.simulate = simulate
            
    def renamePath(self, path, newPath): 
        try:
            absPath = os.path.abspath(path)
            os.chmod(absPath, 0666)
            os.rename( absPath, newPath )
        except Exception, e:
            self.output('RenamePath failed: %s, %s' % (path, newPath))
    
    def execute(self):
        fileNames = os.listdir(self.dir)
        for fileName in fileNames:
            if self.matchPat.match(fileName):
                newName = self.matchPat.sub(self.replaceRe, fileName)
                self.output("%s -> %s\n" % (fileName, newName))
                if not self.simulate:
                    path = os.path.join(self.dir, fileName)
                    newPath = os.path.join(self.dir, newName)
                    self.renamePath(path, newPath)
        return self 

""" Wx utils """    
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
    
""" Wx app """
class FileRenamePanel(wx.Panel):
    LABEL_WIDTH = 50
    ENTRY_WIDTH = DialogWidth-100
    def __init__(self, parent, id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)

        dir = searchText = ""
        path = parent.app.path
        if os.path.exists(path):
            if os.path.isdir(path):
                dir = path
                fileNames = os.listdir(dir)
                if fileNames:
                    fileNames.sort()
                    searchText = fileNames[0]
            elif os.path.isfile(path):
                dir, searchText = os.path.split(path)
        replaceText = searchText
        
        self.consoleText = wx.TextCtrl(self, -1, "", size=(DialogWidth-20, DialogHeight-220), style=wx.TE_MULTILINE)       

        dirLabel = wx.StaticText(self, -1, "Dir:", size=(FileRenamePanel.LABEL_WIDTH, -1), style=wx.ALIGN_RIGHT)
        self.dirEntry = wx.TextCtrl(self, -1, dir, wx.DefaultPosition, wx.Size(FileRenamePanel.ENTRY_WIDTH, -1))
        self.dirEntry.SetFont(wx.Font(-1, -1, wx.NORMAL, wx.BOLD))
        
        searchLabel = wx.StaticText(self, -1, "Search:", size=(FileRenamePanel.LABEL_WIDTH, -1), style=wx.ALIGN_RIGHT)
        self.searchEntry = wx.TextCtrl(self, -1, searchText , wx.DefaultPosition, wx.Size(FileRenamePanel.ENTRY_WIDTH, -1))
        self.searchEntry.SetFont(wx.Font(-1, -1, wx.NORMAL, wx.BOLD))

        replaceLabel = wx.StaticText(self, -1, "Replace:", size=(FileRenamePanel.LABEL_WIDTH, -1), style=wx.ALIGN_RIGHT)
        self.replaceEntry = wx.TextCtrl(self, -1, replaceText, wx.DefaultPosition, wx.Size(FileRenamePanel.ENTRY_WIDTH, -1))
        self.replaceEntry.SetFont(wx.Font(-1, -1, wx.NORMAL, wx.BOLD))
        
        self.simulateButton = CreateButton(parent, self, "Simulate", parent.OnSimulate)
        self.executeButton = CreateButton(parent, self, "Execute", parent.OnExecute)
        self.quitButton = CreateButton(parent, self, "Quit", parent.OnQuit)
        
        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )
        buttonSizer.Add(self.simulateButton, 0, wx.ALL, 5 )
        buttonSizer.Add(self.executeButton, 0, wx.ALL, 5 )
        buttonSizer.Add(self.quitButton, 0, wx.ALL, 5 )
        
        sizer = wx.BoxSizer( wx.VERTICAL )
        sizer.Add(self.consoleText, 0, wx.ALL, 5 )
        sizer.Add(CreateLabeledTextSizer(dirLabel, self.dirEntry), 0, wx.ALIGN_LEFT) 
        sizer.Add(CreateLabeledTextSizer(searchLabel, self.searchEntry), 0, wx.ALIGN_LEFT) 
        sizer.Add(CreateLabeledTextSizer(replaceLabel, self.replaceEntry), 0, wx.ALIGN_LEFT) 
        sizer.Add(buttonSizer, 0, wx.ALL, 5 )
        
        self.SetSizer(sizer)
        self.Layout()        

    def GetConsoleText(self):
        return self.consoleText.GetValue()

    def SetConsoleText(self, text):
        self.consoleText.SetValue(text)
        self.consoleText.SetSelection(0, 0)

    def GetDirText(self):
        return self.dirEntry.GetValue()

    def GetSearchText(self):
        return self.searchEntry.GetValue()

    def GetReplaceText(self):
        return self.replaceEntry.GetValue()


class FileRenameFrame(wx.Frame):
    def __init__(self, app, parent, title):
        self.app = app
        wx.Frame.__init__(self, parent, -1, title, pos=(0, 0), size=(DialogWidth, DialogHeight))
        self.CreateStatusBar()

        menuBar = CreateMenuBar(self)
        fileMenu = CreateMenu(menuBar, "&File")
        CreateMenuItem(self, fileMenu, wx.ID_EXIT, "Q&uit\tCtrl-Q", "Exit", self.OnTimeToClose)
        self.panel = FileRenamePanel(self)
    
    def OnInit(self):
        self.frame = frame = FileRenameFrame(self, None, "FileRename Dialog")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

    def OnSimulate(self, evt):
        self.Execute(True)

    def OnExecute(self, evt):
        self.Execute(False)
        
    def Execute(self, simulate=True):
        dir = self.panel.GetDirText()
        matchRe = self.panel.GetSearchText()
        replaceRe = self.panel.GetReplaceText()
        fileRenamer = FileRenamer(dir, matchRe, replaceRe, self.AppendConsoleText, simulate).execute()
        self.AppendConsoleText("\n")

    def OnQuit(self, evt):
        self.OnTimeToClose(evt)

    def OnTimeToClose(self, evt):
        self.Close()

    def GetConsoleText(self):
        return self.panel.GetConsoleText()

    def SetConsoleText(self, text):
        self.panel.SetConsoleText(text)

    def AppendConsoleText(self, text):
        self.panel.consoleText.AppendText(text)

class WxFileRenamer(wx.App):
    def __init__(self, path, redirect=True, fileName=None):
        self.path = path
        wx.App.__init__(self, redirect, fileName)
        
    def OnInit(self):
        self.frame = frame = FileRenameFrame(self, None, "WxFileRenamer")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        
def main(path):
    app = WxFileRenamer(path, redirect=False)
    app.MainLoop()

if __name__ == '__main__':
    path = r""
    if len(sys.argv) > 1:
        path = sys.argv[1]
    main(path)
