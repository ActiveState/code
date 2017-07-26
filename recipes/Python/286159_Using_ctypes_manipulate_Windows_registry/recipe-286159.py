# Creating the following registry key
# HKEY_CURRENT_USER\Please_Delete_Me\Level_1\Level_2

from ctypes import *
import win32con

advapi32 = oledll . LoadLibrary ( 'advapi32.dll' )
newKey = c_ulong ( )

nextKey = win32con . HKEY_CURRENT_USER
for subKey in [ 'Please_Delete_Me', 'Level_1', 'Level_2' ] :
    advapi32 . RegCreateKeyA ( nextKey, c_char_p ( subKey ), byref ( newKey ) )
    nextKey = newKey

advapi32 . RegCloseKey ( newKey )

# Registering and Unregistering a DLL

from ctypes import windll

dll = windll[<path-to-dll> ]
result = dll.DllRegisterServer()
result = dll.DllUnregisterServer()
