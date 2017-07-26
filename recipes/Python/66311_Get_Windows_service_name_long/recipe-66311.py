import win32api
import win32con

def GetShortName(longName):
    # looks up a services name
    # from the display name
    hkey = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services", 0, win32con.KEY_ALL_ACCESS)
    num = win32api.RegQueryInfoKey(hkey)[0]

    # loop through number of subkeys
    for x in range(0, num):
        # find service name, open subkey
        svc = win32api.RegEnumKey(hkey, x)
        skey = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, \
"SYSTEM\\CurrentControlSet\\Services\\%s" % svc, 0, win32con.KEY_ALL_ACCESS)
        try:
            # find short name
            shortName = str(win32api.RegQueryValueEx(skey, "DisplayName")[0])
            if shortName == longName:
                return svc
        except win32api.error: 
            # in case there is no key called DisplayName
            pass
    return None

if __name__=='__main__':
    assert(GetShortName('Windows Time') == 'W32Time')
    assert(GetShortName('FoobarService') == None)
