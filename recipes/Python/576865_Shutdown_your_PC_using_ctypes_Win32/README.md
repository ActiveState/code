## Shutdown your PC by using ctypes (Win32 Platform) 
Originally published: 2009-08-03 10:05:38 
Last updated: 2009-08-03 10:05:38 
Author: Shao-chuan Wang 
 
It is true that by using win32 extension python modules, such as win32api, win32con, and win32security, we can easily shutdown the computer with a few steps. However, sometimes your python's runtime environment does not provide win32com module (because it is not a build-in module), we may have to shutdown the pc on our own.\n\nBy using ctypes, we are still able to shutdown or reboot the PC easily.\n