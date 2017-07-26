#!/usr/bin/env python
# -*- coding: Windows-1251 -*-
'''
File: tail-f.py

Call 'tail -f' for specified file and restarts when file's inode changed
'''
import os
import subprocess
import time

__author__ = 'Denis Barmenkov <denis.barmenkov@gmail.com>'
__source__ = 'http://code.activestate.com/recipes/577398/'

SLEEP_TIME = 1.0 # seconds
DELIM_LINE = '=' * 65
TAIL_PID = None

def get_inode(filename):
    '''get inode for file'''
    if not os.path.exists(filename):
        return None
    else:
        return os.stat(filename)[1]

def kill_tail(pid):
    '''kill tail on specified PID'''
    if pid:
        os.system('kill -9 %d' % pid)

def run_tail(filename):
    '''run tail -f on file, returns tails's PID'''
    if not os.path.exists(filename):
        return None

    process = subprocess.Popen(['tail', '-f', filename], bufsize=1)
    return process.pid

def monitor_file(filename):
    '''main monitor function'''
    global TAIL_PID
    inode = None

    while 1:
        inode_new = get_inode(filename)
        if inode_new != inode:
            kill_tail(TAIL_PID)
            print DELIM_LINE
            print 'restarted: tail -f %s' % filename
            print DELIM_LINE
            TAIL_PID = run_tail(filename)
            inode = inode_new
        else:
            time.sleep(SLEEP_TIME)

def break_handler(signum, frame):
    '''basic interrupt handling'''
    kill_tail(TAIL_PID)
    print
    print DELIM_LINE
    print 'Interrupted by signal %r' % signum
    sys.exit(0)    

if __name__ == '__main__':
    import sys
    import signal

    for sig_name in 'SIGABRT SIGBREAK SIGILL SIGINT SIGTERM'.split():
        if not hasattr(signal, sig_name):
            continue
        sig_id = getattr(signal, sig_name)
        signal.signal(sig_id, break_handler)

    monitor_file(sys.argv[1])
