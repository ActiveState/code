## Treat the Win32 Registry like a Python dict -- updated (again!)  
Originally published: 2008-06-20 21:46:28  
Last updated: 2008-06-21 08:12:09  
Author: Chris Melville  
  
This class wraps most of the win32api functions for accessing a registry. It will read and write all win32 registry types, and will de/serialize python objects to registry keys when a string or integer representation is not possible.

This is an update of recipe 551761, which is in turn an update of 174627, folding in the enhancements listed in the discussion there to allow registry value types to be read and written within the dictionary metaphore if required. It doesnt change how it worked before, it adds a new capability, and shouldnt break existing code using the 551761 version.