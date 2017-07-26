"""
    The MIT License
    
    Copyright 2009 Shao-Chuan Wang <shaochuan.wang@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

"""
__author__ = "Shao-Chuan Wang"
__email__ = "shaochuan.wang@gmail.com"
__version__ = "1.0"
__URL__ = "http://shao-chuan.appspot.com"


import ctypes
from ctypes import Structure
from ctypes import byref
import ctypes.wintypes as wintypes

SE_PRIVILEGE_ENABLED = 2
SE_SHUTDOWN_NAME = 'SeShutdownPrivilege'
TOKEN_ALL_ACCESS = 0xf00ff
TOKEN_ADJUST_PRIVILEGES = 0x20
host = None  #: it means local machine.

class LUID(Structure):
  _fields_ = [("LowPart", wintypes.DWORD),
              ("HighPart", wintypes.LONG)]

class LUID_AND_ATTRIBUTES(Structure):
  _fields_ = [("Luid", LUID),
              ("Attributes", wintypes.DWORD)]  

class TOKEN_PRIVILEGES(Structure):
  _fields_ = [("PrivilegeCount", wintypes.DWORD),
              ("Privileges", LUID_AND_ATTRIBUTES)]  


def shutdown(msg, timeout, force=False, reboot=True):
  advapi32 = ctypes.windll.advapi32
  kernel32 = ctypes.windll.kernel32

  luid = LUID()
  if not advapi32.LookupPrivilegeValueA(None, SE_SHUTDOWN_NAME, byref(luid)):
    print 'LookupPrivilegeValueA failed.'

  attr = LUID_AND_ATTRIBUTES(luid, SE_PRIVILEGE_ENABLED)
  privilegeCount = 1
  tokenPrivileges = TOKEN_PRIVILEGES(privilegeCount, attr)

  p = kernel32.GetCurrentProcess()
  hToken = wintypes.HANDLE()
  if not advapi32.OpenProcessToken(p, TOKEN_ADJUST_PRIVILEGES, byref(hToken)):
    print 'OpenProcessToken failed.'
    return False
  if not advapi32.AdjustTokenPrivileges(hToken, False, byref(tokenPrivileges), None, None, None):
    print 'AdjustTokenPrivileges failed.'
    return False
  if not advapi32.InitiateSystemShutdownA(host, msg, timeout, force, reboot):
    print 'InitiateSystemShutdownA failed.'
    return False
  return True

if __name__ == '__main__':
  # to cancel the shutdown, just type 'shudown -a' in your terminal.    
  shutdown('This computer is about to shutdown...', 20)
