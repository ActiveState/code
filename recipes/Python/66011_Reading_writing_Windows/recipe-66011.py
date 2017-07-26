from _winreg import *

print r"*** Reading from SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***"
aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run") 
for i in range(1024):                                           
    try:
        n,v,t = EnumValue(aKey,i)
        print i, n, v, t
    except EnvironmentError:                                               
        print "You have",i," tasks starting at logon..."
        break          
CloseKey(aKey)                                                  

print r"*** Writing to SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***"
aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
try:   
   SetValueEx(aKey,"MyNewKey",0, REG_SZ, r"c:\winnt\explorer.exe") 
except EnvironmentError:                                          
    print "Encountered problems writing into the Registry..."
CloseKey(aKey)

CloseKey(aReg)            
