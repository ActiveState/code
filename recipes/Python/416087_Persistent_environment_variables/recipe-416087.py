from _winreg import *
import os, sys, win32gui, win32con

def queryValue(key, name):       
    value, type_id = QueryValueEx(key, name)
    return value

def show(key):
    for i in range(1024):                                           
        try:
            n,v,t = EnumValue(key, i)
            print '%s=%s' % (n, v)
        except EnvironmentError:
            break          

def main():
    try:
        path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        key = OpenKey(reg, path, 0, KEY_ALL_ACCESS)
        
        if len(sys.argv) == 1:
            show(key)
        else:
            name, value = sys.argv[1].split('=')
            if name.upper() == 'PATH':
                value = queryValue(key, name) + ';' + value
            if value:
                SetValueEx(key, name, 0, REG_EXPAND_SZ, value)
            else:
                DeleteValue(key, name)
            
        win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
                            
    except Exception, e:
        print e

    CloseKey(key)    
    CloseKey(reg)
    
if __name__=='__main__':    
    usage = \
"""
Usage:

Show all environment vsarisbles - enver
Add/Modify/Delete environment variable - enver <name>=[value]

If <name> is PATH enver will append the value prefixed with ;

If there is no value enver will delete the <name> environment variable

Note that the current command window will not be affected, 
only new command windows.
"""
    argc = len(sys.argv)
    if argc > 2 or (argc == 2 and sys.argv[1].find('=') == -1):
        print usage
        sys.exit()
        
    main()    
