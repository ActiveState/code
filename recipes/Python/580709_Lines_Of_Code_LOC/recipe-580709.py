#! /usr/bin/env python
# -*- coding: utf-8 -*-

# <https://code.activestate.com/recipes/580709-lines-of-code-loc/>

# Basic Lines-Of-Code counter in Python source files, reporting the
# number of blank, comment and source code lines and total number of
# lines in all Python files scanned.

# Usage example:

# % python locs.py -rec ~/Projects
# 8691 *.py files: 365038 blank (14.0%), 212100 comment (8.1%),
#                 2030198 source (77.9%), 2607336 total lines
#                  (2.739 secs, 951872 lines/sec)

# % python3 locs.py -rec ~/Projects
# 8691 *.py files: 365037 blank (14.0%), 212100 comment (8.1%),
#                 2030198 source (77.9%), 2607335 total lines
#                  (2.599 secs, 1003158 lines/sec)

# % python3 locs.py -h
# usage: locs.py [-help] [-recurse] [-verbose] <file_or_dir_name> ...

# Tested with 64-bit Python 2.7.10 and 3.5.1 on MacOS 10.11.6 only.

from glob import iglob
from os.path import basename, exists, isdir, join
from time import time

__all__ = ('Loc',)
__version__ = '16.10.25'


class Loc(object):
    '''Lines-Of-Code accumulator.
    '''
    blank   = 0
    comment = 0
    files   = 0
    source  = 0
    ext     = '.py'

    _time0 = 0

    _recurse = False  # process dirs
    _verbose = False  # print details

    def __init__(self, recurse=False, verbose=False):
        if recurse:
            self._recurse = recurse
        if verbose:
            self._verbose = verbose
        self._time0 = time()

    def __str__(self):
        s = time() - self._time0
        n = self.source + self.comment + self.blank
        p = int(n / s) if n > s > 0 else '-'
        t = ['%s *%s files:' % (self.files, self.ext),
             self._bcst(self.blank, self.comment, self.source),
             '(%.3f secs, %s lines/sec)' % (s, p)]
        return ' '.join(t)

    def _bcst(self, blank, comment, source):
        t, n = [], blank + comment + source
        for a, v in (('blank',   blank),
                     ('comment', comment),
                     ('source',  source)):
            p = ' (%.1f%%)' % ((v * 100.0) / n,) if n > 0 else ''
            t.append('%s %s%s' % (v, a, p))
        t.append('%s total lines' % (n,))
        return ', '.join(t)

    def adir(self, name):
        '''Process a directory.
        '''
        if self._recurse:
            if self._verbose:
                print(' dir %s: %s' % (name, '...'))
                b, c, s = self.blank, self.comment, self.source
                self.aglob(join(name, '*'))
                b = self.blank - b
                c = self.comment - c
                s = self.source - s
                t = name, self._bcst(b, c, s)
                print(' dir %s: %s' % t)
            else:
                self.aglob(join(name, '*'))

    def afile(self, name):
        '''Process a file.
        '''
        if name.endswith(self.ext) and exists(name):
            b = c = s = 0
            with open(name, 'rb') as f:
                for t in f.readlines():
                    t = t.lstrip()
                    if not t:
                        b += 1
                    elif t.startswith(b'#'):  # Python 3+
                        c += 1
                    else:
                        s += 1

            self.blank += b
            self.comment += c
            self.source += s
            self.files += 1
            if self._verbose:
                t = self.files, name, self._bcst(b, c, s)
                print('file %s %s: %s' % t)

    def aglob(self, wild):
        '''Process a possible wildcard.
        '''
        for t in iglob(wild):
            if isdir(t):
                self.adir(t)
            else:
                self.afile(t)


if __name__ == '__main__':

    import sys

    argv0 = basename(sys.argv[0])

    loc = Loc()
    try:
        for arg in sys.argv[1:]:
            if not arg.startswith('-'):
                loc.aglob(arg)

            elif '-help'.startswith(arg):
                print('usage: %s [-help] [-recurse] [-verbose] <file_or_dir_name> ...' % (argv0,))
                sys.exit(0)
            elif '-recurse'.startswith(arg):
                loc._recurse = True
            elif '-verbose'.startswith(arg):
                loc._verbose = True
            elif arg != '--':
                print('%s: invalid option: %r' % (argv0, arg))
                sys.exit(1)

    except KeyboardInterrupt:
        print('')

    print('%s' % (loc,))
