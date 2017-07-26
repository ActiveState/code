## Treat the Win32 Registry like a Python dict 
Originally published: 2003-01-18 20:51:54 
Last updated: 2003-01-18 20:51:54 
Author: Bob Ippolito 
 
This class wraps most of the win32api functions for accessing a registry.  It will read and write all win32 registry types, and will de/serialize python objects to registry keys when a string or integer representation is not possible.