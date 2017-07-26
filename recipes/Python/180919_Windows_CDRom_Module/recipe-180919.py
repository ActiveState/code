'''
Python Module: WinCDROM
Purpose: Loads or unloads a cd-rom drive on Windows. Only
tested on Windows 2000 and XP.
'''

import os, time
try:
    import win32file, win32api
    from win32con import *
except ImportError:
    print "The WinCDROM module requires the Python Win32 extensions."
    raise

class Cdrom:
    '''Controls for loading,ejecting, and reading cds on Win32 platforms.'''

    def __init__(self, drive=None, timeout=20):
        '''Accepts a cd drive letter. For example 'E:' or 'e'.'''
        self.drives = []
        try:
            self.drive = drive[:1].upper()
        except TypeError:
            self.drive = ''
            self.getDrives()
        self.timeout = timeout

    def __getDeviceHandle(self, drive=''):
        '''Returns a properly formatted device handle for DeviceIOControl call.'''
        drive = drive[:1]
        return "\\\\.\\%s:" % drive.upper()

    def __is_cd_inserted(self, drive=''):
        try:
            x = win32api.GetVolumeInformation(drive)
            #print "CD is inserted in drive %s" % drive
            return 1
        except:
            #print "no CD inserted in drive %s" % drive
            return 0

    def getDrives(self):
        '''Assign all available cd drives to self.drives. If CdRom.drive
        is not already set the first drive returned becomes the default.
        '''
        letters = [l.upper() + ':' for l in 'abcdefghijklmnopqrstuvwxyz']
        for drive in letters:
            if win32file.GetDriveType(drive)==5:
                self.drives.append(drive)
        if not self.drive:
            self.drive = self.drives[0]

    def load(self, drive=''):
        '''Closes cd drive door and waits until cd is readable.'''
        drive = drive or self.drive
        device = self.__getDeviceHandle(drive)
        hdevice = win32file.CreateFile(device, GENERIC_READ,
                                        FILE_SHARE_READ, None, OPEN_EXISTING, 0, 0)
        win32file.DeviceIoControl(hdevice,2967564,"", 0, None)
        win32file.CloseHandle(hdevice)
        # Poll drive for loaded and give up after timeout period
        i=0
        while i < 20:
            if self.__is_cd_inserted(drive) == 1:
                return 1
            else:
                time.sleep(1)
            i = i+1
        return 0

    def eject(self, drive=''):
        '''Opens the cd drive door.'''
        drive = drive or self.drive
        device = self.__getDeviceHandle(drive)
        hdevice = win32file.CreateFile(device, GENERIC_READ,
                                        FILE_SHARE_READ, None, OPEN_EXISTING, 0, 0)
        win32file.DeviceIoControl(hdevice,2967560,"", 0, None)
        win32file.CloseHandle(hdevice)

    def close(self, drive=''):
        '''Closes the cd drive door.'''
        drive = drive or self.drive
        device = self.__getDeviceHandle(drive)
        hdevice = win32file.CreateFile(device, GENERIC_READ,
                                        FILE_SHARE_READ, None, OPEN_EXISTING, 0, 0)
        win32file.DeviceIoControl(hdevice,2967564,"", 0, None)
        win32file.CloseHandle(hdevice)
        
if __name__ == '__main__':
    cd = Cdrom(timeout=5)
    print "Running WinCDRom tests"; print
    print "Listing drives:"; print
    print cd.drives; print
    print "Default drive: %s" % cd.drive; print
    print "Opening drive door..."
    cd.eject(); print
    import time; time.sleep(2)
    print "Closing cd drive door... (CD read attempt will time out at %s seconds.)" % cd.timeout
    print
    if cd.load() == 1:
        print "Loaded cd successfully in drive %s" % cd.drive
        print
    else:
        print "Unable to load cd."
        print "If you have a slower drive try increasing the 'timeout' parameter."
        print
    print "WinCDRom Tests completed."
