"""
CommentEditor: Small HTML editor for online comments with preview feature.

Based on wxWidgets.
"""
__author__=["Jack Trainor (jacktrainor@gmail.com)",]
__version__="June 2009"
import sys
import os, os.path
import re
import wx, wx.html

DIALOG_WIDTH = 600
DIALOG_HEIGHT = 300
    
def create_button(frame, panel, buttonTitle, method, id=wx.ID_ANY):
    button = wx.Button(panel, id, buttonTitle)
    frame.Bind(wx.EVT_BUTTON, method, button)
    return button


class PreviewHtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, frame):
        wx.html.HtmlWindow.__init__(self,parent,id)

class PreviewPanel(wx.Panel):
    def __init__(self, parent, id, frame):
        wx.Panel.__init__(self, parent, id)
        self.frame = frame
        self.html = PreviewHtmlWindow(self, -1, self.frame)

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.html, 1, wx.GROW)
        subbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.backButton = create_button(parent, self, "Back", self.OnBack)
        subbox.Add(self.backButton, 1, wx.GROW | wx.ALL, 2)

        self.forwardButton = create_button(parent, self, "Forward", self.OnForward)
        subbox.Add(self.forwardButton, 1, wx.GROW | wx.ALL, 2)

        self.box.Add(subbox, 0, wx.GROW)
        self.SetSizer(self.box)
        self.SetAutoLayout(True)

    def OnBack(self, event):
        if not self.html.HistoryBack():
            wx.MessageBox("No more items in history!")

    def OnForward(self, event):
        if not self.html.HistoryForward():
            wx.MessageBox("No more items in history!")

class PreviewFrame(wx.Frame):
    def __init__(self, app, parent, title):
        self.app = app
        screen_pos = parent.ScreenPosition
        screen_pos.y += parent.Size.y
        wx.Frame.__init__(self, parent, -1, title, screen_pos, parent.Size)
        self.panel = PreviewPanel(self, wx.ID_ANY, self)
    
    def OnTimeToClose(self, evt=None):
        self.Close()

class EditorPanel(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)

        font = wx.Font(10, -1, wx.NORMAL, wx.FONTSTYLE_NORMAL, faceName="Courier New")
        self.editText = wx.TextCtrl(self, -1, "", size=(DIALOG_WIDTH-20, DIALOG_HEIGHT-96), style=wx.TE_MULTILINE) 
        self.editText.SetFont(font)

        self.anchorButton = create_button(parent, self, "Anchor", parent.OnAnchor)
        self.anchorEntry = wx.TextCtrl(self, -1, "" , wx.DefaultPosition, wx.Size(DIALOG_WIDTH-100, -1))
        self.anchorEntry.SetFont(font)

        self.boldButton = create_button(parent, self, "Bold", parent.OnBold)
        self.italicButton = create_button(parent, self, "Italic", parent.OnItalic)
        self.blockquoteButton = create_button(parent, self, "Blockquote", parent.OnBlockquote)

        self.previewButton = create_button(parent, self, "Preview", parent.OnPreview)
        self.quitButton = create_button(parent, self, "Quit", parent.OnTimeToClose)
        
        anchorSizer = wx.BoxSizer(wx.HORIZONTAL)
        anchorSizer.Add(self.anchorButton, 0, wx.GROW | wx.ALL, 2)
        anchorSizer.Add(self.anchorEntry, 0, wx.GROW | wx.ALL, 2)
        
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(self.boldButton, 0, wx.GROW | wx.ALL, 2)
        buttonSizer.Add(self.italicButton, 0, wx.GROW | wx.ALL, 2)
        buttonSizer.Add(self.blockquoteButton, 0, wx.GROW | wx.ALL, 2)
        buttonSizer.Add(self.previewButton, 0, wx.GROW | wx.ALL, 2)        
        buttonSizer.Add(self.quitButton, 0, wx.GROW | wx.ALL, 2)       

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.editText, 1, wx.GROW | wx.ALL, 2)
        sizer.Add(anchorSizer, 0, wx.ALL, 2) 
        sizer.Add(buttonSizer, 0, wx.ALL, 2)
        
        self.SetSizer(sizer)
        self.Layout()        

    def GetText(self):
        return self.editText.GetValue()

    def GetAnchorText(self):
        return self.anchorEntry.GetValue()

    def SetText(self, text):
        self.editText.SetValue(text)
        self.editText.SetSelection(0, 0)
        
    def TagSelection(self, tag, attributes={}):
        from_pos, to_pos = self.editText.GetSelection()
        s = self.editText.GetStringSelection()
        if s:
            attrs_list = []
            for key, val in attributes.items():
                if type(val) == str:
                    val = '"%s"' % (key)                
                attrs_list.append('%s=%s' % (key, str(val)))
            open_tag = "<" + tag
            if attrs_list:
                open_tag += " " + " ".join(attrs_list)
            open_tag += ">"
            end_tag = "</" + tag + ">"
            s = open_tag + s + end_tag
            self.editText.Replace(from_pos, to_pos, s)  


class EditorFrame(wx.Frame):
    def __init__(self, app, parent, title):
        self.app = app
        wx.Frame.__init__(self, parent, -1, title, pos=(0, 0), size=(DIALOG_WIDTH, DIALOG_HEIGHT))
        self.panel = EditorPanel(self)
        self.previewFrame = None
    
    def OnBold(self, evt):
        self.panel.TagSelection("b")  

    def OnItalic(self, evt):
        self.panel.TagSelection("i")  

    def OnBlockquote(self, evt):
        self.panel.TagSelection("blockquote")  

    def OnAnchor(self, evt):
        anchorText = self.panel.GetAnchorText()
        if anchorText and anchorText.find("http:") == 0:
            self.panel.TagSelection("a", {"href":anchorText})           

    def OnPreview(self, evt):
        if self.previewFrame:
            self.previewFrame.OnTimeToClose()
        self.previewFrame = PreviewFrame(self.app, self, "Preview")
        self.previewFrame.Show(True)
        text = self.GetText()
        text = text.replace("\n", "<br>")
        text = "<html><body>" + text + "</body></html>"
        self.previewFrame.panel.html.SetPage(text)

    def OnTimeToClose(self, evt):
        if self.previewFrame:
            self.previewFrame.OnTimeToClose()
        self.Close()

    def GetText(self):
        return self.panel.GetText()

    def SetText(self, text):
        self.panel.SetText(text)
        
        
class CommentEditor(wx.App):
    def __init__(self, redirect=True, fileName=None):
        wx.App.__init__(self, redirect, fileName)
        
    def OnInit(self):
        self.frame = EditorFrame(self, None, "Comment Editor")
        self.SetTopWindow(self.frame)
        self.frame.Show(True) 
        return True

def main():
    app = CommentEditor(redirect=False)
    app.MainLoop()

if __name__ == '__main__':
    main()
    
