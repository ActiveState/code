## export variable on win32 like *nix  
Originally published: 2008-08-19 03:06:49  
Last updated: 2008-08-18 20:10:34  
Author: winterTTr Dong  
  
Export variable PERMANENTLY on win32 , without needing to reboot system.

EXAMPLE:

import win32export

win32export.export("fooname" , "foovalue")

NOTE: 

you need to install "pywin32" if you want to use this .