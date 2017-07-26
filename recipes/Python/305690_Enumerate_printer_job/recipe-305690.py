import time
from ctypes import *

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
ws = WinDLL("winspool.drv")

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

class SYSTEMTIME(Structure):
    _fields_ = [
        ("wYear", c_short),
        ("wMonth", c_short),
        ("wDayOfWeek", c_short),
        ("wDay", c_short),
        ("wHour", c_short),
        ("wMinute",c_short),
        ("wSecond", c_short),
        ("wMilliseconds", c_short)
        ]

class DEVMODE(Structure): 
    _fields_ = [ 
        ("dmDeviceName", c_char * 32), 
        ("dmSpecVersion", c_short), 
        ("dmDriverVersion", c_short), 
        ("dmSize", c_short), 
        ("dmDriverExtra", c_short), 
        ("dmFields", c_int), 
        ("dmOrientation", c_short), 
        ("dmPaperSize", c_short), 
        ("dmPaperLength", c_short), 
        ("dmPaperWidth", c_short), 
        ("dmScale", c_short), 
        ("dmCopies", c_short), 
        ("dmDefaultSource", c_short), 
        ("dmPrintQuality", c_short), 
        ("dmColor", c_short), 
        ("dmDuplex", c_short), 
        ("dmYResolution", c_short), 
        ("dmTTOption", c_short), 
        ("dmCollate", c_short), 
        ("dmFormName", c_char * 32), 
        ("dmLogPixels", c_int), 
        ("dmBitsPerPel", c_long), 
        ("dmPelsWidth", c_long), 
        ("dmPelsHeight", c_long), 
        ("dmDisplayFlags", c_long), 
        ("dmDisplayFrequency", c_long) 
    ]
class JOB_INFO_2(Structure):
    _fields_ = [
        ("JobId", c_ulong),
        ("pPrinterName", c_char_p),
        ("pMachineName", c_char_p),
        ("pUserName", c_char_p),
        ("pDocument", c_char_p),
        ("pNotifyName", c_char_p),
        ("pDatatype", c_char_p),
        ("pPrintProcessor", c_char_p),
        ("pParameters", c_char_p),
        ("pDriverName", c_char_p),
        ("pDevMode", POINTER(DEVMODE)),
        ("pStatus", c_char_p),
        ("pSecurityDescriptor", c_void_p),
        ("Status", c_ulong),
        ("Priority", c_ulong),
        ("Position",c_ulong),
        ("StartTime", c_ulong),
        ("UntilTime", c_ulong),
        ("TotalPages", c_ulong),
        ("Size", c_ulong),
        ("Submitted", SYSTEMTIME),
        ("Time", c_ulong),
        ("PagesPrinted", c_ulong)      
        ]    


class Printer:

    def ReadPrinterData(self, hPrinter):
        
        #-- Read Data from printer
        pReadBuffer = c_buffer(500) # can make this dynamic depending on the job Size i.e. pJobInfo[i].Size
        pBuf = addressof(pReadBuffer) 
        READ_BUFFER_SIZE = sizeof(pReadBuffer)
        NoRead = c_ulong()
        pNoRead = addressof(NoRead)

        #-- Lets try to get the spool file
        ret = ws.ReadPrinter(hPrinter,
                               pBuf,
                               READ_BUFFER_SIZE,
                               pNoRead)

        if ret:
            print "".join([i for i in pReadBuffer])
        pBuf = None
        pReadBuffer = None
        
    def GetDefaultPrinter(self):
        
        #-- Get the default printer
        plen = c_long() 
        ret = ws.GetDefaultPrinterA(None, byref(plen)) 
        pname = c_buffer(plen.value) 
        ret = ws.GetDefaultPrinterA(pname, byref(plen)) 
        return pname.value
    
    def OpenPrinter(self, prtname = None):
        #-- Let open our printer
        if prtname == None:
            self.prtname = self.GetDefaultPrinter()
        self.handle = c_ulong()
        ret = ws.OpenPrinterA(self.prtname, byref(self.handle), None)
        return self.handle

    def ClosePrinter(self, handle = None):
        #-- Close our printer after opening it
        if handle == None:
            ws.ClosePrinter(self.handle)
            self.handle = None
        else:
            ws.ClosePrinter(handle)
            handle = None
        
    def EnumJobs(self, pJob, cbBuf):
        
        #-- Enumerates printer jobs
        FirstJob = c_ulong(0) #Start from this job
        self.NoJobs = 20 #How many jobs do you want to get?
        Level = 2 #JOB_INFO_2 Structure
        self.pcbNeeded = c_ulong(0) # Bytes needed to fill the structure
        self.nReturned = c_ulong(0) # No. of jobs returned

        ret = ws.EnumJobsA(self.OpenPrinter(),
                       FirstJob,
                       self.NoJobs,
                       Level,
                       pJob,
                       cbBuf,
                       byref(self.pcbNeeded),
                       byref(self.nReturned))
        
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
            pJob = addressof(pJobInfo)

            #-- Call EnumJobs now with the correct memory needed from the first call
            prt.EnumJobs(pJob, prt.pcbNeeded)
            
            #-- Lets check whether we got any job from the second call
            if prt.nReturned.value:
                for i in range (prt.nReturned.value):
                    print  pJobInfo[i].JobId, pJobInfo[i].pDocument, pJobInfo[i].pUserName, pJobInfo[i].Status
                    
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
