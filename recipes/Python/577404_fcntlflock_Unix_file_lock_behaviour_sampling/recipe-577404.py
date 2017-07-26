#!/usr/bin/python
# Unix/Linux only (as the 'fcntl' module is). Python >=2.6/3.x compatibile.
# Copyright (c) 2010 Jan Kaliszewski (zuo). Licensed under the MIT License.

"""
flocktests.py: fcntl.flock(LOCK_EX|LOCK_NB) behaviour sampling -- with one
file object or separate file objects (pointing to the same filesystem path),
with/without threading or forking.
"""

from __future__ import print_function

import os
import sys
import threading

from fcntl import flock, LOCK_EX, LOCK_UN, LOCK_NB
from os.path import basename


class lockpath(object):

    "Open a file, flock it, generate appropriate info, unflock if necessary"

    def __init__(self, path, _keep=False):
        "By default, unflock/close the file immediately after setting the lock"
        self.file = file = open(path, 'a')
        locked = _lockonly(file)
        if _keep:
            self.locked = locked
        else:
            file.close()
            self.locked = False

    @classmethod
    def keeping(cls, path):
        "Constructor for with-blocks: tries to keep the file open and flocked"
        return cls(path, _keep=True)

    def __enter__(self):
        "Enter a with-block binding the file to the as-clause target"
        if self.locked:
            return self.file
        else:
            raise RuntimeError('lockpath().file is not locked '
                               '-- cannot enter the with-block')

    def __exit__(self, *args, **kwargs):
        "Leave the with-block closing the file (=> unflocking it)"
        self.file.close()


def _help(*args):
    print('\n  '.join(args), file=sys.stderr)

def _msg(*args):
    print('pid:{0}'.format(os.getpid()),
          threading.current_thread().name,
          *args)

def _lockonly(file):
    _msg('got file #', file.fileno())
    try:
        flock(file, LOCK_EX | LOCK_NB)
    except IOError:
        _msg('failed to lock')
        return False
    else:
        _msg('locked successfully')
        return True

def lockfile(file):
    "flock a given file, then unflock it immediately"
    if _lockonly(file):
        flock(file, LOCK_UN)

# Options

def n(path):
    "one file object + no concurrency"
    with lockpath.keeping(path) as file:
        lockfile(file)

def N(path):
    "separate file objects + no concurrency"
    with lockpath.keeping(path):
        lockpath(path)

def t(path):
    "one file object + threading"
    with lockpath.keeping(path) as file:
        t = threading.Thread(target=lockfile, args=(file,))
        t.start()
        t.join()

def T(path):
    "separate file objects + threading"
    with lockpath.keeping(path):
        t = threading.Thread(target=lockpath, args=(path,))
        t.start()
        t.join()

def f(path):
    "one file object + forking"
    with lockpath.keeping(path) as file:
        if os.fork():
            os.wait()
        else:
            lockfile(file)

def F(path):
    "separate file objects + forking"
    with lockpath.keeping(path):
        if os.fork():
            os.wait()
        else:
            lockpath(path)


OPTIONS = 'nNtTfF'

def main(program, option='', path='test.flock'):
    "Do one of the tests or print a short help"
    flocktests = globals()
    option = option.lstrip('-')
    if option and (option in OPTIONS):
        function = flocktests[option]
        function(path)
    else:
        _help(__doc__.lstrip())
        _help('Usage: {0} OPTION [PATH]'.format(basename(program)),
              'Default PATH: test.flock', 'OPTIONS:',
              *('-{0}  {1}'.format(option, flocktests[option].__doc__)
                for option in OPTIONS))


if __name__ == '__main__':
    main(*sys.argv)
