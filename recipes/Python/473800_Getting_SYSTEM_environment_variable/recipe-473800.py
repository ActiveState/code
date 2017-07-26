# -*- coding: Windows-1251 -*-
'''
getenv_system.py

Get SYSTEM environment value, as if running under Service or SYSTEM account

Author: Denis Barmenkov <denis.barmenkov@gmail.com>

Copyright: this code is free, but if you want to use it, 
           please keep this multiline comment along with function source. 
           Thank you.

2006-01-28 15:30
'''

import os, win32api, win32con

def getenv_system(varname, default=''):
    v = default
    try:
        rkey = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment')
        try:
            v = str(win32api.RegQueryValueEx(rkey, varname)[0])
            v = win32api.ExpandEnvironmentStrings(v)
        except:
            pass
    finally:
        win32api.RegCloseKey(rkey)
    return v

print 'SYSTEM.TEMP => %s' % getenv_system('TEMP')
print 'USER.TEMP   => %s' % os.getenv('TEMP')
