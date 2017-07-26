""" open pipes, urls ... uniformly with Popen, urlopen ... open

openplus() opens pipes and some other objects that quack like files,
as well as files:
    | pipe ...  -- Popen() a shell
    http:// ftp:// ...  -- urlopen()
    `ls $x`, `geturl web data`  -- shell -> filename or url
    ~/a/b       -- sh ls
    .gz         -- gunzip
    -           -- stdin / stdout
    else        -- the builtin open()

Users can then read e.g.
    "| filter data | sort"
    "| convert ... xx.jpg"
    "`geturl web data`"
like files, just by importing openplus and changing open() -> openplus().

The idea is that if it walks like a file and quacks like a file,
i.e. can open/get/put a data stream, or generates a file name or object,
let it be used anywhere a "real" file can be used.
(However xxopen() may lack some methods of __builtin__.open() .)

Error handling is left up to Popen() ... open()
except for `shell expand`, which writes an error message to errout (sys.stderr)
if the result is not a url or os.path.isfile().

"""
    # wibni: > awindow, < aparamwindow -- pyqt
    # reinventing this wheel ...

import gzip
import os.path
import re
import subprocess  # py 2.4
import sys
import urllib2

__version__ = __date__ = "11dec2008"
__author__ = "Denis Bzowy"

_urlpat = re.compile( "[a-z+]+://" )  # http:// ftp:// ... 20+ in urlparse

#-------------------------------------------------------------------------------
def openplus( filelike, rw='r', errout=sys.stderr ):
    """ open pipes, urls ... uniformly with Popen, urlopen ... open """
    start = filelike[0]
    if start == '|':
        if rw[0] == 'r':
            return subprocess.Popen( filelike[1:], shell=True,
                stdout=subprocess.PIPE) .stdout
            # for line in a pipe: see http://bugs.python.org/issue3907
        else:
            return subprocess.Popen( filelike[1:], shell=True,
                stdin=subprocess.PIPE) .stdin

    elif _urlpat.match( filelike ):
        return urllib2.urlopen( filelike )

    elif start == '~':  # ~/x -> $HOME/x, ~sam/x -> sam's home /x (aka glob)
        ls = sh( "/bin/ls -d " + filelike, errout )  # not all shells
        return open( ls, rw )

    elif start == '`':
            # sh: `ls ${x-default}`, `newest *.py`, `geturl web data`
            # -> filename or url, not | etc.
        shexpand = sh( filelike.strip('`'), errout )
        if _urlpat.match( shexpand ):
            return urllib2.urlopen( filelike )
        if os.path.isfile( shexpand ):
            return open( shexpand, rw )
        if errout:  # logger ?
            print >>errout, "error: openplus( \"%s\" ) = \"%s\" " \
                "is not a file or url" % (filelike, shexpand)
        return None

        # ! eval pyfunc() -> a file-like object with next() etc.
        # elif start == '!':
        #     return eval( filelike[1:] )  # wrong globals(), unsafe, mttiw

    elif filelike.endswith( ".gz" ):
        return gzip.GzipFile( filelike, rw )

    elif filelike == '-':
        return (sys.stdin if rw[0] == 'r'  else sys.stdout)

    else:
        return open( filelike, rw )  # a "real" file


#...............................................................................
def sh( cmd_arg_str, errout=sys.stderr ):
    r""" Popen a shell -> line or "line1 \n line2 ...", trim last \n """
    # crashes after pyqt QApplication() with mac py 2.5.1, pyqt 4.4.2 
    # subprocess.py _communicate select.error: (4, 'Interrupted system call')
    # see http://bugs.python.org/issue1068268 subprocess is not EINTR-safe
    # QProcess instead of Popen works

    (lines, err) = subprocess.Popen( cmd_arg_str,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True ) \
        .communicate()  # wait til process ends
    if errout and err:
        print >>errout, err
    # trim the last \n so sh( "ls xx" ) -> "xx" not "xx\n"
    # and split( "\n" ) -> no extra ""
    return lines[:-1] if (lines and lines[-1] == "\n") \
        else lines

# end openplus.py
