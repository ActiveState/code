###Get memory usage of Windows processes using GetProcessMemoryInfo (via ctypes)

Originally published: 2013-04-25 01:26:19
Last updated: 2013-04-25 01:26:19
Author: Ben Hoyt

These functions call the Win32 function GetProcessMemoryInfo() using ctypes to get the memory usage of the current process. Works on both 32-bit and 64-bit Windows and Python 2.6+ (including Python 3.x).