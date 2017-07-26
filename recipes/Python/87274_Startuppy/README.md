## Startup.py  
Originally published: 2001-11-08 17:32:43  
Last updated: 2001-11-08 17:32:43  
Author: Jim Jinkins  
  
r'''Initialize the Python runtime environment when the interpreter starts.

Local modules are kept in a PythonLib directory instead of site-packages,
so they are not affected by updating, replacing, or removing the Python
directory tree under Windows.