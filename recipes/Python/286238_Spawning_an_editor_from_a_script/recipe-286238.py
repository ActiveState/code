#!/usr/bin/env python

import os
from tempfile import NamedTemporaryFile

def edit(filehandle):
    """spawns an editor returns the file as a string; by default uses emacs if
    EDITOR is not defined in the environment, expects a filehandle as returned
    by NamedTemporaryFile()"""
    editor = os.getenv('EDITOR','emacs')
    x = os.spawnlp(os.P_WAIT,editor,editor,filehandle.name)
    if x != 0:
        print "ERROR"
    return filehandle.read()

if __name__=='__main__':
    fd = NamedTemporaryFile()
    text = edit(fd)
