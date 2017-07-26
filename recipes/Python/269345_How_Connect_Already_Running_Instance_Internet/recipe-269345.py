from win32com . client import Dispatch 
from win32gui import GetClassName

ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
ShellWindows = Dispatch ( ShellWindowsCLSID )

for shellwindow in ShellWindows :
    if GetClassName ( shellwindow . HWND ) == 'IEFrame' :
        print shellwindow 
        print shellwindow . LocationName
        print shellwindow . LocationURL
        print 50 * '-'
