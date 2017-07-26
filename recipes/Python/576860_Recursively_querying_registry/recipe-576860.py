import win32api
import win32con

def regquerysubkeys(handle, key, keylist = []):
    """
    This function returns a recursively generated list of subkeys of a given 
    key in deletable order, see win32api.RegDeleteKey. 
    If an unexpected Exception occurs, it is raised!
    
    Parameters
    handle: one of the constants from win32con (e.g. win32con.HKEY_CURRENT_USER)
    key: a subkey within the handle as a string
    keylist: may be left empty, this is just neede for the recursion

    Returns
    keylist: a list with subkeys in deleteable order

    Sample call
    regquerysubkeys(win32con.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\")
    """
    #get registry handle
    reghandle = win32api.RegOpenKeyEx(handle, key, 0, win32con.KEY_READ)    
    try:
        i = 0
        #enumerates subkeys and recursively calls this function again
        while True:
           subkey = win32api.RegEnumKey(reghandle, i)
           i += 1
           #braintwister here ;-)
           regquerysubkeys(handle, key + subkey + "\\", keylist)
    except win32api.error as ex:
           #If no more subkeys can be found, we can append ourself
           if ex[0] == 259:
               keylist.append(key)
           #unexpected exception is raised
           else:
               raise
    finally:
        #do some cleanup and close the handle
        win32api.RegCloseKey(reghandle)
    #returns the generated list
    return keylist
