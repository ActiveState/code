import ctypes
from ctypes import byref
from ctypes import Structure, Union
from ctypes.wintypes import *
import threading

__author__ = 'Shao-chuan Wang'

LONGLONG = ctypes.c_longlong
HQUERY = HCOUNTER = HANDLE
pdh = ctypes.windll.pdh
Error_Success = 0x00000000

class PDH_Counter_Union(Union):
    _fields_ = [('longValue', LONG),
                ('doubleValue', ctypes.c_double),
                ('largeValue', LONGLONG),
                ('AnsiStringValue', LPCSTR),
                ('WideStringValue', LPCWSTR)]

class PDH_FMT_COUNTERVALUE(Structure):
    _fields_ = [('CStatus', DWORD),
                ('union', PDH_Counter_Union),]

g_cpu_usage = 0
class QueryCPUUsageThread(threading.Thread):
    def __init__(self):
        super(QueryCPUUsageThread, self).__init__()
        self.hQuery = HQUERY()
        self.hCounter = HCOUNTER()
        if not pdh.PdhOpenQueryW(None, 
                                 0, 
                                 byref(self.hQuery)) == Error_Success:
            raise Exception
        if not pdh.PdhAddCounterW(self.hQuery,
                                 u'''\\Processor(_Total)\\% Processor Time''',
                                 0,
                                 byref(self.hCounter)) == Error_Success:
            raise Exception
        
    def run(self):
        while True:
            global g_cpu_usage
            g_cpu_usage = self.getCPUUsage()
            print 'cpu_usage: %d' % g_cpu_usage
        
    def getCPUUsage(self):
        PDH_FMT_LONG = 0x00000100
        if not pdh.PdhCollectQueryData(self.hQuery) == Error_Success:
            raise Exception
        ctypes.windll.kernel32.Sleep(1000)
        if not pdh.PdhCollectQueryData(self.hQuery) == Error_Success:
            raise Exception

        dwType = DWORD(0)
        value = PDH_FMT_COUNTERVALUE()
        if not pdh.PdhGetFormattedCounterValue(self.hCounter,
                                          PDH_FMT_LONG,
                                          byref(dwType),
                                          byref(value)) == Error_Success:
            raise Exception

        return value.union.longValue

if __name__=='__main__':
    thread = QueryCPUUsageThread()
    thread.start()
