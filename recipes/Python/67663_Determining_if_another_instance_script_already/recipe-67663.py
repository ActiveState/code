from win32event import CreateMutex
from win32api import GetLastError
from winerror import ERROR_ALREADY_EXISTS
from sys import exit

handle = CreateMutex ( None, 1, 'A unique mutex name' )

if GetLastError ( ) == ERROR_ALREADY_EXISTS:
# take appropriate action if this is the second
# instance of this script; for example,
    print 'Oh! dear, I exist already.'
    exit ( 1 )
