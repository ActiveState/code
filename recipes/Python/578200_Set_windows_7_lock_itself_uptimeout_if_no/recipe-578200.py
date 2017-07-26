# Author: c8
# Date created: 9/7/12

# Purpose: Set windows to lock itself(upon timeout) with a screensaver 
#          if no internet connection found.

from _winreg import *
import urllib2, socket

debug = False

########################## TO RUN ####################################
# schedule to run every x mins

########################### DEF ######################################
def locker(set):
    # make set in terms of 1/0
    set = 1 if set else 0
    
    subkey = r'Control Panel\Desktop'

    # to ensure screensaver is set to 'none' (straight to lock screen) 
    deleteRegistryKey(HKEY_CURRENT_USER, subkey, r'SCRNSAVE.EXE')

    data= [('ScreenSaverIsSecure', REG_SZ, str(set)),
                  ('ScreenSaveTimeOut', REG_SZ, '420')]
     
    for valueName, valueType, value in data:
        modifyRegistry(HKEY_CURRENT_USER, subkey, valueName, 
                       valueType, value)
    
    if debug: message = 'changed to locked' if set else 'changed to unlocked'
    if debug: print message

    
def modifyRegistry(key, sub_key, valueName, valueType, value):
    """
    A simple function used to change values in
    the Windows Registry.
    """
    try:
        key_handle = OpenKey(key, sub_key, 0, KEY_ALL_ACCESS)
    except WindowsError:
        key_handle = CreateKey(key, sub_key)
 
    SetValueEx(key_handle, valueName, 0, valueType, value)
    CloseKey(key_handle)

def deleteRegistryKey(key, sub_key, name):
    """
    A simple function used to delete values in
    the Windows Registry if present. Silently ignores failure 
    if value doesn't exist.
    """
    try:
        key_handle = OpenKey(key, sub_key, 0, KEY_ALL_ACCESS)
    except WindowsError:
        if debug: print 'No such key'
        return
    
    try:
        DeleteValue(key_handle, name) 
    except WindowsError:
        if debug: print "Value doesn't exist"
        return 
        
    CloseKey(key_handle)
    
def internet_on():
    # list of sites not likely to go down soon: google.com, microsoft.com etc
    sites = ['173.194.79.94', '74.125.113.99', '64.4.11.20',
            '173.194.33.21', '96.16.97.11']
    for i in sites:
        try:
            site = 'http://%s' % (i)
            response=urllib2.urlopen(site,timeout=1)
            return True
        # if urllib error, cant find site etc
        except urllib2.URLError as err: 
            continue
        # if timeout - occurs on some connections occasionally
        except socket.timeout:
            continue
    return False

################################## CODE ######################################    
   
# if connected to internet
if internet_on():
    # set windows to unlocked
    locker(False)
else:
    # set windows to locked
    locker(True)
