from ctypes import c_long , c_int , c_uint , c_char , c_ubyte , c_char_p , c_void_p, c_size_t, c_ulong, c_wchar
from ctypes import windll
from ctypes import Structure
from ctypes import sizeof , POINTER , pointer , cast

# const variable
TH32CS_SNAPPROCESS = 2
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPTHREAD = 0x00000004

STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)

MAX_PATH=260
MAX_MODULE_NAME32 = 255

# originally just PROCESSENTRY32 
class PROCESSENTRY32A(Structure):
    _fields_ = [ ( 'dwSize' , c_ulong ) , 
                 ( 'cntUsage' , c_ulong) ,
                 ( 'th32ProcessID' , c_ulong) ,
                 ( 'th32DefaultHeapID' , c_size_t) ,
                 ( 'th32ModuleID' , c_ulong) ,
                 ( 'cntThreads' , c_ulong) ,
                 ( 'th32ParentProcessID' , c_ulong) ,
                 ( 'pcPriClassBase' , c_long) ,
                 ( 'dwFlags' , c_ulong) ,
                 ( 'szExeFile' , c_char * MAX_PATH ) ]

# c_wchar instead of c_char is the only difference
class PROCESSENTRY32W(Structure):
    _fields_ = [ ( 'dwSize' , c_ulong ) , 
                 ( 'cntUsage' , c_ulong) ,
                 ( 'th32ProcessID' , c_ulong) ,
                 ( 'th32DefaultHeapID' , c_size_t) ,
                 ( 'th32ModuleID' , c_ulong) ,
                 ( 'cntThreads' , c_ulong) ,
                 ( 'th32ParentProcessID' , c_ulong) ,
                 ( 'pcPriClassBase' , c_long) ,
                 ( 'dwFlags' , c_ulong) ,
                 ( 'szExeFile' , c_wchar * MAX_PATH ) ] 

# originally just MODULEENTRY32
class MODULEENTRY32A(Structure):
    _fields_ = [ ( 'dwSize' , c_ulong ) , 
                ( 'th32ModuleID' , c_ulong ),
                ( 'th32ProcessID' , c_ulong ),
                ( 'GlblcntUsage' , c_ulong ),
                ( 'ProccntUsage' , c_ulong ) ,
                ( 'modBaseAddr' , c_size_t ) , #POINTER(c_ubyte) in MSDN
                ( 'modBaseSize' , c_ulong ) , 
                ( 'hModule' , c_void_p ) ,
                ( 'szModule' , c_char * (MAX_MODULE_NAME32+1) ),
                ( 'szExePath' , c_char * MAX_PATH ) ]

# c_wchar instead of c_char is the only difference
class MODULEENTRY32W(Structure):
    _fields_ = [ ( 'dwSize' , c_ulong ) , 
                ( 'th32ModuleID' , c_ulong ),
                ( 'th32ProcessID' , c_ulong ),
                ( 'GlblcntUsage' , c_ulong ),
                ( 'ProccntUsage' , c_ulong ) ,
                ( 'modBaseAddr' , c_size_t ) , #POINTER(c_ubyte) in MSDN
                ( 'modBaseSize' , c_ulong ) , 
                ( 'hModule' , c_void_p ) ,
                ( 'szModule' , c_wchar * (MAX_MODULE_NAME32+1) ),
                ( 'szExePath' , c_wchar * MAX_PATH ) ]
                
class THREADENTRY32(Structure):
    _fields_ = [
        ('dwSize' , c_long ),
        ('cntUsage' , c_long),
        ('th32ThreadID' , c_long),
        ('th32OwnerProcessID' , c_long),
        ('tpBasePri' , c_long),
        ('tpDeltaPri' , c_long),
        ('dwFlags' , c_long) ]





# forigen function
## CreateToolhelp32Snapshot
CreateToolhelp32Snapshot= windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.reltype = c_long
CreateToolhelp32Snapshot.argtypes = [ c_ulong , c_ulong ]


## Process32First
Process32FirstA = windll.kernel32.Process32First
Process32FirstA.argtypes = [ c_void_p , POINTER( PROCESSENTRY32A ) ]
Process32FirstA.rettype = c_int

## Process32FirstW
Process32FirstW = windll.kernel32.Process32FirstW
Process32FirstW.argtypes = [ c_void_p , POINTER( PROCESSENTRY32W ) ]
Process32FirstW.rettype = c_int

## Process32Next
Process32NextA = windll.kernel32.Process32Next
Process32NextA.argtypes = [ c_void_p , POINTER(PROCESSENTRY32A) ]
Process32NextA.rettype = c_int

## Process32NextW
Process32NextW = windll.kernel32.Process32NextW
Process32NextW.argtypes = [ c_void_p , POINTER(PROCESSENTRY32W) ]
Process32NextW.rettype = c_int

## OpenProcess
OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = [ c_ulong , c_int , c_ulong ]
OpenProcess.rettype = c_void_p

## GetPriorityClass
GetPriorityClass = windll.kernel32.GetPriorityClass
GetPriorityClass.argtypes = [ c_void_p ]
GetPriorityClass.rettype = c_long

## CloseHandle
CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [ c_void_p ]
CloseHandle.rettype = c_int

