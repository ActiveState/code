#!/usr/bin/python
# coding:utf-8

# This script tries to identify all chr(XX) constant calls in python scripts and replace them with '\xXX' strings.

import sys
import re


def chrrepl(match):
    # See http://www.amk.ca/python/howto/regex/regex.html
    # Use the captured group to get the hex string value. 
    char_number = match.group(1)
    return repr(chr(int(char_number)))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python chr_cleaner.py infile.py outfile.py'
        sys.exit(1)
    
    infile = sys.argv[1]
    outfile = sys.argv[2]
    # Open file for reading
    try:
        fin = open(infile, 'r')
        fout = open(outfile, 'w')
    except IOError:
        print 'Error when reading %s or trying to write %s' % (infile, outfile)
        sys.exit(2)
    
    intext = fin.read()
    pattern = 'chr\\((\\d+)\\)' # Group the chr() function parameter to capture it
    p = re.compile(pattern)
    outtext = p.sub(chrrepl, intext)
    fout.write(outtext)
    fout.flush()

    fin.close()
    fout.close()
