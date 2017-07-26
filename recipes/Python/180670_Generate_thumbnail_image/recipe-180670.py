#!/usr/bin/env python
# -*- python -*-
#
# Python Thumbnail image generator
#

import os
import sys
import re
import imghdr
from getopt import getopt
from StringIO import StringIO
from PIL import Image # Require PIL module.

class ThumbnailGenerator:
    "Thumbnail image generator."
    default_geom = (100, 100)
    geomfmt = re.compile('(?P<W>\d+)x(?P<H>\d+)')

    def __init__(self):
        self.limit_geom = self.default_geom
        self.outd = '.'
        self.suf = '-thumb'

    def setoutdir(self, outd):
        self.outd = outd

    def setsuffix(self, suf):
        self.suf = suf

    def setbasesize(self, geom):
        matched = self.geomfmt.match(geom)
        if not matched:
            raise ValueError, 'Geometory format is not "XxY"'
        self.limit_geom = (int(matched.group('W')), int(matched.group('H')))

    def generate(self, fn, fp=None):
        "Generate thumbnail."
        im = Image.open(fn)
        im.thumbnail(self.limit_geom)
        base, ext = os.path.splitext(fn)
        if fp: im.save(fp, imghdr.what(fn))
        else: im.save(os.path.join(self.outd, '%s%s%s'%(base, self.suf, ext)))
        return im

    def raw_generate(self, fn):
        "Generate thumbnail (retruns rawdata)"
        im = Image.open(fn)
        im.thumbnail(self.limit_geom)
        buf = StringIO()
        im.save(buf, imghdr.what(fn))
        return buf.getvalue()

def __usage():
    print >>sys.stderr, 'usage: %s [options] imagefile ...' % sys.argv[0]

def __help():
    __usage()
    print '''options:
    -b XxY       base thumbnail size
    -h           print this usage
    -o directory output directory
    -s suffix    thumbnail suffix'''

def __main():
    optdic = {}
    arglist = []
    optlist = []
    tmp = sys.argv[1:]
    while 1:
        opts, tmp = getopt(tmp, 'b:ho:s:')
        if opts: optlist += opts
        if not tmp: break
        arglist.append(tmp[0])
        tmp = tmp[1:]

    # Examine options and filenames.
    if optlist:
        for key, val in optlist:
            if key == '-h':
                __help()
                return
            if optdic.has_key(key):
                raise ValueError, '%s option duplicated' % key
            optdic[key] = val
    if not arglist:
        __usage()
        return

    generator = ThumbnailGenerator()
    if optdic.has_key('-b'): generator.setbasesize(optdic['-b'])
    if optdic.has_key('-o'): generator.setoutdir(optdic['-o'])
    if optdic.has_key('-s'): generator.setsuffix(optdic['-s'])

    # Generate thumbnails.
    for fn in arglist:
        generator.generate(fn)

if __name__ == '__main__':
    try:
        __main()
    except Exception, e:
        print >>sys.stderr, e
        __usage()
        sys.exit(1)
    sys.exit(0)
