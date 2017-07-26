"""
Enumerates active processes as seen under windows Task Manager on Win NT/2k/XP using PSAPI.dll
(new api for processes) and using ctypes.Use it as you please.

Based on information from http://support.microsoft.com/default.aspx?scid=KB;EN-US;Q175030&ID=KB;EN-US;Q175030

By Eric Koome
email ekoome@yahoo.com
license GPL
"""
from ctypes import *

#PSAPI.DLL
psapi = windll.psapi
#Kernel32.DLL
kernel = windll.kernel32

def EnumProcesses():
    arr = c_ulong * 256
    lpidProcess= arr()
    cb = sizeof(lpidProcess)
    cbNeeded = c_ulong()
    hModule = c_ulong()
    count = c_ulong()
    modname = c_buffer(30)
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    
    #Call Enumprocesses to get hold of process id's
    psapi.EnumProcesses(byref(lpidProcess),
                        cb,
                        byref(cbNeeded))
    
    #Number of processes returned
    nReturned = cbNeeded.value/sizeof(c_ulong())
    
    pidProcess = [i for i in lpidProcess][:nReturned]
    
    for pid in pidProcess:
        
        #Get handle to the process based on PID
        hProcess = kernel.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                                      False, pid)
        if hProcess:
            psapi.EnumProcessModules(hProcess, byref(hModule), sizeof(hModule), byref(count))
            psapi.GetModuleBaseNameA(hProcess, hModule.value, modname, sizeof(modname))
            print "".join([ i for i in modname if i != '\x00'])
            
            #-- Clean up
            for i in range(modname._length_):
                modname[i]='\x00'
            
            kernel.CloseHandle(hProcess)

if __name__ == '__main__':
    EnumProcesses()
