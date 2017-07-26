#!/usr/bin/env python
# -*- python -*-

"""
Image finder. Usage is run this script with no arguments. :)
"""

import os
import sys
import re
from getopt import getopt
from PIL import Image

class ImageScanner:
    def __init__(self):
        self.maxsize = (1000, 1000)
        self.minsize = (0, 0)
        self.printsize = 1
        self.verbose = 0

    def __parsesize(self, geom):
        matched = re.match('(?P<W>\d+)x(?P<H>\d+)', geom)
        if not matched:
            raise ValueError, 'Geometory format is not "XxY"'
        return (int(matched.group('W')), int(matched.group('H')))

    def setmaxsize(self, geom):
        self.maxsize = self.__parsesize(geom)

    def setminsize(self, geom):
        self.minsize = self.__parsesize(geom)

    def setnoprint(self):
        self.printsize = 0

    def setverbose(self):
        self.verbose = 1

    def scan(self, fn):
        try:
            size = Image.open(fn).size
            if self.maxsize >= size and self.minsize <= size:
                if self.printsize or self.verbose:
                    return fn + ' %dx%d' % size
                return fn
        except: pass
        if self.verbose:
            return fn + ' nil'
        return None

    def __recursivescan(self, arg, path, dirlist):
        for d in dirlist:
            self.__tmpbuf.append(self.scan(os.path.join(path, d)))
    def recursivescan(self, args):
        self.__tmpbuf = []
        for arg in args: os.path.walk(arg, self.__recursivescan, None)
        return self.__tmpbuf

def __list(arg, path, dirlist):
    return

def __usage():
    print >>sys.stderr, 'usage: %s [options] imagefile ...' % sys.argv[0]
    print >>sys.stderr, '''options:
    -h     print this usage
    -M XxY filter maximum image size
    -m XxY filter minimum image size
    -n     do not print size
    -r     recursive
    -v     verbose'''

def __main():
    optdic = {}
    arglist = []
    optlist = []
    tmp = sys.argv[1:]
    while 1:
        opts, tmp = getopt(tmp, 'hm:M:nrv')
        if opts: optlist += opts
        if not tmp: break
        arglist.append(tmp[0])
        tmp = tmp[1:]

    # Examine options and filenames.
    if optlist:
        for key, val in optlist:
            if key == '-h':
                __usage()
                return
            if optdic.has_key(key):
                raise ValueError, '%s option duplicated' % key
            optdic[key] = val
    if not arglist:
        raise ValueError, 'requires filename'

    scanner = ImageScanner()
    if optdic.has_key('-M'): scanner.setmaxsize(optdic['-M'])
    if optdic.has_key('-m'): scanner.setminsize(optdic['-m'])
    if optdic.has_key('-n'): scanner.setnoprint()
    if optdic.has_key('-v'): scanner.setverbose()

    if optdic.has_key('-r'):
        for data in filter(lambda a:a, scanner.recursivescan(arglist)):
            print data
    else:
        for data in filter(lambda a:a, map(scanner.scan, arglist)): print data

if __name__ == '__main__':
    try:
        __main()
    except Exception, e:
        print >>sys.stderr, e
        __usage()
        sys.exit(1)
