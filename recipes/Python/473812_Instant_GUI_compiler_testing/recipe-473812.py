import wx   # requires wxPython
import sys  # required to redirect the output

class EditorSashWindow(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        winids = []

        # Left window has fixed size and contains control buttons
        self.controls = wx.SashLayoutWindow(self, -1)
        winids.append(self.controls.GetId())
        
        self.controls.SetDefaultSize((80, 600))
        self.controls.SetOrientation(wx.LAYOUT_VERTICAL)
        self.controls.SetAlignment(wx.LAYOUT_LEFT)
        
        b = wx.Button(self.controls, -1, "Open", (3, 20))
        self.Bind(wx.EVT_BUTTON, self.openFile, b)
        b.SetDefault()
        b2 = wx.Button(self.controls, -1, "Save", (3, 60))
        self.Bind(wx.EVT_BUTTON, self.saveFile, b2)
        b2.SetDefault()
        b3 = wx.Button(self.controls, -1, "Run", (3, 100))
        self.Bind(wx.EVT_BUTTON, self.run, b3)
        b3.SetDefault()
        b4 = wx.Button(self.controls, -1, "Clear", (3, 140))
        self.Bind(wx.EVT_BUTTON, self.clear, b4)
        b4.SetDefault()

        # This will occupy the space not used by the Layout Algorithm
        self.remainingSpace = wx.SashLayoutWindow(
                                 self, -1, style=wx.NO_BORDER|wx.SW_3D)
                                
        self.python_editor = wx.TextCtrl(self.remainingSpace,
                        -1, "", wx.DefaultPosition, wx.DefaultSize, 
                        wx.TE_MULTILINE|wx.SUNKEN_BORDER
                        )
        self.python_editor.SetValue("#Editor window")

        # The output window is at the extreme right
        win =  wx.SashLayoutWindow(
                self, -1, wx.DefaultPosition, (200, 30), 
                wx.NO_BORDER|wx.SW_3D
                )
        winids.append(win.GetId())
        win.SetDefaultSize((300, 600))
        win.SetOrientation(wx.LAYOUT_VERTICAL)
        win.SetAlignment(wx.LAYOUT_RIGHT)
        win.SetSashVisible(wx.SASH_LEFT, True)
        win.SetExtraBorderSize(10)
        self.rightWindow = win
        self.output_window = wx.TextCtrl(win, -1, "", wx.DefaultPosition, 
                        wx.DefaultSize, wx.TE_MULTILINE|wx.SUNKEN_BORDER)
        self.output_window.SetValue("Output Window\n")
        #redirecting output
        sys.stdout = self.output_window
        sys.stderr = self.output_window   

        self.Bind(wx.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag, id=min(winids), 
                  id2=max(winids))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def OnSashDrag(self, event):
        eobj = event.GetEventObject()
        if eobj is self.rightWindow:
            self.rightWindow.SetDefaultSize((event.GetDragRect().width, 600))
        wx.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)
        self.remainingSpace.Refresh()

    def OnSize(self, event):
        wx.LayoutAlgorithm().LayoutWindow(self, self.remainingSpace)

    def saveFile(self, event):
        self.output_window.SetValue("Save File not implemented")
        
    def openFile(self, event):
        self.output_window.SetValue("Open File not implemented")
        
    def run(self, event):
        '''Runs the user code; input() and raw_input() are implemented
           with dialogs.'''
        user_code = self.python_editor.GetValue()
        myGlobals = globals()
        myGlobals['raw_input'] = self.myRawInput
        myGlobals['input'] = self.myInput
        exec user_code in myGlobals
 
    def clear(self, event):
        '''Clears the output window'''
        self.output_window.SetValue("")

    def myRawInput(self, text):
        dlg = wx.TextEntryDialog(self, text, 'raw_input() request', '')
        if dlg.ShowModal() == wx.ID_OK:
            user_response = dlg.GetValue()
        dlg.Destroy()
        return user_response
    
    def myInput(self, text):
        dlg = wx.TextEntryDialog(self, text, 'input() request', '')
        if dlg.ShowModal() == wx.ID_OK:
            user_response = dlg.GetValue()
        dlg.Destroy()
        return eval(user_response)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self,parent, -1, title, size=(800, 600),
                    style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.app = EditorSashWindow(self)
        self.Show(True)

app = wx.PySimpleApp()
frame=MainWindow(None, 'Lightning Compiler')
app.MainLoop()
