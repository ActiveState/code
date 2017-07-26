#!/usr/bin/env python

import string, sys

text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
_null_trans = string.maketrans("", "")

def istextfile(filename, blocksize = 512):
    return istext(open(filename).read(blocksize))

def istext(s):
    if "\0" in s:
        return 0
    
    if not s:  # Empty files are considered text
        return 1

    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)

    # If more than 30% non-text characters, then
    # this is considered a binary file
    if len(t)/len(s) > 0.30:
        return 0
    return 1

def main(argv):
    import os, getopt
    try:
        args, dirnames = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error:
        args = "dummy"
    if args:
        print "Usage: %s <directory> [<directory> ...]" % (argv[0],)
        print " Shows which files in a directory are text and which are binary"
        sys.exit(0)

    table = {0: "binary", 1: "text"}
    if not dirnames:
        dirnames = ["."]
    for dirname in dirnames:
        try:
            filenames = os.listdir(dirname)
        except OSError, err:
            print >>sys.stderr, err
            continue
        for filename in filenames:
            fullname = os.path.join(dirname, filename)
            try:
                print table[istextfile(fullname)], repr(fullname)[1:-1]
            except IOError:  # eg, this is a directory
                pass
    
if __name__ == "__main__":
    main(sys.argv)
