#!/usr/bin/env python

import sys
import time
import subprocess

"""
Keep a process up and running

If you have a long running process that can be killed for strange and unknown
reason, you might want it to be restarted ... this script does that.

$ cat alive.sh 
#!/bin/sh

while `true`; do echo Alive && sleep 3 ; done

Use it like this:
$ keepup.py ./alive.sh 
"""

cmd = ' '.join(sys.argv[1:])

def start_subprocess():
    return subprocess.Popen(cmd, shell=True)

p = start_subprocess()

while True:
    
    res = p.poll()
    if res is not None:
        print p.pid, 'was killed, restarting it'
        p = start_subprocess()

    time.sleep(1)
