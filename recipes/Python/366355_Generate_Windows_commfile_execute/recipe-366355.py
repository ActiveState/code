# MkPyCmd.py
# Copyright 2005 by James M Jinkins --- Released to the Public Domain.
# email address: jim -dot_ jinkins -at_ comports -dot_ com

progDoc = r"""MkPyCmd.py generates a command file to execute a Python program.

The windows command file will have the same filename as the Python program, but 
will have a '.cmd' extension instead of '.py..  It will pass its command line 
arguments to the Python program.

Note:

usage:      python [py_path\]python_program [cmd_path]
  where
    py_path         Optional path to the python program.  Default is the
                    current directory.  
    python_program  Python program.  Since the extension must be .py,
                    it is not required.
    cmd_path        Optional path to the generated command file.  Default is 
                    the current directory.  Generate it in a directory in the 
                    PATH environment variable.
The command
    python C:\PyLib\MkPyCmd.py C:\PyLib\my_prog C:\cmd
generates file C:\cmd\my_prog.cmd, which contains this line:
    python "C:\PyLib\my_prog.py" %*
"""

import os
import sys

def displayErrMsgExit(msg = ''):
    print progDoc
    if msg:
        print "\nError: %s" % msg
    sys.exit(1)


if (len(sys.argv) < 2 or sys.argv[1].lower() == '-h' or 
        sys.argv[1].lower() == '--help'): 
    displayErrMsgExit()
if len(sys.argv) > 3:
    displayErrMsgExit("Too many command line arguments")
pyProgram = sys.argv[1]
pyProgPath = os.path.abspath(pyProgram) 
pyPath, pyFilespec = os.path.split(pyProgPath)
pyFilename, pyExt = os.path.splitext(pyFilespec)
if pyExt.lower() == '.py':
    cmdFilespec = pyFilename + '.cmd'
else:
    cmdFilespec = pyFilespec + '.cmd'
    pyProgPath += '.py'
if not os.path.isfile(pyProgPath):
    displayErrMsgExit("python_program file '%s' not found" % pyProgramPath)
if len(sys.argv) > 2:
    if not os.path.isdir(sys.argv[2]):
        displayErrMsgExit("cmd_path arg '%s' is not a directory" % 
                sys.argv[2])
    cmdPath = os.path.join(sys.argv[2], cmdFilespec)
else:
    cmdPath = cmdFilespec
f = open(cmdPath, 'w')
print >>f, 'python "%s" %%*' % pyProgPath 
f.close()
