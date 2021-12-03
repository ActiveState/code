import time
import ctypes as ct
from ctypes import wintypes as wt


"""
This script enumerates printer jobs from a specified default printer. This information includes Jobid, Document name,
username of person submitting the job and if you are lucky would be able to get the spool file (SPL file format) from
the printer. It could be used as a printer monitor for job accounting.

Usage: python EnumeratePrinterJobs.py

Known Issues: You might find that it might crash from time to time with memory access errors. However, it stabilises
and does the job.

Based on information from http://support.microsoft.com/default.aspx?scid=kb;en-us;160129

By Eric Koome
email ekoome@yahoo.com
license GPL

"""

LPPRINTER_DEFAULTS = wt.LPVOID

ws = ct.WinDLL("winspool.drv")

ws.ClosePrinter.argtypes = (wt.HANDLE,)
ws.ClosePrinter.restype = wt.BOOL

ws.EnumJobsA.argtypes = (wt.HANDLE, wt.DWORD, wt.DWORD, wt.DWORD, wt.LPBYTE, wt.DWORD, wt.LPDWORD, wt.LPDWORD)
ws.EnumJobsA.restype = wt.BOOL

ws.GetDefaultPrinterA.argtypes = (wt.LPSTR, wt.LPDWORD)
ws.GetDefaultPrinterA.restype = wt.BOOL

ws.OpenPrinterA.argtypes = (wt.LPSTR, ct.POINTER(wt.HANDLE), LPPRINTER_DEFAULTS)
ws.OpenPrinterA.restype = wt.BOOL

ws.ReadPrinter.argtypes = (wt.HANDLE, wt.LPVOID, wt.DWORD, wt.LPDWORD)
ws.ReadPrinter.restype = wt.BOOL


#-- Job Status meaning
JOB_STATUS_PAUSED                  = 0x00000001
JOB_STATUS_ERROR                   = 0x00000002
JOB_STATUS_DELETING                = 0x00000004
JOB_STATUS_SPOOLING                = 0x00000008
JOB_STATUS_PRINTING                = 0x00000010
JOB_STATUS_OFFLINE                 = 0x00000020
JOB_STATUS_PAPEROUT                = 0x00000040
JOB_STATUS_PRINTED                 = 0x00000080
JOB_STATUS_DELETED                 = 0x00000100
JOB_STATUS_BLOCKED_DEVQ            = 0x00000200
JOB_STATUS_USER_INTERVENTION       = 0x00000400
JOB_STATUS_RESTART                 = 0x00000800


class SYSTEMTIME(ct.Structure):
    _fields_ = [
        ("wYear", ct.c_short),
        ("wMonth", ct.c_short),
        ("wDayOfWeek", ct.c_short),
        ("wDay", ct.c_short),
        ("wHour", ct.c_short),
        ("wMinute", ct.c_short),
        ("wSecond", ct.c_short),
        ("wMilliseconds", ct.c_short),
    ]


class DEVMODE(ct.Structure):
    _fields_ = [
        ("dmDeviceName", ct.c_char * 32),
        ("dmSpecVersion", ct.c_short),
        ("dmDriverVersion", ct.c_short),
        ("dmSize", ct.c_short),
        ("dmDriverExtra", ct.c_short),
        ("dmFields", ct.c_int),
        ("dmOrientation", ct.c_short),
        ("dmPaperSize", ct.c_short),
        ("dmPaperLength", ct.c_short),
        ("dmPaperWidth", ct.c_short),
        ("dmScale", ct.c_short),
        ("dmCopies", ct.c_short),
        ("dmDefaultSource", ct.c_short),
        ("dmPrintQuality", ct.c_short),
        ("dmColor", ct.c_short),
        ("dmDuplex", ct.c_short),
        ("dmYResolution", ct.c_short),
        ("dmTTOption", ct.c_short),
        ("dmCollate", ct.c_short),
        ("dmFormName", ct.c_char * 32),
        ("dmLogPixels", ct.c_int),
        ("dmBitsPerPel", ct.c_long),
        ("dmPelsWidth", ct.c_long),
        ("dmPelsHeight", ct.c_long),
        ("dmDisplayFlags", ct.c_long),
        ("dmDisplayFrequency", ct.c_long),
    ]


