"""
PathCatcher is a Windows utility that allows one to right-click on 
a folder or a file in Explorer and save its path to the clipboard.

If this module is run by itself, it installs PathCatcher to the registry.
After it is installed, when one clicks on a file or folder, "PathCatcher" 
appears in the right-click menu.

This module also contains some useful code for accessing the Windows
clipboard and registry.

Requires ctypes -- download from SourceForge.

Jack Trainor 2007
"""
import sys
import os, os.path
import win32api
import win32con
import ctypes
import time

""" Abbreviations for readability """
OpenClipboard = ctypes.windll.user32.OpenClipboard
EmptyClipboard = ctypes.windll.user32.EmptyClipboard
GetClipboardData = ctypes.windll.user32.GetClipboardData
SetClipboardData = ctypes.windll.user32.SetClipboardData
CloseClipboard = ctypes.windll.user32.CloseClipboard
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
memcpy = ctypes.cdll.msvcrt.memcpy

""" Windows Clipboard utilities """
def GetClipboardText():
    text = ""
    if OpenClipboard(0):
        hClipMem = GetClipboardData(win32con.CF_TEXT)
        GlobalLock.restype = ctypes.c_char_p   
        text = GlobalLock(hClipMem)
        GlobalUnlock(hClipMem)
        CloseClipboard()
    return text

def SetClipboardText(text):
    buffer = ctypes.c_buffer(text)      
    bufferSize = ctypes.sizeof(buffer)
    hGlobalMem = GlobalAlloc(win32con.GHND, bufferSize)
    GlobalLock.restype = ctypes.c_void_p                        
    lpGlobalMem = GlobalLock(hGlobalMem)
    memcpy(lpGlobalMem, ctypes.addressof(buffer), bufferSize) 
    GlobalUnlock(hGlobalMem)
    if OpenClipboard(0):
        EmptyClipboard()
        SetClipboardData(win32con.CF_TEXT, hGlobalMem)
        CloseClipboard()

""" Windows Registry utilities """
def OpenRegistryKey(hiveKey, key):
    keyHandle = None
    try:
        curKey = ""
        keyItems = key.split('\\')
        for keyItem in keyItems:
            if curKey:
                curKey = curKey + "\\" + keyItem
            else:
                curKey = keyItem
            keyHandle = win32api.RegCreateKey(hiveKey, curKey)
    except Exception, e:
        keyHandle = None
        print "OpenRegistryKey failed:", e
    return keyHandle

def ReadRegistryValue(hiveKey, key, name):
    """ Simple api to read one value from Windows registry. 
    If 'name' is empty string, reads default value."""
    data = typeId = None
    try:
        hKey = win32api.RegOpenKeyEx(hiveKey, key, 0, win32con.KEY_ALL_ACCESS)
        data, typeId = win32api.RegQueryValueEx(hKey, name)
        win32api.RegCloseKey(hKey)
    except Exception, e:
        print "ReadRegistryValue failed:", e
    return data, typeId

def WriteRegistryValue(hiveKey, key, name, typeId, data):
    """ Simple api to write one value to Windows registry. 
    If 'name' is empty string, writes to default value."""
    try:
        keyHandle = OpenRegistryKey(hiveKey, key)
        win32api.RegSetValueEx(keyHandle, name, 0, typeId, data)
        win32api.RegCloseKey(keyHandle)
    except Exception, e:
        print "WriteRegistry failed:", e

""" misc utilities """
def GetPythonwExePath():
    """ Get path to current version of pythonw.exe """
    pythonExePath = ""
    try:
        pythonwExeName = "pythonw.exe"
        pythonInstallHiveKey = win32con.HKEY_LOCAL_MACHINE
        pythonInstallKey = r"Software\Python\PythonCore\%s\InstallPath" % sys.winver
        pythonInstallDir, typeId = ReadRegistryValue(pythonInstallHiveKey, pythonInstallKey, "")
        pythonwExePath = os.path.join(pythonInstallDir, pythonwExeName)
    except Exception, e:
        print "GetPythonExePath failed:", e
    return pythonwExePath
  
def GetModulePath(): 
    """ Get path to this module """
    return GetModulePath.func_code.co_filename

def WriteLastTime():
    secsString = str(time.time())
    WriteRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\PathCatcher\time", "", win32con.REG_SZ, secsString)

def ReadLastTime():
    secs = 0.0
    secsString, dateTypId = ReadRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\PathCatcher\time", "")
    if secsString:
        secs = float(secsString)
    return secs

def AccumulatePaths(path):
    """ Windows creates a Python process for each selected file on right-click.
    Check to see if this invocation is part of current batch and accumulate to clipboard """
    lastTime = ReadLastTime()
    now = time.time()
    if (now - lastTime) < 1.0:
        SetClipboardText(GetClipboardText() + "\n" + path)
    else:
        SetClipboardText(path)
    WriteLastTime()
     
#########################################################
def InstallPathCatcher():
    """ Installs PathCatcher to the Windows registry """
    command = '"%s" "%s" "%s"' % (GetPythonwExePath(), GetModulePath(), "%1")
    WriteRegistryValue(win32con.HKEY_CLASSES_ROOT, r"*\shell\PathCatcher\Command", "", win32con.REG_SZ, command)
    WriteRegistryValue(win32con.HKEY_CLASSES_ROOT, r"Folder\shell\PathCatcher\Command", "", win32con.REG_SZ, command)
    WriteLastTime()
    
#########################################################
if __name__ == "__main__":
    if len(sys.argv) > 1:
        """ If invoked through a right-click, there will be a path argument """
        path = sys.argv[1]
        AccumulatePaths(path)
    else:
        """ If module is run by itself, install PathCatcher to registry """
        InstallPathCatcher()
        raw_input("PathCatcher installed.\nPress RETURN...")
