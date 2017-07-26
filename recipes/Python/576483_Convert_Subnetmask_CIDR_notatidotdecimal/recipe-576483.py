#!/usr/bin/env python

import sys

def usage():
    print "Call : %s <BitCount>" % sys.argv[0]
    print " shows the dotted netmask (i.e %s 24  => 255.255.255.0)"  % sys.argv[0]


def calcDottedNetmask(mask):
    bits = 0
    for i in xrange(32-mask,32):
        bits |= (1 << i)
    return "%d.%d.%d.%d" % ((bits & 0xff000000) >> 24, (bits & 0xff0000) >> 16, (bits & 0xff00) >> 8 , (bits & 0xff))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        print calcDottedNetmask(int(sys.argv[1]))
    else:
        usage()
