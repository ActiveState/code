from subprocess import Popen
from win32com.client import GetObject
from string import replace

def isRunning(app):
    WMI = GetObject('winmgmts:')
    app = replace(app,"\\","\\\\")
    return(len(WMI.ExecQuery('select * from Win32_Process where ExecutablePath="%s"'%app))!=0)

def execAll(appList):
    for app in appList:
        if not isRunning(app):
            Popen(app)

def killAll(appList):
    WMI = GetObject('winmgmts:')
    for app in appList:
        app = replace(app,"\\","\\\\")
        processes = WMI.ExecQuery('select * from Win32_Process where ExecutablePath="%s"'%app)
        for process in processes:
            try:
                process.Terminate()
            except TypeError:
                raise

def main():
    myApps = ["C:\\Program Files\\Pidgin\\pidgin.exe",
        "C:\\Program Files\\Opera 10\\opera.exe",
        "C:\\Program Files\\Vuze\\Azureus.exe",
        "C:\\Program Files\\Winamp\\winamp.exe"]
    unwantedApps = ["C:\\WINDOWS\\system32\\notepad.exe"]
    execAll(myApps)
    killAll(unwantedApps)
    
if __name__ == "__main__":
    main()
