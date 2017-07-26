import os
import sys
import ctypes
from ctypes import Structure
from ctypes import byref
import ctypes.wintypes as wintypes
from ctypes import addressof

FILE_ATTRIBUTE_DIRECTORY = 16
OPEN_EXISTING = 3
MAX_PATH = 260

GetLastError = ctypes.windll.kernel32.GetLastError

class FILETIME(Structure):
  _fields_ = [("dwLowDateTime", wintypes.DWORD),
              ("dwHighDateTime", wintypes.DWORD)]

class WIN32_FIND_DATAW(Structure):
  _fields_ = [("dwFileAttributes", wintypes.DWORD),
              ("ftCreationTime", FILETIME),
              ("ftLastAccessTime", FILETIME),
              ("ftLastWriteTime", FILETIME),
              ("nFileSizeHigh", wintypes.DWORD),
              ("nFileSizeLow", wintypes.DWORD),
              ("dwReserved0", wintypes.DWORD),
              ("dwReserved1", wintypes.DWORD),
              ("cFileName", wintypes.WCHAR * MAX_PATH),
              ("cAlternateFileName", wintypes.WCHAR * 20)]

def windows_walk(folder):
    folder = unicode(folder)
    if not folder.startswith(u'\\\\?\\'):
        if folder.startswith(u'\\\\'):
            # network drive
            folder = u'\\\\?\\UNC' + folder[1:]
        else:
            # local drive
            folder = u'\\\\?\\' + folder

    dirs = []
    files = []
    data = WIN32_FIND_DATAW()
    gle = 0
    h = ctypes.windll.kernel32.FindFirstFileW(os.path.join(folder, u'*'), byref(data))
    gle = ctypes.windll.kernel32.GetLastError()
    if h < 0:
        ctypes.windll.kernel32.FindClose(h)
        if not sys.stderr.isatty():
            print >> sys.stderr, 'Failed to find first file %s' % (os.path.join(folder, u'*'),)
        if gle != 5: # access denied.
            raise WindowsError('FindFirstFileW %s, Error: %d' % (folder, ctypes.windll.kernel32.GetLastError()))
        return
        
    if data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY:
        if data.cFileName not in (u'.', u'..'):
            dirs.append(data.cFileName[:])
    else:
        files.append(data.cFileName[:])

    try:
        while ctypes.windll.kernel32.FindNextFileW(h, byref(data)):
            if data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY:
                if data.cFileName not in (u'.', u'..'):
                    dirs.append(data.cFileName[:])
            else:
                files.append(data.cFileName[:])
    except WindowsError as e:
        if not sys.stderr.isatty():
            print >> sys.stderr, 'Failed to find next file %s, handle %d, buff addr: 0x%x' % (os.path.join(folder, u'*'), h, addressof(data))
        
        
    ctypes.windll.kernel32.FindClose(h)
    yield folder, dirs, files
    for d in dirs:
        for base, ds, fs in windows_walk(os.path.join(folder, d)):
            yield base, ds, fs

if __name__=='__main__':
    for root, dirs, files in windows_walk(os.getcwdu()):
        for f in files:
            abspath = os.path.join(root, f)
            print abspath
