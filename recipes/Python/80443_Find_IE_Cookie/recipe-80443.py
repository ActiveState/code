from string import lower, find
import re, os, glob
import win32api, win32con

def _getLocation():
    ''' Looks through the registry to find the current users Cookie folder. This is the folder IE uses. '''
    key = 'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    regkey = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, key, 0, win32con.KEY_ALL_ACCESS)
    num = win32api.RegQueryInfoKey(regkey)[1]
    for x in range(0, num):
        k = win32api.RegEnumValue(regkey, x)
        if k[0] == 'Cookies':
            return k[1]

def _getCookieFiles(location, name):
    ''' Rummages through all the files in the cookie folder, and returns only the ones whose file name, contains name. 
    Name can be the domain, for example 'activestate' will return all cookies for activestate. 
    Unfortunately it will also return cookies for domains like activestate.foo.com, but thats highly unlikely. '''
    filenm = os.path.join(location, '*%s*' % name)
    files = glob.glob(filenm)
    return files

def _findCookie(files, cookie_re):
    ''' Look through a group of files looking for a specific cookie,
    when we find it return, which means the first one found '''
    for file in files:
        data = open(file, 'r').read()
        m = cookie_re.search(data)
        if m: return m.group(1)

def findIECookie(domain, cookie):
    '''  Finds the ASPN Cookie from IE cookie files '''
    cookie_re = re.compile('%s\n(.*?)\n' % cookie)
    try: 
        l = _getLocation()
    except:
        # just print a debug
        print "Error pulling registry key"
        return None

    # Found the key, now find the files and look through them
    f = _getCookieFiles(l, domain)
    if f: 
        return _findCookie(f, cookie_re)
    else: 
        print "No cookies for that domain found"
        return None


if __name__=='__main__':
    print findIECookie(domain='kuro5hin', cookie='k5-new_session')from string 
