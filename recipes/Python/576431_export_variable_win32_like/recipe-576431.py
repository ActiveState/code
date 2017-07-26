"""
vim: set enc=utf-8

Author :  winterTTr
Mail   :  winterTTr@gmail.com
Desc   :  Tools for Operation on Win32 Environment variables
Module :  win32export.py
"""

import win32gui
import win32con
import win32api

def export ( name , value , update_system = True ):
    try :
        modifyVariableInRegister( name , value )
    except:
        return False

    if update_system :
        updateSystem()

    return True

def modifyVariableInRegister( name , value ):
    key = win32api.RegOpenKey( win32con.HKEY_CURRENT_USER,"Environment",0,win32con.KEY_ALL_ACCESS)
    if not key : raise
    win32api.RegSetValueEx( key , name , 0 , win32con.REG_SZ , value )
    win32api.RegCloseKey( key )

def updateSystem():
    rc,dwReturnValue = win32gui.SendMessageTimeout( win32con.HWND_BROADCAST , win32con.WM_SETTINGCHANGE , 0 , "Environment" , win32con.SMTO_ABORTIFHUNG, 5000)
