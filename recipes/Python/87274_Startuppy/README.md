###Startup.py

Originally published: 2001-11-08 17:32:43
Last updated: 2001-11-08 17:32:43
Author: Jim Jinkins

r'''Initialize the Python runtime environment when the interpreter starts.\n\nLocal modules are kept in a PythonLib directory instead of site-packages,\nso they are not affected by updating, replacing, or removing the Python\ndirectory tree under Windows.