## Module32First
Module32FirstA = windll.kernel32.Module32First
Module32FirstA.argtypes = [ c_void_p , POINTER(MODULEENTRY32A) ]
Module32FirstA.rettype = c_int

## Module32FirstW
Module32FirstW = windll.kernel32.Module32FirstW
Module32FirstW.argtypes = [ c_void_p , POINTER(MODULEENTRY32W) ]
Module32FirstW.rettype = c_int

## Module32Next
Module32NextA = windll.kernel32.Module32Next
Module32NextA.argtypes = [ c_void_p , POINTER(MODULEENTRY32A) ]
Module32NextA.rettype = c_int

## Module32NextW
Module32NextW = windll.kernel32.Module32NextW
Module32NextW.argtypes = [ c_void_p , POINTER(MODULEENTRY32W) ]
Module32NextW.rettype = c_int

## Thread32First
Thread32First = windll.kernel32.Thread32First
Thread32First.argtypes = [ c_void_p , POINTER(THREADENTRY32) ]
Thread32First.rettype = c_int

## Thread32Next
Thread32Next = windll.kernel32.Thread32Next
Thread32Next.argtypes = [ c_void_p , POINTER(THREADENTRY32) ]
Thread32Next.rettype = c_int

## GetLastError
GetLastError = windll.kernel32.GetLastError
GetLastError.rettype = c_ulong


use_unicode=True
if use_unicode:
    Process32First=Process32FirstW
    Process32Next=Process32NextW
    Module32First=Module32FirstW
    Module32Next=Module32NextW
    PROCESSENTRY32=PROCESSENTRY32W
    MODULEENTRY32=MODULEENTRY32W
else: #ANSI version
    Process32First=Process32FirstA
    Process32Next=Process32NextA
    Module32First=Module32FirstA
    Module32Next=Module32NextA
    PROCESSENTRY32=PROCESSENTRY32A
    MODULEENTRY32=MODULEENTRY32A


def ListProcessModules( ProcessID ):
    hModuleSnap = c_void_p(0)
    me32 = MODULEENTRY32()
    me32.dwSize = sizeof( MODULEENTRY32 )
    hModuleSnap = CreateToolhelp32Snapshot( TH32CS_SNAPMODULE, ProcessID )

    ret = Module32First( hModuleSnap, pointer(me32) )
    if ret == 0 :
        print('ListProcessModules() Error on Module32First[%d]' % GetLastError())
        CloseHandle( hModuleSnap )
        return False 

    while ret :
        print("   MODULE NAME:     %s"%             me32.szModule) 
        print("   executable     = %s"%             me32.szExePath) 
        print("   process ID     = 0x%08X"%         me32.th32ProcessID) 
        print("   ref count (g)  =     0x%04X"%     me32.GlblcntUsage) 
        print("   ref count (p)  =     0x%04X"%     me32.ProccntUsage)
        print("   base address   = 0x%08X"%         me32.modBaseAddr) 
        print("   base size      = %d"%             me32.modBaseSize) 

        ret = Module32Next( hModuleSnap , pointer(me32) )

    CloseHandle( hModuleSnap )
    return True




def ListProcessThreads( ProcessID ):
    hThreadSnap = c_void_p(0)
    te32 = THREADENTRY32 ()
    te32.dwSize = sizeof(THREADENTRY32 )

    hThreadSnap = CreateToolhelp32Snapshot( TH32CS_SNAPTHREAD, 0 )

    ret = Thread32First( hThreadSnap, pointer(te32) )

    if ret == 0 :
        print('ListProcessThreads() Error on Thread32First[%d]' % GetLastError())
        CloseHandle( hThreadSnap )
        return False

    while ret :
        if te32.th32OwnerProcessID == ProcessID : 
            print("   THREAD ID      = 0x%08X"% te32.th32ThreadID) 
            print("   base priority  = %d"% te32.tpBasePri) 
            print("   delta priority = %d"% te32.tpDeltaPri) 

        ret = Thread32Next( hThreadSnap, pointer(te32) )

    CloseHandle( hThreadSnap )
    return True
    






# main
if __name__ == '__main__' :
    hProcessSnap = c_void_p(0)
    hProcessSnap = CreateToolhelp32Snapshot( TH32CS_SNAPPROCESS , 0 )


    pe32 = PROCESSENTRY32()
    pe32.dwSize = sizeof( PROCESSENTRY32 )
    ret = Process32First( hProcessSnap , pointer( pe32 ) )

    while ret :
        print("")
        print("==================================================")
        print("Process Name : %s " % pe32.szExeFile)
        print("--------------------------------------------------")

        hProcess = OpenProcess( PROCESS_ALL_ACCESS , 0 , pe32.th32ProcessID )
        dwPriorityClass = GetPriorityClass( hProcess )
        if dwPriorityClass == 0 :
            CloseHandle( hProcess )


        print("  process ID        = 0x%08X" % pe32.th32ProcessID)
        print("  thread count      = %d" % pe32.cntThreads)
        print("  parent process ID = 0x%08X" % pe32.th32ParentProcessID)
        print("  Priority Base     = %d" % pe32.pcPriClassBase)
        print("  Priority Class    = %d" %  dwPriorityClass)

        ListProcessModules( pe32.th32ProcessID )
        ListProcessThreads( pe32.th32ProcessID )

        ret = Process32Next( hProcessSnap, pointer(pe32) )
