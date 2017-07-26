## Disable File System Redirector  
Originally published: 2012-02-06 12:42:34  
Last updated: 2012-02-06 16:34:02  
Author: zxw   
  
This disables the [Windows File System Redirector](http://msdn.microsoft.com/en-us/library/aa384187(v=vs.85\\).aspx).\n\nWhen a 32 bit program runs on a 64 bit operating system the paths to C:/Windows/System32 automatically get redirected to the 32 bit version (C:/Windows/SysWow64), if you really do need to access the contents of System32, you need to disable the file system redirector first.