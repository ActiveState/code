#/usr/bin/python
# fib.py
"""
Number generator

Uses cPickle to save and load previously calculated numbers. Could be improved to use databases or
other mathods which are faster.
"""

import os
from cPickle import dump, load, HIGHEST_PROTOCOL

class LoadableDict(dict):

    def __init__(self, filename="loadeddict.dict", *args, **kw):
        dict.__init__(self, *args, **kw)
        self.filename = filename
        self.load()

    def load(self, filename=None):
        filename = filename or self.filename
        if not os.path.exists(filename):
            return
        with open(filename, "rb") as f:
            d = load(f)
            assert isinstance(d, dict)
            self.loaddict(d)

    def loaddict(self, d):
        for key, value in d.iteritems():
            self[key] = value
        
    def save(self, filename=None):
        filename = filename or self.filename
        with open(filename, "wb") as f:
            dump(self, f, HIGHEST_PROTOCOL)

    def __del__(self):
        self.save()

try:
    _mem = LoadableDict("fib.dict", {1: 0, 2: 1})
except MemoryError:
    os.remove("fib.dict")
    _mem = LoadableDict("fib.dict", {1: 0, 2: 1})

def fib(n):
    if n in _mem:
        return _mem[n]
    for i in xrange(1, n+1):
        if i in _mem:
            continue
        else:
            _mem[i] = _mem[i-1] + _mem[i-2]
    return _mem[n]

def fibrange(start, stop=None, step=1):
    if stop is None:
        stop, start = start, 0
    return (fib(n+1) for n in xrange(start, stop, step))
