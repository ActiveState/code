#!/usr/bin/env python

## md5hash
##
## 2004-01-30
##
## Nick Vargish
##
## Simple md5 hash utility for generating md5 checksums of files. 
##
## usage: md5hash <filename> [..]
##
## Use '-' as filename to sum standard input.

import md5
import sys

def sumfile(fobj):
    '''Returns an md5 hash for an object with read() method.'''
    m = md5.new()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()


def md5sum(fname):
    '''Returns an md5 hash for file fname, or stdin if fname is "-".'''
    if fname == '-':
        ret = sumfile(sys.stdin)
    else:
        try:
            f = file(fname, 'rb')
        except:
            return 'Failed to open file'
        ret = sumfile(f)
        f.close()
    return ret


# if invoked on command line, print md5 hashes of specified files.
if __name__ == '__main__':
    for fname in sys.argv[1:]:
        print '%32s  %s' % (md5sum(fname), fname)
