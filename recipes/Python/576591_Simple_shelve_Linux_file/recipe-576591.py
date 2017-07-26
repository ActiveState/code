#!/usr/bin/env python
import shelve, os, fcntl, new
import __builtin__
from fcntl import LOCK_SH, LOCK_EX, LOCK_UN, LOCK_NB

def _close(self):
    shelve.Shelf.close(self)
    fcntl.flock(self.lckfile.fileno(), LOCK_UN)
    self.lckfile.close()

def open(filename, flag='c', protocol=None, writeback=False, block=True, lckfilename=None):
    """Open the sheve file, createing a lockfile at filename.lck.  If 
    block is False then a IOError will be raised if the lock cannot
    be acquired"""
    if lckfilename == None:
	lckfilename = filename + ".lck"
    lckfile = __builtin__.open(lckfilename, 'w')

    # Accquire the lock
    if flag == 'r':
	lockflags = LOCK_SH
    else:
	lockflags = LOCK_EX
    if not block:
        lockflags = LOCK_NB
    fcntl.flock(lckfile.fileno(), lockflags)

    # Open the shelf
    shelf = shelve.open(filename, flag, protocol, writeback)

    # Override close 
    shelf.close = new.instancemethod(_close, shelf, shelve.Shelf)
    shelf.lckfile = lckfile 

    # And return it
    return shelf
