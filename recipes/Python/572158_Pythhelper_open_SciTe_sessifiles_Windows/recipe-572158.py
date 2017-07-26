# script to load SciTe .session files by double-clicking them in Windows Explorer

# the .session file type must be present and its 'open" command associated with :
# "/path/to/python.exe" "/path/to/scite.py"  "%1"

# NOTE: /path/to/scite.py MUST be the same as /path/to/scite.exe !

# Example :
# "c:\python\python.exe"  "c:\program files\wscite\wscite.py"  "%1"

import sys, os, subprocess

# argv[0] is the full path to where this python script was launched from
# it must be in the same directory as the SciTe executable !
# argv[1] is the full path to the scite session file we want to load
script, sessionpath = sys.argv

# this gives us the path to the scite executable
scite = script[:-2] + 'exe'

# this gives us the basename of the session file and the directory it is in
sessiondir, sessionname = os.path.split(sessionpath)

# here we switch to the session file dir and launch scite with just the file name as the loadsession parm
subprocess.Popen([scite, "-loadsession:%s" % sessionname], cwd = sessiondir)

# script ends without waiting for command completion
