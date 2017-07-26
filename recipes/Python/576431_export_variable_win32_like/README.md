## export variable on win32 like *nix 
Originally published: 2008-08-19 03:06:49 
Last updated: 2008-08-18 20:10:34 
Author: winterTTr Dong 
 
Export variable PERMANENTLY on win32 , without needing to reboot system.\n\nEXAMPLE:\n\nimport win32export\n\nwin32export.export("fooname" , "foovalue")\n\nNOTE: \n\nyou need to install "pywin32" if you want to use this .