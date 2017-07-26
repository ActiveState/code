## converting windows 64 bit time to  python useable formatOriginally published: 2004-09-03 13:05:30 
Last updated: 2004-09-03 13:05:30 
Author: John Nielsen 
 
In Win32 often you'll find time stored in 100-nanosecond intervals since January 1, 1600 UTC. It is stored in a 64-bit value which uses 2 32 bit parts to store the time. The following is a function that returns the time in the typical format the python time libraries use (seconds since 1970).