import win32con
import sys
from ctypes import *

WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)

class WNDCLASS(Structure):
    _fields_ = [('style', c_uint),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', c_int),
                ('hIcon', c_int),
                ('hCursor', c_int),
                ('hbrBackground', c_int),
                ('lpszMenuName', c_char_p),
                ('lpszClassName', c_char_p)]

class RECT(Structure):
    _fields_ = [('left', c_long),
                ('top', c_long),
                ('right', c_long),
                ('bottom', c_long)]

class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', c_int),
                ('fErase', c_int),
                ('rcPaint', RECT),
                ('fRestore', c_int),
                ('fIncUpdate', c_int),
                ('rgbReserved', c_char * 32)]

class POINT(Structure):
    _fields_ = [('x', c_long),
                ('y', c_long)]
    
class MSG(Structure):
    _fields_ = [('hwnd', c_int),
                ('message', c_uint),
                ('wParam', c_int),
                ('lParam', c_int),
                ('time', c_int),
                ('pt', POINT)]

def ErrorIfZero(handle):
    if handle == 0:
        raise WinError
    else:
        return handle

def MainWin():
    CreateWindowEx = windll.user32.CreateWindowExA
    CreateWindowEx.argtypes = [c_int, c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int]
    CreateWindowEx.restype = ErrorIfZero

    # Define Window Class
    wndclass = WNDCLASS()
    wndclass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wndclass.lpfnWndProc = WNDPROC(WndProc)
    wndclass.cbClsExtra = wndclass.cbWndExtra = 0
    wndclass.hInstance = windll.kernel32.GetModuleHandleA(c_int(win32con.NULL))
    wndclass.hIcon = windll.user32.LoadIconA(c_int(win32con.NULL), c_int(win32con.IDI_APPLICATION))
    wndclass.hCursor = windll.user32.LoadCursorA(c_int(win32con.NULL), c_int(win32con.IDC_ARROW))
    wndclass.hbrBackground = windll.gdi32.GetStockObject(c_int(win32con.WHITE_BRUSH))
    wndclass.lpszMenuName = None
    wndclass.lpszClassName = "MainWin"
    # Register Window Class
    if not windll.user32.RegisterClassA(byref(wndclass)):
        raise WinError()
    # Create Window
    hwnd = CreateWindowEx(0,
                          wndclass.lpszClassName,
                          "Python Window",
                          win32con.WS_OVERLAPPEDWINDOW,
                          win32con.CW_USEDEFAULT,
                          win32con.CW_USEDEFAULT,
                          win32con.CW_USEDEFAULT,
                          win32con.CW_USEDEFAULT,
                          win32con.NULL,
                          win32con.NULL,
                          wndclass.hInstance,
                          win32con.NULL)
    # Show Window
    windll.user32.ShowWindow(c_int(hwnd), c_int(win32con.SW_SHOWNORMAL))
    windll.user32.UpdateWindow(c_int(hwnd))
    # Pump Messages
    msg = MSG()
    pMsg = pointer(msg)
    NULL = c_int(win32con.NULL)
    
    while windll.user32.GetMessageA( pMsg, NULL, 0, 0) != 0:
        windll.user32.TranslateMessage(pMsg)
        windll.user32.DispatchMessageA(pMsg)

    return msg.wParam
    
def WndProc(hwnd, message, wParam, lParam):
    ps = PAINTSTRUCT()
    rect = RECT()
    
    if message == win32con.WM_PAINT:
        hdc = windll.user32.BeginPaint(c_int(hwnd), byref(ps))
        windll.user32.GetClientRect(c_int(hwnd), byref(rect))
        windll.user32.DrawTextA(c_int(hdc),
                                "Python Powered Windows" ,
                                c_int(-1), byref(rect), 
                                win32con.DT_SINGLELINE|win32con.DT_CENTER|win32con.DT_VCENTER)
        windll.user32.EndPaint(c_int(hwnd), byref(ps))
        return 0
    elif message == win32con.WM_DESTROY:
        windll.user32.PostQuitMessage(0)
        return 0

    return windll.user32.DefWindowProcA(c_int(hwnd), c_int(message), c_int(wParam), c_int(lParam))

if __name__=='__main__':
    sys.exit(MainWin())
