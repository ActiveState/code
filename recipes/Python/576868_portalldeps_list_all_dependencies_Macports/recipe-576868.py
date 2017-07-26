#!/usr/bin/env python
"""
port-alldeps package ...
lists all dependencies of Macports packages -- 1st 2nd 3rd level ...
by repeatedly calling "port deps".
Example:
    port deps pandoc ->
        pandoc has build dependencies on:
                ghc
                haddock
        pandoc has library dependencies on:
                gmp

    port-alldeps pandoc ->
        pandoc*    -> ghc haddock* gmp
        ghc        -> readline gmp perl5.8
        haddock*   -> ghc hs-ghc-paths*
        gmp        ->
        readline   -> ncurses
        perl5.8    ->
        hs-ghc-paths* -> ghc
        ncurses    -> ncursesw
        ncursesw   ->

"*" marks packages that are not installed.
Thus port-alldeps | egrep '\*  *->'  lists what has to be built:
    pandoc*    -> ghc haddock* gmp
    haddock*   -> ghc hs-ghc-paths*
    hs-ghc-paths* -> ghc

"port list installed" is run first, which may be slow.
To use a file instead,
    port list installed > date.portsinstalled
    export Macportsinstalled=date.portsinstalled

"""

# breadth-first, not topo sorted
# alldeps-dot | graphviz not so hot, see aewm.png
# "port deps" is slow, one exec per dep is slower:
#   alldeps ImageMagick 14 sec, port -F 9 sec

# http://en.wikipedia.org/wiki/Macports ff

# alternate approach: cache the whole deps graph, 4k nodes
# google "package dependency graph" ...
# really need a short Howto edit portfiles to ignore some deps


#...............................................................................
import os
import subprocess
import sys

__date__ = "4aug 2009"  # 27oct 2008
__author_email__ = "denis-bz-py at t-online dot de"

#...............................................................................
def execv( cmd_arg_list ):
    """ execvp [cmd, args ...] -> [line ...]
    """
    out, err = subprocess.Popen( cmd_arg_list, stdout=subprocess.PIPE, shell=False ) \
        .communicate()  # wait til process ends
    lines = out.split( "\n" )
    if lines:  lines.pop()  # "" after \n at the end
    return lines

def macport( args ):
    """ port args -> [lines]
        (exec each call, slow)
    """
        # <-> one running process ? try Pexpect ?
    return execv( ["port"] + args.split() )  # in $PATH

installed = {}
Macportsinstalled = os.getenv( "Macportsinstalled", None )

def port_installed():
    """ port list installed -> installed[ mod ... ] """
    if Macportsinstalled:
        lines = open( Macportsinstalled ) .readlines()
    else:
        print >>sys.stderr, "running \"port list installed\" ..."
        lines = macport( "list installed" )
    for line in lines:
        mod, version = line.split()[0:2]
        installed[mod] = version
    print "# info: %d ports are installed" % len(installed)

#...............................................................................
def port_deps( mod ):
    """ -> [deps] or [] """
    deps = []
    for line in macport( "deps " + mod ):
        if not (line.endswith( ":" ) \
        or      line.endswith( " has no dependencies" )):
            deps.append( line.strip() )
    return deps

#...............................................................................
def deco( mod ):
    return mod if mod in installed  else (mod + "*")

def print_deps( mod, deps ):
    print "%-10s ->" % deco(mod) ,
    for d in deps:
        print deco(d) ,
    print ""

def alldeps( mod ):
    """ all deps: just iterate port deps ... breadth-first """
    bfs = [mod]
    done = {}
    while bfs:
        mod = bfs.pop( 0 )
        if mod in done:  continue
        deps = port_deps( mod )
        print_deps( mod, deps )
        done[mod] = 1
        bfs.extend( [d for d in deps if d not in done] )


#...............................................................................
roots = ["pandoc"]
if len(sys.argv) > 1:
    if sys.argv[1].startswith( "-" ):  # -h --help
        print __doc__  # at the top
        exit( 1 )
    roots = sys.argv[1:]

try:
    import bz.util
    print bz.util.From()  # date pwd etc.
    bz.util.scan_eq_args( globals() )  # Macportsinstalled= ...
except:
    pass

port_installed()  # port list installed -> installed[ mod ... ]
for root in roots:
    alldeps( root )
    print ""

# end port-alldeps.py
