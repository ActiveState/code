"""
Locks the users workstation, for Windows NT and 2000

Design philosophy for this was simple, create a utility to lock
a users' workstation, without messing up their screensaver settings.
"""

import win32con
import win32api

#########################################
#Set up the two methods we'll use in this program:
#########################################

#We need a method to check what they have setup for their screensaver, so
#that we can return things to what they should be once the workstation is
#locked:
def queryHKCUValues(valuePath, valueName):
	settingsDict = {}
	#First, we need to open a handle to the relevant HIVE in the registry...
	keyHandle = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, valuePath, 0, win32con.KEY_READ)
	for value in valueName:
		(valueData, valueType) = win32api.RegQueryValueEx(keyHandle, value)
		settingsDict[value] = [valueData, valueType]
	keyHandle.Close()
	#This dictionary now holds all the info that we'll need to put things back where
	#they belong once we're done...
	return settingsDict

#This method we will use to 'tidy up' after ourselves...
def returnHKCUValues(valuePath, valueDict):
	#First, we need to open a handle to the relevant HIVE in the registry...
	keyHandle = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, valuePath, 0, win32con.KEY_WRITE)
	valueDictKeys = valueDict.keys()
	#'Unpack' the dictionary values back into the registry where they belong:
	for value in valueDictKeys:
		win32api.RegSetValueEx(keyHandle, value, 0, valueDict[value][1], valueDict[value][0])
	keyHandle.Close()


#########################################
#On to the real work now!
#########################################

#Before we begin, lets record the state of the values that we'll be working with:
tempDict = queryHKCUValues('Control Panel\Desktop', ['ScreenSaveActive', 'ScreenSaverIsSecure', 'SCRNSAVE.EXE'])

#Now we can assign our own values to these without fear of messing them up:
keyHandle = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, 'Control Panel\Desktop', 0, win32con.KEY_WRITE)
#Now that we have the handle, we can use it to setup the relevant settings in the registry.
#These ensure that every time this program is run, the screensaver is in a predictable state.
win32api.RegSetValueEx(keyHandle, 'ScreenSaveActive', 0, win32con.REG_SZ, '1')
win32api.RegSetValueEx(keyHandle, 'ScreenSaverIsSecure', 0, win32con.REG_SZ, '1')
win32api.RegSetValueEx(keyHandle, 'SCRNSAVE.EXE', 0, win32con.REG_SZ, 'logon.scr')
#Now that we've satisfied all assumptions, we can close the handle:
keyHandle.Close()

#Now that we now that a secure screensaver is guaranteed, we send the
#'Launch Screensaver' message, as recommended in Microsoft KB article
#Q262646.  Don't ask why we have to call it twice to get it to work...
win32api.SendMessage(win32con.HWND_TOPMOST, win32con.WM_SYSCOMMAND, win32con.SC_SCREENSAVE, 0)
win32api.SendMessage(win32con.HWND_TOPMOST, win32con.WM_SYSCOMMAND, win32con.SC_SCREENSAVE, 0)

#Now that the workstation is locked, we will return everything to the way
#it was beforehand:
returnHKCUValues('Control Panel\Desktop', tempDict)

#Finally, we will force the value of the screen saver grace period to zero
#so that locking happens instantaneously upon the launching of the
#screensaver.  This setting requires a reboot to take effect, so we will
#simply force it here everytime to make sure that it is always set for
#when the user reboots:
keyHandle = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, 'Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 0, win32con.KEY_WRITE)
win32api.RegSetValueEx(keyHandle, 'ScreenSaverGracePeriod', 0, win32con.REG_SZ, '0')
keyHandle.Close()

#Have fun!
#God bless Python and the Win32 extensions library ;-)
#esrever_otua
