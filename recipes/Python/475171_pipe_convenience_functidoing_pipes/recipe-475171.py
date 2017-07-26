#!/usr/bin/env python

import os
import subprocess
import sys
import StringIO

def cmdtolist(str):
    cmdlist=[]
    current=[]
    gc=''
    last=''
    for c in str:
        if (c == '\\'):
            pass
        elif (last == '\\'):
            current.append(c)
        elif (gc != ''):
            if (c != gc):
                current.append(c)
            else:
                gc=''
        else:
            if (c.isspace()):
                cmdlist.append(''.join(current))
                current = []
            elif (c == '"'):
                gc = c
            elif (c == "'"):
                gc = c
            else:
                current.append(c)
        last = c
    if (len(current) != 0):
        cmdlist.append(''.join(current))
    return cmdlist

def pipe(*cmds):
    def func():
        pass
    def norm(cmd):
        if (isinstance(cmd, str)):
            return cmdtolist(cmd)
        return cmd
    def pipeobj(cmd, stdin=None):
        if (callable(cmd)):
            fp = Fpipe(cmd, stdin)
            fp.call()
            fp.stdout.seek(0)
            return fp
        if (stdin is None):
            return subprocess.Popen(norm(cmd), stdout=subprocess.PIPE)
        else:
            return subprocess.Popen(norm(cmd), stdin=stdin, stdout=subprocess.PIPE)
    if (len(cmds) == 0):
        return
    prev = None
    for cmd in cmds:
        if (prev is None):
            prev = pipeobj(cmd)
        else:
            prev = pipeobj(cmd, stdin=prev.stdout)
    return prev.stdout

class Fpipe:
    def __init__(self, fn, stdin=None):
        self.fn = fn
        self.stdin = stdin
        self.stdout = StringIO.StringIO()
    def call(self):
        self.fn(self.stdin, self.stdout)
