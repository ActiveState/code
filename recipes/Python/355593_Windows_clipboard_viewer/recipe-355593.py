import wx
import win32api
import win32gui
import win32con
import win32clipboard

class TestFrame (wx.Frame):
    def __init__ (self):
        wx.Frame.__init__ (self, None, title="Clipboard viewer", size=(250,150))

        self.first   = True
        self.nextWnd = None

        # Get native window handle of this wxWidget Frame.
        self.hwnd    = self.GetHandle ()

        # Set the WndProc to our function.
        self.oldWndProc = win32gui.SetWindowLong (self.hwnd,
                                                  win32con.GWL_WNDPROC,
                                                  self.MyWndProc)

        try:
            self.nextWnd = win32clipboard.SetClipboardViewer (self.hwnd)
        except win32api.error:
            if win32api.GetLastError () == 0:
                # information that there is no other window in chain
                pass
            else:
                raise

    def MyWndProc (self, hWnd, msg, wParam, lParam):
        if msg == win32con.WM_CHANGECBCHAIN:
            self.OnChangeCBChain (msg, wParam, lParam)
        elif msg == win32con.WM_DRAWCLIPBOARD:
            self.OnDrawClipboard (msg, wParam, lParam)

        # Restore the old WndProc. Notice the use of win32api
        # instead of win32gui here. This is to avoid an error due to
        # not passing a callable object.
        if msg == win32con.WM_DESTROY:
            if self.nextWnd:
               win32clipboard.ChangeClipboardChain (self.hwnd, self.nextWnd)
            else:
               win32clipboard.ChangeClipboardChain (self.hwnd, 0)

            win32api.SetWindowLong (self.hwnd,
                                    win32con.GWL_WNDPROC,
                                    self.oldWndProc)

        # Pass all messages (in this case, yours may be different) on
        # to the original WndProc
        return win32gui.CallWindowProc (self.oldWndProc,
                                        hWnd, msg, wParam, lParam)

    def OnChangeCBChain (self, msg, wParam, lParam):
        if self.nextWnd == wParam:
           # repair the chain
           self.nextWnd = lParam
        if self.nextWnd:
           # pass the message to the next window in chain
           win32api.SendMessage (self.nextWnd, msg, wParam, lParam)

    def OnDrawClipboard (self, msg, wParam, lParam):
        if self.first:
           self.first = False
        else:
           print "clipboard content changed"
        if self.nextWnd:
           # pass the message to the next window in chain
           win32api.SendMessage (self.nextWnd, msg, wParam, lParam)

app   = wx.PySimpleApp ()
frame = TestFrame ()
frame.Show ()
app.MainLoop ()
