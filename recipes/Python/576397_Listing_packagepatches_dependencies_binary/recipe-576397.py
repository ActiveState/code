#!/usr/bin/env python
''' 
== Infos == 

Print (1) packages used by a binary, and (2) the list of installed patches
related to these packages. If you have a binary that works with Solaris 10 update N, but doesn't with Solaris 10 update N-2, run this script on both platform and it will help you to find the patches you're looking for.
 
(1) is retrieved: 
 * By using pldd(pid) on the process you want to trace to get a list of loaded
   shared library 

 * By retrieving in the main /var/sadm/install/contents database
   the list of package related to these shared libraries

(2) is retrieved by parsing the output of the showrev -p command, given as
input of this script

Requires Python 2.3 (Set module usage)

== Usage == 

Use the -h / --help switch for options.

# give it a pid
$ pldd2pkg.py -p `pgrep dtexec` 

# give it a file (offline)
$ pldd 732 > /tmp/foobar
$ pldd2pkg.py -l /tmp/foobar 

Written by Benjamin Sergeant: bsergean@gmail.com
'''

import sys
from optparse import OptionParser
from sets import Set
from commands import getoutput
from cStringIO import StringIO

def uniq(alist): # Fastest order preserving
    ''' Helper from comments in http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52560 '''
    set = {}
    return [set.setdefault(e,e) for e in alist if e not in set]

def package_info(p):
    ''' 
    $ pkginfo SUNWglrt
    application SUNWglrt       Sun OpenGL for Solaris Runtime Libraries
    '''
    output = getoutput('pkginfo %s' % p)
    return (' ').join(output.split()[2:])

def showrev_minus_p():
    print 'Get a list of patches installed on the system with `showrev -p`'
    return getoutput('showrev -p')

def pldd(pid):
    return getoutput('pldd %s' % pid)

def main(pldd_fo):
    # Read list of libraries from pldd output
    # First name is name of binary
    binaries = pldd_fo.read().splitlines()
    shared_libraries = binaries[1:]
    executable       = binaries[0]

    # Create a map between files and SVR4 packages
    map_files_package = {}
    map_files_package_lines = open('/var/sadm/install/contents').read().splitlines()
    for l in map_files_package_lines:
        tokens = l.split()
        # we are only interested in regular files
        if tokens[1] == 'f':
            fn, pkg = tokens[0], tokens[-1] 
            map_files_package[fn] = pkg

    # Output
    print executable
    for f in shared_libraries:
        if f in map_files_package:
            print '\t', f, ' -> ', map_files_package[f]
        else:
            print '\t', f, ' -> ', '(Not found)'
    print

    print 'package used:'
    pkg_used = [map_files_package[f] for f in shared_libraries if f in map_files_package]
    pkg_used = uniq(pkg_used)
    pkg_used_set = Set(pkg_used)
    for p in pkg_used:
        print '\t', p, ' -> ', package_info(p)
    print

    # Create a map between patch and SVR4 packages
    map_patch_package = {}
    showrev_fo = StringIO(showrev_minus_p())
    map_patch_package_lines = showrev_fo.read().splitlines()
    for l in map_patch_package_lines:
        # Patch: 108806-17 Obsoletes:  Requires:  Incompatibles:  Packages: SUNWqfed, SUNWqfedu
        patch = l.split()[1]

        tokens = l.split(':')
        packages = [p.strip() for p in tokens[5].split(',')]
        packages_set = Set(packages)

        if packages_set & pkg_used_set:
            map_patch_package[patch] = packages

    # Output used patch / per patch
    print 'patch related to package used:'
    for k, v in map_patch_package.iteritems():
        print '\t', k, ' -> ', (', ').join(v) 
    print

    # Output used patch / per package
    print 'patch related to package used:'
    for p in pkg_used:
        print '\t', p, ' -> ', package_info(p)

        patches = [k for k, v in map_patch_package.iteritems() if p in v]
        patches.sort()
        for p in patches:
            print '\t\t', p
    print

if __name__ == "__main__":
    # parse args
    parser = OptionParser(usage = "usage: %prog <options>")

    parser.add_option("-p", "--pid", dest="pid", default='',
            help="The pid of the process to analyse")
    parser.add_option("-l", "--pldd-file", dest="pldd_fn", default='',
            help="offline: The file captured output of the pldd pid command")

    options, args = parser.parse_args()
    if options.pldd_fn:
        pldd_fo = open(options.pldd_fn)
    elif options.pid:
        pldd_fo = StringIO(pldd(options.pid))

    main(pldd_fo)
