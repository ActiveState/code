from win32gui import EnumWindows, SetWindowPos, GetDesktopWindow, \
     GetWindowRect, FindWindow, GetClassName, ShowWindow
import os, time
import pywintypes

def enumWinProc(h, lparams):
    
    if GetClassName(h) == 'ExploreWClass':
        lparams.append(h)

winList = []
EnumWindows(enumWinProc,winList)
winCnt = len(winList)
if winCnt == 0: # No Explorer running
    os.system('explorer.exe')
    while 1:
        try:
            FindWindow('ExploreWClass',None) #Wait for first instance to run
        except pywintypes.error,e:
            pass
        else:
            break
        time.sleep(0.1) # Sleep for a while before continuing
    os.system('explorer.exe') # Start second instance
elif winCnt == 1:
    os.system('explorer.exe') # Start second instance
time.sleep(2) # Wait for Explorer to run
winList = []
EnumWindows(enumWinProc,winList) # Get handles of running Explorer
hDesk = GetDesktopWindow()
(dLeft,dTop,dRight,dBottom) = GetWindowRect(hDesk) # Get desktop size
SetWindowPos(winList[0],0,dRight/2,0,dRight/2,dBottom,0) # Set the windows sizes
SetWindowPos(winList[1],0,0,0,dRight/2,dBottom,0)
ShowWindow(winList[0],1) #Show the windows
ShowWindow(winList[1],1)
    
