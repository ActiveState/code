## Searching .dll and .exe files in PATH  
Originally published: 2008-10-03 08:59:57  
Last updated: 2014-10-06 09:22:53  
Author: Michal Niklas  
  
Returns the pathnames of the file (.exe or .dll)
which would be loaded/executed in the current environment.
It uses some dirs from configuration (SystemDir, WindowsDir)
and dirs from PATH.

To obtain version info it uses code from:
http://pywin32.hg.sourceforge.net/hgweb/pywin32/pywin32/file/tip/win32/Demos/getfilever.py

Example of usage:

        c:\tools\pyscripts\scripts>which_dll.py libpq.dll
        2008-06-09 02:58:26	  167936 [b]	c:\postgresql\8.3\bin\libpq.dll	ver:8.3.3.8160
        2008-03-17 01:47:50	  167936 [b]	c:\tools\libpq.dll	ver:8.3.1.8075
        2008-03-17 01:47:50	  167936 [b]	g:\public\libpq.dll	ver:8.3.1.8075
        	trying to load "libpq.dll" ...
        	c:\postgresql\8.3\bin\libpq.dll loaded
    
