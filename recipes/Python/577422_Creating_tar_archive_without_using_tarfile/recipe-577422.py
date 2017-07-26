#!/usr/bin/env python
''' Create tar archives the hard way.

The python tarfile module does that much better but it's more 
an exercise and fun to see very little code is needed to manage to 
create a tarball.

Support only the original tar format. 
http://en.wikipedia.org/wiki/Tar_(file_format)
'''

import os, sys
from os.path import getsize, isfile, isdir, islink
from os import stat

def write_header(f, fn):
    '''
    100	 name	 name of file
    8	 mode	 file mode
    8	 uid	 owner user ID
    8	 gid	 owner group ID
    12	 size	 length of file in bytes
    12	 mtime	 modify time of file
    8	 chksum	 checksum for header
    1	 link	 indicator for links
    100	 linkname	 name of linked file
    '''
    def rpad(s, size):
        L = len(s)
        return s + (size - L) * '\0'
        
    header  = rpad(fn, 100) 
    header += rpad('%o' % stat(fn).st_mode, 8)
    header += rpad('%o' % stat(fn).st_uid, 8)
    header += rpad('%o' % stat(fn).st_gid, 8)
    size = getsize(fn) if isfile(fn) else 0
    header += rpad('%o' % size, 12)
    header += rpad('%o' % stat(fn).st_mtime, 12)
    header += 8 * '\0' # 8 zeros while the cksum is computed
    if islink(fn): header += 1 * '2'
    elif isfile(fn): header += 1 * '0'
    elif isdir(fn): header += 1 * '5'
    if islink(fn): header += rpad(os.readlink(fn), 100)
    else: header += 100 * '\0'

    # the checksum part is shamelessy stolen from the tarfile module 
    # with little edit
    cksum = 256 + sum(ord(h) for h in header)
    header = rpad(header, 512)
    header = header[:-364] + '%06o\0' % cksum + header[-357:]

    f.write( header )

def write_body(f, fn):
    fo = open(fn)
    bytes = fo.read()
    fo.close()

    f.write(bytes)
    zeros = 512 - len(bytes) % 512
    f.write(zeros * '\0')

def write(files, out):
    f = open(out, 'wb')

    for fn in files:
        write_header(f, fn)
        if isfile(fn) and not islink(fn): write_body(f, fn)

    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: batar.py <tar archive> [files | directories]'
    else:
        write(sys.argv[2:], sys.argv[1])
    
