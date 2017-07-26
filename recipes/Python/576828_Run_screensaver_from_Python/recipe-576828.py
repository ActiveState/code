import os, win32com.client

def runScreensaver():
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
    colItems = objSWbemServices.ExecQuery("Select * from Win32_Desktop")
    for objItem in colItems:
        if objItem.ScreenSaverExecutable:
            os.system(objItem.ScreenSaverExecutable + " /start")
            break
