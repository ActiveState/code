# This script demonstrates changing the color of the menu bar/individual
# menus in a wxPython UI for the Win32 platform
# Requires
# - ctypes to access the user32 and gdi32 modules, to set up structures
#   and other win32 oriented helper functions
# - pywin32 module, to use win32con and access constants (this is optional
#   but really handy). Alternative is to get the values of the constants
#   from MSDN.

import wx
import win32con
from ctypes import *
import sys

# Structure passed to CreateSolidBrush function
# Represents RGB
class COLORREF(Structure):
    _fields_ = [
    ("byRed", c_byte),
    ("byGreen", c_byte),
    ("byBlue", c_byte)
    ]

# Menu structure used in calls to SetMenuInfo
class MENUINFO(Structure):
    _fields_ = [
    ("cbSize", c_long),
    ("fMask", c_long),
    ("dwStyle", c_long),
    ('cyMax', c_long),
    ("hbrBack", c_long),
    ("dwContextHelpID", c_long),
    ("dwMenuData", c_long)
    ]

class TestFrame(wx.Frame):
    """
    Subclass of wx.Frame that presents the app's main window
    """
    def __init__(self, parent, id=-1, title='Test Menu',
            pos=wx.DefaultPosition,
            size=wx.DefaultSize, 
            style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE,
            name='TestFrame',
            shadesubmenus=False):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
        self.bShadeSubMenus = shadesubmenus
        menubar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(-1, 'Open', 'Open new file')
        menu1.Append(-1, 'Exit', 'Quit application')
        menubar.Append(menu1, 'File')
        menu2 = wx.Menu()
        menu2.Append(-1, 'About', 'About')
        menubar.Append(menu2, 'Help')
        self.SetMenuBar(menubar)
        self.Show(True)
        self.size = self.GetSize()
        # Get my windows handle - hwnd
        self.hwnd = self.GetHandle()
        self.ChangeMenuBarColor()

    def ChangeMenuBarColor(self):
        """
        Changes the background color of the menubar and optionally gives 
        different colors to menu items
        """
        user32 = windll.user32
        DrawMenuBar = user32.DrawMenuBar
        GetMenu = user32.GetMenu
        GetSubMenu = user32.GetSubMenu
        GetSystemMenu = user32.GetSystemMenu
        SetMenuInfo = user32.SetMenuInfo
        GetMenuInfo = user32.GetMenuInfo
        gdi32 = windll.gdi32
        CreateSolidBrush = gdi32.CreateSolidBrush
        # Instantiate MENUINFO
        menuinfo = MENUINFO()
        # Important to set the size
        menuinfo.cbSize = sizeof(MENUINFO)
        menuinfo.fMask = win32con.MIM_BACKGROUND
        if not self.bShadeSubMenus:
            menuinfo.fMask |= win32con.MIM_APPLYTOSUBMENUS
        menuinfo.hbrBack = CreateSolidBrush(COLORREF(255, 0, 0))
        # Important! Pass *pointer* of the menuinfo instance to the win32 call
        SetMenuInfo(GetMenu(self.hwnd), pointer(menuinfo))
        if self.bShadeSubMenus:
            menuinfo.fMask = win32con.MIM_BACKGROUND | win32con.MIM_APPLYTOSUBMENUS
            menuinfo.hbrBack = CreateSolidBrush(COLORREF(255, 255, 0))
            SetMenuInfo(GetSubMenu(GetMenu(self.hwnd), 0), pointer(menuinfo))
            menuinfo.fMask = win32con.MIM_BACKGROUND | win32con.MIM_APPLYTOSUBMENUS
            menuinfo.hbrBack = CreateSolidBrush(COLORREF(128, 255, 128))
            SetMenuInfo(GetSubMenu(GetMenu(self.hwnd), 1), pointer(menuinfo))
        DrawMenuBar(self.hwnd)

if __name__ == '__main__':
    try:
        bShadeSubMenus = sys.argv[1]
    except:
        bShadeSubMenus = False
    app = wx.PySimpleApp()
    f = TestFrame(None, shadesubmenus=bShadeSubMenus)
    app.MainLoop()
