## Control CPU Usage by using ctypes (Win32 Platform)  
Originally published: 2009-01-26 09:27:40  
Last updated: 2009-01-26 09:32:34  
Author: Shao-chuan Wang  
  
This program will make your cpu work at a given cpu usage. It should be also able to work on machines with multi-processors. The program has been tested on Windows xp sp2 with python of version 2.5.4.\n\nThe implementation is based on the fact that it will adjust the ratio of being busy over being idle in the main process to approach the target cpu usage rate. 