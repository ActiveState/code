#! /usr/bin/env python
"""
silence.py
Peter Waller 
March 2010
"""

from __future__ import with_statement

from contextlib import contextmanager, nested
from threading import Thread

from tempfile import mkdtemp
from os.path import join as pjoin
from os import (dup, fdopen, open as osopen, O_NONBLOCK, O_RDONLY, remove, 
                rmdir, mkfifo)
from fcntl import fcntl, F_GETFL, F_SETFL
from select import select
from sys import stdout, stderr

from ctypes import PyDLL, CDLL, c_void_p, c_char_p, py_object

pyapi = PyDLL(None)
this_exe = CDLL(None)

def make_fn(what, res, *args):
    what.restype = res
    what.argtypes = args
    return what
    
FILE_p = c_void_p
    
PyFile_AsFile = make_fn(pyapi.PyFile_AsFile, FILE_p, py_object)
freopen = make_fn(this_exe.freopen, FILE_p, c_char_p, c_char_p, FILE_p)

@contextmanager
def fifo():
    """
    Create a fifo in a temporary place.
    """
    tmpdir = mkdtemp()
    filename = pjoin(tmpdir, 'myfifo')
    try:
        mkfifo(filename)
    except OSError, e:
        print >>stderr, "Failed to create FIFO: %s" % e
        raise
    else:
        yield filename
        remove(filename)
        rmdir(tmpdir)

def reader_thread_func(filename, filter_, real_stdout):
    """
    Sit there, reading lines from the pipe `filename`, sending those for which
    `filter_()` returns False to `real_stdout`
    """
    with fdopen(osopen(filename, O_NONBLOCK | O_RDONLY)) as fd:
        while True:
            rlist, _, _ = select([fd], [], [])
            
            line = fd.readline()
            if not line:
                break
                
            elif not filter_(line):
                real_stdout.write(line)

@contextmanager
def threaded_file_reader(*args):
    """
    Operate a read_thread_func in another thread. Block with statement exit
    until the function completes.
    """
    reader_thread = Thread(target=reader_thread_func, args=args)
    reader_thread.start()
    try:
        yield
    finally:
        reader_thread.join()

@contextmanager
def silence(filter_=lambda line: True, file_=stdout):
    """
    Prevent lines matching `filter_` ending up on `file_` (defaults to stdout)
    """
    if not filter_:
        yield
        return
    
    saved_stdout = dup(file_.fileno())
    stdout_file = PyFile_AsFile(file_)
    
    with nested(fdopen(saved_stdout, "w"), fifo()) as (real_stdout, filename):
        with threaded_file_reader(filename, filter_, real_stdout):
            # Redirect stdout to pipe
            freopen(filename, "w", stdout_file)
            try:
                yield
            finally:
                # Redirect stdout back to it's original place
                freopen("/dev/fd/%i" % saved_stdout, "w", stdout_file)

def test():
    
    def filter_stupid(line):
        if line.startswith("Stupid"):
            return True
            
    print "Before with block.."
    
    with silence(filter_stupid):
        print "Stupid output from a C library I don't want to hear"
        print "Sensible stuff!"
        
    print "After the silence block"

if __name__ == "__main__":
    test()
