'''
Created on Jun 22, 2009

@author: mgarrana
'''
from _winreg import *
import shutil
from win32net import NetLocalGroupGetMembers
import win32api
mapping = { "HKLM":HKEY_LOCAL_MACHINE, "HKCU":HKEY_CURRENT_USER, "HKU":HKEY_USERS }

def readSubKeys(hkey, regPath):
    if not pathExists(hkey, regPath):
        return -1
    reg = OpenKey(mapping[hkey], regPath)
    subKeys = []
    noOfSubkeys = QueryInfoKey(reg)[0]
    for i in range(0, noOfSubkeys):
        subKeys.append(EnumKey(reg, i))
    CloseKey(reg)
    return subKeys

def pathExists(hkey, regPath):
    try:
        reg = OpenKey(mapping[hkey], regPath)
    except WindowsError:
        return False
    CloseKey(reg)
    return True                    


def Dumpfile(): 
    fv.write('##########')
    fv.write('\n')
    fv.write("local Administrators on machine ")
    fv.write(host)
    fv.write(" are : ....\n\n")
    result,t,r= NetLocalGroupGetMembers(None,"Administrators",1)
    for item in result:
        fv.write(str(item))
        fv.write('\n')
    fv.write('\n\n')
    fv.write ("##########\n")
    fv.write('the following software is installed on ')
    fv.write(host)
    fv.write(': .... \n\n')
    listofsoft=readSubKeys("HKLM", "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    listofsoft.sort()
    for software in listofsoft:
        fv.write(str(software))
        fv.write('\n')
    fv.close()
    shutil.copy(srcfile,r"\\10.1.1.12\gms")
    win32api.DeleteFile(srcfile)



def GeneralInfo():
    global host,fv,srcfile
    host=win32api.GetComputerName()
    srcfile="C:\\"+host
    fv=open(srcfile,'w')
    fv.write("Machine NAME : ")
    fv.write(host)
    fv.write('\n')
    fv.write("the machine is joined to the domain : ")
    fv.write(str(win32api.GetDomainName()))
    fv.write('\n')
    fv.write("these settings were logged for user : ")
    fv.write(str(win32api.GetUserName()))
    fv.write('\n')
    fv.write("System Time is : ")
    fv.write(str(win32api.GetSystemTime()))
    fv.write('\n\n\n')

try:   
    GeneralInfo()    
    Dumpfile()
except:
    pass

    
