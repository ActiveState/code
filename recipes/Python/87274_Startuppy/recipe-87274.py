# Startup.py
r'''Initialize the Python runtime environment when the interpreter starts.

Local modules are kept in a PythonLib directory instead of site-packages,
so they are not affected by updating, replacing, or removing the Python
directory tree under Windows.

This program appends the PythonLib directory, where this program resides,
to sys.path.  It also appends all the first-level subdirectories except
PythonLib\Override.

If directory PythonLib\Override exists insert it in sys.path immediately
after the current directory and before everything else, so it can be used
to override standard modules if necessary.

Otherwise make minimal changes to the Python runtime environment, so
scripts developed on this system will be portable.

To use this program create a PythonLib directory; copy this program into
it; and set environment variable PYTHONSTARTUP to the fully qualified
pathname of this program, e.g. 'C:\Programs\PythonLib\Startup.py'.

Copyright 2001 by James M Jinkins.  Released under the Python License.
'''

# Import new language features from __future__ to insure that programs
# developed on this system will run under Python 2.2.
# For older code this conflicts with "minimal changes to the Python
# runtime environment."
# from __future__ import division
# from __future__ import generators
# from __future__ import nested_scopes

# Add directories to sys.path
import os, sys
startupDir = os.path.dirname(os.getenv("PYTHONSTARTUP"))
sys.path.append(startupDir)
for file in os.listdir(startupDir):
    path = os.path.join(startupDir, file)
    if os.path.isdir(path):
        if file.lower() == "override":
            sys.path.insert(2, path)
        else:
            sys.path.append(path)

# Cleanup the global namespace
del(sys)
del(os)
del(startupDir)
del(file)
del(path)
