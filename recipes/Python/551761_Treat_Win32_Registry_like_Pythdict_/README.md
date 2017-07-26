###Treat the Win32 Registry like a Python dict -- updated

Originally published: 2008-03-11 11:38:50
Last updated: 2008-03-11 11:38:50
Author: Don Dwiggins

This class wraps most of the win32api functions for accessing a registry. It will read and write all win32 registry types, and will de/serialize python objects to registry keys when a string or integer representation is not possible.\n\nThis is an update of recipe 174627, folding in the corrections listed in the discussion there.