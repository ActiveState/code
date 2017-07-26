#!/bin/env/python
import os

# figure out what user I am:
myusr = os.popen("/usr/bin/whoami").read().strip()

# see if pine is already running for me:
pines = os.popen("/usr/bin/pgrep -u %s pine" % myusr).read().split()

# but *this* script is called pine, so take it out of the list:
mypid = str(os.getpid())
pines.remove(mypid)

if pines:
    print "pine is already running."
else:
    # replace this process with the real thing:
    os.execv("/usr/bin/pine", [""])
