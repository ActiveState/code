from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS

class singleinstance:
    """ Limits application to single instance """

    def __init__(self):
        self.mutexname = "testmutex_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}"
        self.mutex = CreateMutex(None, False, self.mutexname)
        self.lasterror = GetLastError()
    
    def aleradyrunning(self):
        return (self.lasterror == ERROR_ALREADY_EXISTS)
        
    def __del__(self):
        if self.mutex:
            CloseHandle(self.mutex)


#---------------------------------------------#
# sample usage:
#

from singleinstance import singleinstance
from sys import exit

# do this at beginnig of your application
myapp = singleinstance()

# check is another instance of same program running
if myapp.aleradyrunning():
    print "Another instance of this program is already running"
    exit(0)

# not running, safe to continue...
print "No another instance is running, can continue here"
