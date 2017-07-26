# -*- coding: utf8 -*-
# author: Jiri Zahradil, jiri.zahradil@gmail.com

import os, time, sys, os.path

def svn(cmdline):
    SVNBINARY = r"svn" # your path to svn binary
    print "run: svn "+cmdline
    os.system(SVNBINARY +" "+cmdline)
    
def mylistdir(path):
    return (f for f in os.listdir(path) if (f and not f.startswith(".") and not os.path.isdir(f)))
    
path_to_watch = "." if (len(sys.argv)<=1) else sys.argv[1]
start_dir = os.getcwd()

try:
    os.chdir(path_to_watch)
    path_to_watch = "."
    print "Watching",os.getcwd()    
    before = dict ([(f, os.path.getmtime(f)) for f in mylistdir(path_to_watch)])
    svn("add -q "+" ".join(before))
    svn("ci -q . -m \"watching start\"")
    msg = " -m \"auto-commit\""    
    while 1: 
        time.sleep (5) 
        after = dict ([(f, os.path.getmtime(f)) for f in mylistdir(path_to_watch)])
        
        modified = [f for f,ts in after.iteritems() if ts>before.get(f,ts)]
        added = [f for f in after if not f in before] 
        removed = [f for f in before if not f in after]
        if added:
            svn("add -q "+" ".join(added))
            print "Added: ", ", ".join (added)            
        if removed:
            svn("rm -q "+ " ".join(removed))
            print "Removed: ", ", ".join (removed)            
        if modified:
            print "Modified: ", ", ".join (modified)
            
        if added or removed or modified:
            svn("ci -q ."+msg)
    
        before = after      
    pass

finally:
    os.chdir(start_dir)
