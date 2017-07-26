import sys
import threading
import ctypes
from ctypes import byref
from ctypes import Structure, Union
from ctypes.wintypes import * 

# other wintype definition
LPVOID = ctypes.c_void_p
LPCVOID = LPVOID
DWORD_PTR = DWORD
LONGLONG = ctypes.c_longlong
HCOUNTER = HQUERY = HANDLE

# error code
Error_Success = 0

# macro
sleep = ctypes.windll.kernel32.Sleep
pdh = ctypes.windll.pdh

# structure definition
class Sysinfo_Struct(Structure):
    _fields_ = [('wProcessorArchitecture', WORD),
                ('wReserved', WORD)]

class Sysinfo_Union(Union):
    _fields_ = [('dwOemId', DWORD),
                ('struct', Sysinfo_Struct)]

class System_Info(Structure):
    _fields_ = [('union', Sysinfo_Union),
                ('dwPageSize', DWORD),
                ('lpMinimumApplicationAddress', LPVOID),
                ('lpMaximumApplicationAddress', LPVOID),
                ('dwActiveProcessorMask', DWORD_PTR),
                ('dwNumberOfProcessors', DWORD),
                ('dwProcessorType', DWORD),
                ('dwAllocationGranularity', DWORD),
                ('wProcessorLevel', WORD),
                ('wProcessorRevision', WORD)]

class PDH_Counter_Union(Union):
    _fields_ = [('longValue', LONG),
                ('doubleValue', ctypes.c_double),
                ('largeValue', LONGLONG),
                ('AnsiStringValue', LPCSTR),
                ('WideStringValue', LPCWSTR)]

class PDH_FMT_COUNTERVALUE(Structure):
    _fields_ = [('CStatus', DWORD),
                ('union', PDH_Counter_Union),]


# Exception definition
class TargetRateExceedError(Exception):
    pass


def getProcessorNumber():
    si = System_Info()
    ctypes.windll.kernel32.GetSystemInfo(byref(si))
    return si.dwNumberOfProcessors

g_cpu_usage = 0
class QueryCPUUsageThread(threading.Thread):
    def __init__(self):
        super(QueryCPUUsageThread, self).__init__()
        self.hQuery = HQUERY()
        self.hCounter = HCOUNTER()
        if not pdh.PdhOpenQueryW(None, 0, byref(self.hQuery)) == Error_Success:
            raise RuntimeError('[QueryCPUUsageThread] Open query failed')
        if not pdh.PdhAddCounterW(self.hQuery,
                                 u'''\\Processor(_Total)\\% Processor Time''',
                                 0,
                                 byref(self.hCounter)) == Error_Success:
            raise RuntimeError('[QueryCPUUsageThread] Add counter failed')
        
    def run(self):
        while True: 
            usage = self.getCPUUsage()
            global g_cpu_usage
            g_cpu_usage = usage
        
    def getCPUUsage(self):
        if not pdh.PdhCollectQueryData(self.hQuery) == Error_Success:
            raise RuntimeError('[QueryCPUUsageThread] CollectQueryData failed')
        ctypes.windll.kernel32.Sleep(1000)
        if not pdh.PdhCollectQueryData(self.hQuery) == Error_Success:
            raise RuntimeError('[QueryCPUUsageThread] CollectQueryData failed')

        dwType = DWORD(0)
        value = PDH_FMT_COUNTERVALUE()
        if not pdh.PdhGetFormattedCounterValue(self.hCounter,
                                          0x00000100, # PDH_FMT_LONG
                                          byref(dwType),
                                          byref(value)) == Error_Success:
            raise RuntimeError('[QueryCPUUsageThread] Get CounterValue failed')

        return value.union.longValue
                             
def main(targetRateForMainProcess, targetRate):
    timeInterval = 50.0
    busyTime = float(targetRateForMainProcess) * timeInterval / 100.0
    idleTime = timeInterval - busyTime
    TOLERANCE = 2
    while True:
        if len(sys.argv)<=1:
            usage = g_cpu_usage
            if abs(usage - targetRate) < TOLERANCE:
                pass
            elif usage > targetRate:
                busyTime = max(busyTime - 0.1, 1)
                idleTime = timeInterval - busyTime
            else:
                busyTime = min(busyTime + 0.1, 49)
                idleTime = timeInterval - busyTime
            #print busyTime, idleTime
        startTime = ctypes.windll.kernel32.GetTickCount()
        while ctypes.windll.kernel32.GetTickCount() - startTime < int(round(busyTime)):
            pass
        sleep(int(round(idleTime)))

def subpMain():
    while True:
        pass

def inputLoop():
    while True:
        print 'please input target cpu usage: ',
        try:
            rate = float(raw_input().strip())
            if rate >= 100 or rate <=1:
                raise TargetRateExceedError
        except TargetRateExceedError:
            print 'please input a number in range 1-99'
        except Exception:
            print 'please input a target cpu usage rate, e.g. 70'
        else:
            return rate    

if __name__=='__main__':
    if len(sys.argv) <= 1:  # main process
        targetRate = inputLoop()
        nProcessor = getProcessorNumber()
        fullPercentPerProcessor = 100.0 / float(nProcessor)
        targetRateForMainProcess = targetRate
        
        while targetRateForMainProcess > fullPercentPerProcessor:
            from subprocess import Popen            
            obj=Popen([sys.executable, __file__, 'child'])
            targetRateForMainProcess -= fullPercentPerProcessor
            
        queryCpuThread = QueryCPUUsageThread()
        queryCpuThread.start()
        main(targetRateForMainProcess, targetRate)
    else: # subprocess
        subpMain()
