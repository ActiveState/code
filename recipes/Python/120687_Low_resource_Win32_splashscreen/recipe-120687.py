import win32gui
import win32api
import win32con
import struct

IDC_BITMAP = 1028

g_registeredClass = 0

class Splash:
    def __init__(self, bitmapPath):
        win32gui.InitCommonControls()
        self.hinst = win32api.GetModuleHandle(None)

        #retreive width and height from bitmap file, because GetObject does not work for bitmaps :-(
        f = open(bitmapPath, 'rb')
        hdrfm = '<18xii'
        self.bmWidth, self.bmHeight = struct.unpack(hdrfm, f.read(struct.calcsize(hdrfm)))
        f.close()

        self.hSplash = win32gui.LoadImage(self.hinst, bitmapPath, win32con.IMAGE_BITMAP, 
                                          0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
        
            
    def _RegisterWndClass(self):
        className = "PythonSplash"
        global g_registeredClass
        if not g_registeredClass:
            message_map = {}
            wc = win32gui.WNDCLASS()
            wc.SetDialogProc() # Make it a dialog class.
            self.hinst = wc.hInstance = win32api.GetModuleHandle(None)
            wc.lpszClassName = className
            wc.style = 0
            wc.hCursor = win32gui.LoadCursor( 0, win32con.IDC_ARROW )
            wc.hbrBackground = win32con.COLOR_WINDOW + 1
            wc.lpfnWndProc = message_map # could also specify a wndproc.
            wc.cbWndExtra = win32con.DLGWINDOWEXTRA + struct.calcsize("Pi")
            classAtom = win32gui.RegisterClass(wc)
            g_registeredClass = 1
        return className

    def _GetDialogTemplate(self, dlgClassName):
        style = win32con.WS_POPUP

        dlg = [ ["", (0, 0, 0, 0), style, None, (8, "MS Sans Serif"), None, dlgClassName], ]

        dlg.append([130, "", IDC_BITMAP, (0, 0, 0, 0), win32con.WS_VISIBLE | win32con.SS_BITMAP])

        return dlg

    def CreateWindow(self):
        self._DoCreate(win32gui.CreateDialogIndirect)

    def DoModal(self):
        return self._DoCreate(win32gui.DialogBoxIndirect)

    def _DoCreate(self, fn):
        message_map = {
            win32con.WM_INITDIALOG: self.OnInitDialog,
            win32con.WM_CLOSE: self.OnClose,
        }
        dlgClassName = self._RegisterWndClass()
        template = self._GetDialogTemplate(dlgClassName)
        return fn(self.hinst, template, 0, message_map)


    def OnInitDialog(self, hwnd, msg, wparam, lparam):
        self.hwnd = hwnd

        desktop = win32gui.GetDesktopWindow()
        dt_l, dt_t, dt_r, dt_b = win32gui.GetWindowRect(desktop)
        centre_x, centre_y = win32gui.ClientToScreen( desktop, ( (dt_r-dt_l)/2, (dt_b-dt_t)/2) )

        bmCtrl = win32gui.GetDlgItem(self.hwnd, IDC_BITMAP)
        win32gui.SendMessage(bmCtrl, win32con.STM_SETIMAGE, win32con.IMAGE_BITMAP, self.hSplash)

        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 
                              centre_x-(self.bmWidth/2), centre_y-(self.bmHeight/2), 
                              self.bmWidth, self.bmHeight, win32con.SWP_HIDEWINDOW)
        win32gui.SetForegroundWindow(self.hwnd)
        
        
    def Show(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
      
    def Timer(self, timeOut):
        import time
        time.sleep(timeOut)
        self.EndDialog()

    def EndDialogAfter(self, timeOut):
        #thread needed because win32gui does not expose SetTimer API
        import thread
        thread.start_new_thread(self.Timer, (timeOut, ))
    
    def EndDialog(self):
        win32gui.EndDialog(self.hwnd, 0)
        
    def OnClose(self, hwnd, msg, wparam, lparam):
        self.EndDialog()
    
if __name__=='__main__':
    s = Splash("skins\\splash.bmp")
    s.DoModal()
    
    # or use:
    #s.CreateWindow()
    #s.Show()
    #s.EndDialogAfter([timeout in seconds])
    #
    # (then make sure you PumpMessages() elsewhere
