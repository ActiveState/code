import os
import win32con
import sys
import time
from ctypes import *

class PowerClass(Structure):
    _fields_ = [('ACLineStatus', c_byte),
            ('BatteryFlag', c_byte),
            ('BatteryLifePercent', c_byte),
            ('Reserved1',c_byte),
            ('BatteryLifeTime',c_ulong),
            ('BatteryFullLifeTime',c_ulong)]


powerclass = PowerClass()

while True:
    result = windll.kernel32.GetSystemPowerStatus( byref(powerclass) )

    try:
        state = int(powerclass.ACLineStatus)
    except:
        state = 0 

    if state == 1:
        print 'Power is on...'
    else:
        print 'Power is off...\a'  #\a = bell sounds beep on computer
    
    print 'Sleeping for 5 seconds...'
    time.sleep(5)
