import sys, socket
from struct import pack, unpack
from time import time, ctime, mktime
__all__=('sntp_time',)
_TIME1970 = 2208988800L      # Thanks to F.Lundh
_data = '\x1b' + 47*'\0'


#typedef struct _SYSTEMTIME {  // st 
#    WORD wYear; 
#    WORD wMonth; 
#    WORD wDayOfWeek; 
#    WORD wDay; 
#    WORD wHour; 
#    WORD wMinute; 
#    WORD wSecond; 
#    WORD wMilliseconds; 
#} SYSTEMTIME; 
#VOID GetSystemTime(
#  LPSYSTEMTIME lpSystemTime   // address of system time structure
#);
#SYSTEMTIME st;
#GetSystemTime(&st);
#SetSystemTime(&st);

from ctypes import windll, Structure, c_ushort, byref, c_ulong, c_long
kernel32_GetSystemTime = windll.kernel32.GetSystemTime
kernel32_SetSystemTime = windll.kernel32.SetSystemTime
kernel32_SystemTimeToFileTime=windll.kernel32.SystemTimeToFileTime
kernel32_FileTimeToSystemTime=windll.kernel32.FileTimeToSystemTime
class SYSTEMTIME(Structure):
    _fields_ =  (
                ('wYear', c_ushort), 
                ('wMonth', c_ushort), 
                ('wDayOfWeek', c_ushort), 
                ('wDay', c_ushort), 
                ('wHour', c_ushort), 
                ('wMinute', c_ushort), 
                ('wSecond', c_ushort), 
                ('wMilliseconds', c_ushort), 
                )
    def __str__(self):
        return '%4d%02d%02d%02d%02d%02d.%03d' % (self.wYear,self.wMonth,self.wDay,self.wHour,self.wMinute,self.wSecond,self.wMilliseconds)
class LONG_INTEGER(Structure):
    _fields_ =  (
            ('low', c_ulong), 
            ('high', c_long),
            )

def GetSystemTime():
    st = SYSTEMTIME(0,0,0,0,0,0,0,0)
    kernel32_GetSystemTime(byref(st))
    return st

def SetSystemTime(st):
    return kernel32_SetSystemTime(byref(st))

def GetSystemFileTime():
    ft = LONG_INTEGER(0,0)
    st = GetSystemTime()
    if kernel32_SystemTimeToFileTime(byref(st),byref(ft)):
        return (long(ft.high)<<32)|ft.low
    return None

def SetSystemFileTime(ft):
    st = SYSTEMTIME(0,0,0,0,0,0,0,0)
    ft = LONG_INTEGER(ft&0xFFFFFFFFL,ft>>32)
    r = kernel32_FileTimeToSystemTime(byref(ft),byref(st))
    if r: SetSystemTime(st)
    return r

def _L2U32(L):
    return unpack('l',pack('L',L))[0]

_UTIME1970 = _L2U32(_TIME1970)
def _time2ntp(t):
    s = int(t)
    return pack('!II',s+_UTIME1970,_L2U32((t-s)*0x100000000L))

def _ntp2time((s,f)):
    return s-_TIME1970+float((f>>4)&0xfffffff)/0x10000000

def sntp_time(server):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        #originate timestamp 6:8
        #receive timestamp   8:10
        #transmit timestamp 10:12
        t1 = time()
        s.sendto(_data, (server,123))
        data, address = s.recvfrom(1024)
        data = unpack('!12I', data)
        t4 = time()
        t2 = _ntp2time(data[8:10])
        t3 = _ntp2time(data[10:12])
        delay = (t4 - t1) - (t2 - t3)
        offset = ((t2 - t1) + (t3 - t4)) / 2.
        return address[0], delay, offset
    except:
        return 3*(None,)

if __name__=='__main__':
    go = '--go' in sys.argv
    if go: sys.argv.remove('--go')
    servers = sys.argv[1:] or '''a.ntp.alphazed.net bear.zoo.bt.co.uk ntp.cis.strath.ac.uk ntp.exnet.com ntp2a.mcc.ac.uk
                ntp2b.mcc.ac.uk ntp2c.mcc.ac.uk time-server.ndo.com'''.split()
    t0 = time()
    mu = 0
    ss = 0
    n = 0
    data = []
    a = data.append
    for server in servers:
        address, delay, offset = sntp_time(server)
        if address:
            #recursions for mean and sigma squared
            n1 = n
            n += 1
            mu = (offset+mu*n1)/n
            d = offset - mu
            if n1: ss = ((n1-1)*ss+d*d*(n/n1))/n1
            a((server, address, delay, offset))

    ss = ss**0.5
    print "Offset = %.3f(%.3f)" % (mu,ss)
    for (server, address, delay, offset) in data:
        print '%s(%s): delay=%.3f offset=%.3f' % (server, address,delay,offset)

    if n>3:
        if go:
            if abs(mu)<5:
                r = SetSystemFileTime(GetSystemFileTime()+long(mu*10000000L))   #100 nanosecond units (since 16010101)
                print 'Adjustment',r and 'Carried out!' or 'Failed!'
        else:
            st = GetSystemTime()
            print 'Current System Time', str(st)
            ft = GetSystemFileTime()
            adj = long(mu*10000000L)    #100 nanosecond units (since 16010101)
            print 'Current System FileTime', ft, 'adjustment', adj
            ft += adj
            print  'Adjusted System FileTime', ft
            ft = LONG_INTEGER(ft&0xFFFFFFFFL,ft>>32)
            r = kernel32_FileTimeToSystemTime(byref(ft),byref(st))
            print 'Adjusted System Time', str(st), 'r=',r