class JOB_INFO_2(ct.Structure):
    _fields_ = [
        ("JobId", ct.c_ulong),
        ("pPrinterName", ct.c_char_p),
        ("pMachineName", ct.c_char_p),
        ("pUserName", ct.c_char_p),
        ("pDocument", ct.c_char_p),
        ("pNotifyName", ct.c_char_p),
        ("pDatatype", ct.c_char_p),
        ("pPrintProcessor", ct.c_char_p),
        ("pParameters", ct.c_char_p),
        ("pDriverName", ct.c_char_p),
        ("pDevMode", ct.POINTER(DEVMODE)),
        ("pStatus", ct.c_char_p),
        ("pSecurityDescriptor", ct.c_void_p),
        ("Status", ct.c_ulong),
        ("Priority", ct.c_ulong),
        ("Position", ct.c_ulong),
        ("StartTime", ct.c_ulong),
        ("UntilTime", ct.c_ulong),
        ("TotalPages", ct.c_ulong),
        ("Size", ct.c_ulong),
        ("Submitted", SYSTEMTIME),
        ("Time", ct.c_ulong),
        ("PagesPrinted", ct.c_ulong),
    ]


class Printer:

    def ReadPrinterData(self, hPrinter):
        #-- Read Data from printer
        pReadBuffer = ct.c_buffer(500) # can make this dynamic depending on the job Size i.e. pJobInfo[i].Size
        pBuf = ct.addressof(pReadBuffer)
        READ_BUFFER_SIZE = ct.sizeof(pReadBuffer)
        NoRead = ct.c_ulong()
        pNoRead = ct.addressof(NoRead)

        #-- Lets try to get the spool file
        ret = ws.ReadPrinter(hPrinter,
                             pBuf,
                             READ_BUFFER_SIZE,
                             pNoRead)

        if ret:
            print("".join([i for i in pReadBuffer]))
        pBuf = None
        pReadBuffer = None

    def GetDefaultPrinter(self):
        #-- Get the default printer
        plen = wt.DWORD()
        ret = ws.GetDefaultPrinterA(None, ct.byref(plen))
        pname = ct.c_buffer(plen.value)
        ret = ws.GetDefaultPrinterA(pname, ct.byref(plen))
        return pname.value

    def OpenPrinter(self, prtname=None):
        #-- Let open our printer
        if prtname is None:
            self.prtname = self.GetDefaultPrinter()
        self.handle = wt.HANDLE()
        ret = ws.OpenPrinterA(self.prtname, ct.byref(self.handle), None)
        return self.handle

    def ClosePrinter(self, handle=None):
        #-- Close our printer after opening it
        if handle is None:
            ws.ClosePrinter(self.handle)
            self.handle = None
        else:
            ws.ClosePrinter(handle)
            handle = None

    def EnumJobs(self, pJob, cbBuf):
        #-- Enumerates printer jobs
        FirstJob = ct.c_ulong(0) #Start from this job
        self.NoJobs = 20 #How many jobs do you want to get?
        Level = 2 #JOB_INFO_2 Structure
        self.pcbNeeded = ct.c_ulong(0) # Bytes needed to fill the structure
        self.nReturned = ct.c_ulong(0) # No. of jobs returned

        ret = ws.EnumJobsA(self.OpenPrinter(),
                           FirstJob,
                           self.NoJobs,
                           Level,
                           pJob,
                           cbBuf,
                           ct.byref(self.pcbNeeded),
                           ct.byref(self.nReturned))

        return ret


if __name__== "__main__":
    while 1:
        #-- Loop picking up printer jobs
        prt = Printer()

        # we need to call EnumJobs() to find out how much memory you need
        # It should have failed if there are jobs on the printer
        if not prt.EnumJobs(None,0):

            #-- Lets first close the printer
            prt.ClosePrinter()

            #-- Allocate JOB_INFO_2 structures
            pJobArray = JOB_INFO_2 * prt.NoJobs
            pJobInfo = pJobArray()
            pJob = ct.addressof(pJobInfo)

            #-- Call EnumJobs now with the correct memory needed from the first call
            prt.EnumJobs(pJob, prt.pcbNeeded)

            #-- Lets check whether we got any job from the second call
            if prt.nReturned.value:
                for i in range (prt.nReturned.value):
                    print(pJobInfo[i].JobId, pJobInfo[i].pDocument, pJobInfo[i].pUserName, pJobInfo[i].Status)

                    prtName =  prt.GetDefaultPrinter()

                    #-- Lets try and get the spool file. The call to open printer must have the jobid:
                    #-- Format "printername,Job xxxx"
                    prtJobName = prtName+","+"Job"+" "+str(pJobInfo[i].JobId)
                    pHandle = prt.OpenPrinter(prtJobName)

                    if pHandle.value:
                        #-- Read spool file. Does not work well if you do not have a bidirectional printer.
                        prt.ReadPrinterData(pHandle)
                        prt.ClosePrinter(pHandle)
            prt.ClosePrinter()

            #-- Clean up
            pJob = None
            pJobInfo = None
        prt = None

        #-- Wait for the next printer job
        #-- Adjust this depending on the speed of your printer and network
        time.sleep(3)
