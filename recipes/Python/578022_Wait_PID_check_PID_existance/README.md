## Wait for PID and check for PID existance (POSIX)Originally published: 2012-01-20 19:07:58 
Last updated: 2012-04-15 14:13:02 
Author: Giampaolo Rodolà 
 
Two functions: one which waits for a certain PID to terminate (with optional timeout), another one which checks whether a process with a given PID is running.\n\nThis was extracted from [psutil](http://code.google.com/p/psutil/) project which also provides a Windows implementation.\n\nTimeout functionality is implemented as a busy loop and it was inspired by http://bugs.python.org/issue5673.