"""
  a small program to run after the installation of python on windows
  adds the directory path to the python executable to the PATH env. variable
  with optional parameter remove, removes it
  you have to open a new command prompt to see the effects (echo %PATH%)
"""

import sys
import os
import time
import _winreg
import ctypes

def extend(pypath):
    '''
    extend(pypath) adds pypath to the PATH env. variable as defined in the 
    registry, and then notifies applications (e.g. the desktop) of this change.
    Already opened DOS-Command prompt are not updated. Newly opened will have the
    new path (inherited from the updated windows explorer desktop)
    '''
    hKey = _winreg.OpenKey (_winreg.HKEY_LOCAL_MACHINE, 
               r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 
               0, _winreg.KEY_READ | _winreg.KEY_SET_VALUE)
    
    value, typ = _winreg.QueryValueEx (hKey, "PATH")
    vals = value.split(';')
    assert isinstance(vals, list)
    if len(sys.argv) > 1 and sys.argv[1] == 'remove':
        try:
            vals.remove(pypath)
        except ValueError:
            print 'path element', pypath, 'not found'
            return
        print 'removing from PATH:', pypath
    else:
        if pypath in vals:
            print 'path element', pypath, 'already in PATH'
            return
        vals.append(pypath)
        print 'adding to PATH:', pypath
    _winreg.SetValueEx(hKey, "PATH", 0, typ, ';'.join(vals) )
    _winreg.FlushKey(hKey)
    # notify other programs
    SendMessage = ctypes.windll.user32.SendMessageW
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A
    SendMessage(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment')

    
def find_python():
    '''
    retrieves the commandline for .py extensions from the registry
    '''
    hKey = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, 
                           r'Python.File\shell\open\command') 
    # get the default value
    value, typ = _winreg.QueryValueEx (hKey, None)
    program = value.split('"')[1]
    if not program.lower().endswith(r'\python.exe'):
        return None
    return os.path.dirname(program)
    
pypath=find_python()
extend(pypath)
