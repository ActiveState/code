from __future__ import print_function

# which.py
# A minimal version of the UNIX which utility, in Python.
# Author: Vasudev Ram - www.dancingbison.com
# Copyright 2015 Vasudev Ram - http://www.dancingbison.com

import sys
import os
import os.path
import stat

def usage():
    sys.stderr.write("Usage: python which.py name\n") 
    sys.stderr.write("or: which.py name\n") 

def which(name):
    found = 0 
    for path in os.getenv("PATH").split(os.path.pathsep):
        full_path = path + os.sep + name
        if os.path.exists(full_path):
            """
            if os.stat(full_path).st_mode & stat.S_IXUSR:
                found = 1
                print(full_path)
            """
            found = 1
            print(full_path)
    # Return a UNIX-style exit code so it can be checked by calling scripts.
    # Programming shortcut to toggle the value of found: 1 => 0, 0 => 1.
    sys.exit(1 - found)

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    which(sys.argv[1])

if "__main__" == __name__:
        main()
