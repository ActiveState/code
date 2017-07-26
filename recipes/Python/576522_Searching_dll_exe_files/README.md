## Searching .dll and .exe files in PATH 
Originally published: 2008-10-03 08:59:57 
Last updated: 2014-10-06 09:22:53 
Author: Michal Niklas 
 
Returns the pathnames of the file (.exe or .dll)\nwhich would be loaded/executed in the current environment.\nIt uses some dirs from configuration (SystemDir, WindowsDir)\nand dirs from PATH.\n\nTo obtain version info it uses code from:\nhttp://pywin32.hg.sourceforge.net/hgweb/pywin32/pywin32/file/tip/win32/Demos/getfilever.py\n\nExample of usage:\n\n        c:\\tools\\pyscripts\\scripts>which_dll.py libpq.dll\n        2008-06-09 02:58:26\t  167936 [b]\tc:\\postgresql\\8.3\\bin\\libpq.dll\tver:8.3.3.8160\n        2008-03-17 01:47:50\t  167936 [b]\tc:\\tools\\libpq.dll\tver:8.3.1.8075\n        2008-03-17 01:47:50\t  167936 [b]\tg:\\public\\libpq.dll\tver:8.3.1.8075\n        \ttrying to load "libpq.dll" ...\n        \tc:\\postgresql\\8.3\\bin\\libpq.dll loaded\n    \n