#!/usr/bin/env python

"""Find duplicate file names.

Command line options:
  h - show help on usage
  s - compare file sizes
  n <text> - restrict to names containing text
  r <regex> - restrict to names containing regex match (overrides -n)

The non-option parameters, if specified, are used as search path.
Otherwise, current directory is used.
"""

import getopt
import os
import os.path
import re
import sys

def addIfFile(allfiles, dirname, file):
    if os.path.isfile(os.path.join(dirname, file)):
        if file in allfiles:
            allfiles[file].append(dirname)
        else:
            allfiles[file] = [dirname]

def checkdup(allfiles, dirname, files):
    for n in files:
        addIfFile(allfiles, dirname, n)

class CheckdupName:
    def __init__(self, name):
        self.__name = name
    def __call__(self, allfiles, dirname, files):
        for n in files:
            if self.__name in n:
                addIfFile(allfiles, dirname, n)

class CheckdupRegex:
    def __init__(self, pattern):
        self.__re = re.compile(pattern)
    def __call__(self, allfiles, dirname, files):
        for n in files:
            if self.__re.search(n):
                addIfFile(allfiles, dirname, n)

class HelpException(Exception):
    pass

def printDupNames(duplist):
    for n, d in duplist:
        for dd in d:
            pj = os.path.normpath(os.path.join(dd, n))
            print pj
        print

def printDupNameSizes(duplist):
    for n, d in duplist:
        szgroups = {}
        for dd in d:
            pj = os.path.normpath(os.path.join(dd, n))
            sz = os.stat(pj).st_size
            if sz in szgroups:
                szgroups[sz].append(pj)
            else:
                szgroups[sz] = [pj]
        for sz, g in szgroups.iteritems():
            if len(g) > 1:
                for n in g:
                    print n
                print

def main(argv):
    optlist, args = getopt.getopt(argv, "hsn:r:")
    visit = checkdup
    prndup = printDupNames
    for o, a in optlist:
        if o == "-h":
            raise HelpException()
        if o == "-s":
            prndup = printDupNameSizes
        if o == "-n":
            visit = CheckdupName(a)
        if o == "-r":
            visit = CheckdupRegex(a)
    paths = ["."]
    if args:
        paths = args
    allfiles = {}
    for path in paths:
        os.path.walk(path, visit, allfiles)
    duplist = [x for x in allfiles.iteritems() if len(x[1])>1]
    duplist.sort()
    prndup(duplist)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except getopt.GetoptError, e:
        print >> sys.stderr, e
        print >> sys.stderr, "Try '%s -h' for help." % sys.argv[0]
        raise SystemExit(2)
    except re.error, e:
        print >> sys.stderr, "Malformed regex pattern:"
        print >> sys.stderr, e
        raise SystemExit(2)
    except HelpException, e:
        print "Usage: %s [options] [path [path ...]]" % sys.argv[0]
        print
        print __doc__
