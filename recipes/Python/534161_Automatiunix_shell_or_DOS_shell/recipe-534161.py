#!/usr/bin/env python

import os, shutil, sys

try:
    mibsToCompile = sys.argv[1]
except IndexError:
    print "addmibs.py - This program requires HP Systems Insight Manager"
    print "             to be installed."
    print "             This program adds mib files in a directory to the"
    print "             Systems Insight Manager '/mibs' directory and compiles"
    print "             them and then registers them with the system."
    print
    print "Useage: <python> addmibs.py [directory containing .mib files]"
    sys.exit(1)

# validate input
if os.path.isdir(mibsToCompile):
    mibsToCompile = os.path.abspath(mibsToCompile)
else:
    print mibsToCompile, 'is not a valid directory.'
    sys.exit(1)

# get path to HP SIM's mibs directory
for pathChunk in os.getenv("PATH").split(os.pathsep):
    if pathChunk.count("Systems Insight Manager"):
        hpMibsPath = pathChunk[:pathChunk.rfind(os.sep)+1] + "mibs"
        if os.path.isdir(hpMibsPath):
            break
        else:
            print "No valid mibs directory found in the Systems Insight Manager"
            print "directory."
            sys.exit(1)
    else:
        print "No Systems Insight Manager directory found in your system's"
        print "PATH."
        sys.exit(1)

# parse out mibs
mibFiles = []
for file in os.listdir(mibsToCompile):
    if file.endswith(".mib"):
        mibFiles.append(file)

# move mibs
if mibFiles:
    for file in mibFiles:
        shutil.move(mibsToCompile + os.sep + file, hpMibsPath)
else:
    print "No mib files found in %s" % mibsToCompile
    sys.exit(1)

# compile and register mibs
os.chdir(hpMibsPath)
for file in mibFiles:
    os.system("mcompile %s" % file)
    os.system("mxmib -a %s" % file[:-4] + ".cfg")

print "Done."
