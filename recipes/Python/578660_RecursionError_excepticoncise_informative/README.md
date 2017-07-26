## RecursionError exception: concise and informative outputOriginally published: 2013-09-17 00:23:58 
Last updated: 2015-07-05 23:46:59 
Author: elazar  
 
Replaces the default exception hook with one that, upon "infinite recursion", removes the last cycle. This results in a significantly cleaner and shorter error message.\n\nUsage: simply import <module> as _\n\nFor more details see the descussion here:\nhttps://mail.python.org/pipermail/python-ideas/2013-September/023190.html