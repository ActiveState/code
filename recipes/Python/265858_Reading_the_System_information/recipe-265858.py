import win32api
import win32con
import win32file
from StringIO import StringIO

class GetSysInformation:
    def __init__(self):
        # variable to write a flat file
        self.fileHandle = None
        self.HKEY_CLASSES_ROOT = win32con.HKEY_CLASSES_ROOT 
        self.HKEY_CURRENT_USER = win32con.HKEY_CURRENT_USER 
        self.HKEY_LOCAL_MACHINE = win32con.HKEY_LOCAL_MACHINE
        self.HKEY_USERS = win32con.HKEY_USERS
        self.FILE_PATH = "//masblrfs06/karcherarea$/workarea/nishitg/"+ win32api.GetComputerName()
        self.CONST_OS_SUBKEY = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
        self.CONST_PROC_SUBKEY = "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0"
        self.CONST_SW_SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"        
    def getSysInfo(self):
        try:
            hCounter=0
            hProcessorName=""
            # connecting to the base
            hHandle = win32api.RegConnectRegistry(None,self.HKEY_LOCAL_MACHINE)
            # opening the sub key to get the processor name
            print "debug1"
            hHandle = win32api.RegOpenKeyEx(self.HKEY_LOCAL_MACHINE,self.CONST_PROC_SUBKEY,0,win32con.KEY_ALL_ACCESS)
            hNoOfKeys = win32api.RegQueryInfoKey(hHandle)[1]
            while hCounter < hNoOfKeys:           
                hData = win32api.RegEnumValue(hHandle,hCounter)
                if hData[0]== "Identifier":
                    hProcessorName = hData[1]
                hCounter = hCounter + 1
            if hProcessorName=="":
                    hProcessorName = "Processor Name Cannot be determined"
                    self.preparefile("Processor Name",hProcessorName)
            hCompName = win32api.GetComputerName()
            self.preparefile("Computer Name",hCompName)
            hDomainName = win32api.GetDomainName()
            self.preparefile("Domain Name",hDomainName)
            hUserName = win32api.GetUserName()
            self.preparefile("User Name",hUserName)
            # getting OS Details
            hCounter=0
            # opening the sub key to get the processor name
            hHandle = win32api.RegOpenKeyEx(self.HKEY_LOCAL_MACHINE,self.CONST_OS_SUBKEY,0,win32con.KEY_ALL_ACCESS)
            hNoOfKeys = win32api.RegQueryInfoKey(hHandle)[1]
            hOSVersion=""
            hOSName=""        
            while hCounter < hNoOfKeys:           
                hData = win32api.RegEnumValue(hHandle,hCounter)
                if hData[0]== "ProductName":
                    hOSName = hData[1]
                    self.preparefile("OS Name",hOSName)
                    break
                hCounter = hCounter + 1
            if hOSName=="":
                    self.preparefile("OS Name","OS Name could not be read from the registry")
            hCounter = 0 
            while hCounter < hNoOfKeys:
                hData = win32api.RegEnumValue(hHandle,hCounter)            
                if hData[0]== "CSDVersion":
                    hOSVersion = hData[1]
                    self.preparefile("OS Version",hOSVersion)
                    break
                hCounter = hCounter + 1
            if hOSVersion=="":
                self.preparefile("OS Version","OS Version could not be read from the registry")
            # inserting master data
            #insertMachineMaster(hCompName,hDomainName,hOSName,hOSVersion,hProcessorName)
        except:
            self.preparefile("Exception","in Exception in getSysDetails")
    def getSoftwareList(self):
        try:
            hCounter=0
            hAttCounter=0
            # connecting to the base
            hHandle = win32api.RegConnectRegistry(None,win32con.HKEY_LOCAL_MACHINE)
            # getting the machine name and domain name
            hCompName = win32api.GetComputerName()
            hDomainName = win32api.GetDomainName()
            # opening the sub key to get the list of Softwares installed
            hHandle = win32api.RegOpenKeyEx(self.HKEY_LOCAL_MACHINE,self.CONST_SW_SUBKEY,0,win32con.KEY_ALL_ACCESS)
            # get the total no. of sub keys
            hNoOfSubNodes = win32api.RegQueryInfoKey(hHandle)
            # delete the entire data and insert it again
            #deleteMachineSW(hCompName,hDomainName)
            # browsing each sub Key which can be Applications installed
            while hCounter < hNoOfSubNodes[0]:
                hAppName = win32api.RegEnumKey(hHandle,hCounter)
                hPath = self.CONST_SW_SUBKEY + "\\" + hAppName
                # initialising hAttCounter
                hAttCounter = 0
                hOpenApp = win32api.RegOpenKeyEx(self.HKEY_LOCAL_MACHINE,hPath,0,win32con.KEY_ALL_ACCESS)
                # [1] will give the no. of attributes in this sub key
                hKeyCount = win32api.RegQueryInfoKey(hOpenApp)
                hMaxKeyCount = hKeyCount[1]
                hSWName = ""
                hSWVersion = ""
                while hAttCounter < hMaxKeyCount:
                    hData = win32api.RegEnumValue(hOpenApp,hAttCounter)                    
                    if hData[0]== "DisplayName":
                        hSWName = hData[1]
                        self.preparefile("SW Name",hSWName)
                    elif hData[0]== "DisplayVersion":
                        hSWVersion = hData[1]
                        self.preparefile("SW Version",hSWVersion)
                    hAttCounter = hAttCounter + 1
                #if (hSWName !=""):
                #insertMachineSW(hCompName,hDomainName,hSWName,hSWVersion)
                hCounter = hCounter + 1           
        except:
            self.preparefile("Exception","In exception in getSoftwareList")           
    def openFile(self):
        try:
            self.fileHandle = open(self.FILE_PATH,'w')
        except:
            print "Exceptions in openFile"
    def preparefile(self,printCaption,printString):
        try:
            printText = printCaption + " : " + printString
            print printText
            self.fileHandle.write(printText + "\n")        
        except:
            print "In Exception of Prepare file"
    def closeFile(self):
        try:
            self.fileHandle.close()
        except:
            print "Exceptions in closeFile"
