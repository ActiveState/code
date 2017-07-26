#!Python27.exe
#-*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# WHICH.PY
# 
# WHICH.PY scans through all directories specified in the system %PATH%
# environment variable, looking for the specified COMMAND(s). It tries
# to follow the sometimes bizarre rules for Windows command lookup.

# Copyright (c) 2013 by Robert L. Pyron <rpyron+which@gmail.com>
# Distributed under terms of the MIT License: http://opensource.org/licenses/MIT
# 
# TODO:
#   -   Figure out how to automatically update version info (probably related
#       to version control)
#   -   Add option for long listing format: date, time, attributes 
#       (system or hidden), SYMLINK info if appropriate, and file size
#   -   Build executable version.
# 
# HISTORY:
#   Version 0.1
#       -   This is the first version that I am willing to make publically
#           available. 
#       -   Submitted to ActiveState Recipes, 15 August 2013.
# 
#-------------------------------------------------------------------------------

"""Write the full path of COMMAND(s) to standard output.

Usage: %(PROG)s [-e] [-f] [-v] [-h] COMMAND [...]

  -e, --exact   Print exact matches only.
  -f, --first   Print just the first match.
  -v, --version Print version and exit successfully.
  -h, --help    Print help message and exit successfully.

%(PROG)s scans through all directories specified in the system %%PATH%%
environment variable, looking for the specified COMMAND(s). It tries
to follow the sometimes bizarre rules for Windows command lookup.

Copyright (c) 2013 by Robert L. Pyron <rpyron@alum.mit.edu>

"""

#-------------------------------------------------------------------------------

import sys, os, os.path, argparse, traceback

#
# I'm on Windows, so I can arbitrarily force the script name to upper case.
PROG = os.path.basename(sys.argv[0]).upper()

#
# Expand module docstring to get USAGE string
USAGE = __doc__ % {'PROG' : PROG}

#
# Get PATH environment variable, and split it.
PATH = os.environ.get('PATH').split(';')
if True:
    # Clean up the PATH info: A directory may appear in PATH more than 
    # once, but there is no need to scan it twice. Also, since this program 
    # is intended to run on Windows, we will always start in the current 
    # directory. I'm ignoring changes in pathname case, because I'm lazy 
    # and it probably doesn't matter very much.
    tmpDirs = ['.']
    for dir in PATH:
        if dir not in tmpDirs:
                tmpDirs += [dir]
    PATH,tmpDirs = tmpDirs,None

#
# Get PATHEXT environment variable, and split it.
# I'm on Windows, so I can arbitrarily force the extensions to lower case.
PATHEXT = os.environ.get('PATHEXT').lower().split(';')

#
# TODO - fix this
VERSION = '$Id$'
VERSION = '0.1'

#
# These commands are built-in to CMD.EXE under Windows 8.
# Earlier and later versions of Windows may have more (or fewer) built-ins.
# Also, other command-line shells may have a different list.
BUILTINS = ["ASSOC", "BREAK", "BCDEDIT", "CALL", "CD", "CHDIR", "CLS", "COLOR",
			"COPY", "DATE", "DEL", "DIR", "ECHO", "ENDLOCAL", "ERASE", "EXIT", 
			"FOR", "FTYPE", "GOTO", "GRAFTABL", "IF", "MD", "MKDIR", "MKLINK", 
			"MOVE", "PATH", "PAUSE", "POPD", "PROMPT", "PUSHD", "RD", "REM", 
			"REN", "RENAME", "RMDIR", "SET", "SETLOCAL", "SHIFT", "START", 
			"TIME", "TITLE", "TYPE", "VER", "VERIFY", "VOL" ]

#
# Global command-line arguments, to be filled in by parse_args()
args = argparse.Namespace()

#-------------------------------------------------------------------------------

#
# Utility function: split a filename into path,root,extension.
def split_name(filename):
    dirname,basename = os.path.split(filename)
    root,ext = os.path.splitext(basename)
    return dirname,root,ext

#
# Find matches to specified filename in system %PATH%.
def which(COMMAND):
    # Define a convenience exception for early exit from this routine.
    # This is used as a Pythonic equivalent to GOTO.
    class FoundFirstMatch(Exception): 
        pass
    
    try:
        print( COMMAND )
    
        # Check whether this is a built-in command.
        if COMMAND.upper() in BUILTINS:
            print( '    (builtin under CMD.EXE)' )
            # The obvious thing to do at this point would be to return, 
            # because we now know everything we need to know, right? 
            # Think again, buddy. This is Windows we are dealing with.
            if args.firstMatchOnly:
                raise FoundFirstMatch()

        # Split COMMAND into parts.
        specified_directory,specified_command,specified_ext = split_name(COMMAND)

        # In general, we don't want to have a pathname specified as part of
        # the COMMAND. However, I allow the syntax '.\COMMAND' to restrict
        # search to current directory.
        local_currentDirectoryOnly = False
        if specified_directory == '.':
            # Search only in current directory.
            local_currentDirectoryOnly = True
            # Reconstruct COMMAND without path.
            COMMAND = specified_command + specified_ext
        elif specified_directory:
            # Do not include path as part of input name.
            # If you know where it is, why are you calling this program?
            print( '    (please do not specify a path as part of COMMAND)' )
            return

        # I also allow a shortcut to specify exactMatchOnly by appending a dot.
        # For example, "foo.exe." looks for "foo.exe" and nothing else.
        local_exactMatchOnly = args.exactMatchOnly
        if specified_ext == '.':
            local_exactMatchOnly = True
            # Reconstruct COMMAND without extension.
            COMMAND, specified_ext = specified_command, ''

        # Scan through all directories in %PATH%.
        count = 0
        for dir in PATH:
            # Expand environment variables in PATH component
            dir = os.path.expandvars(dir)
            # First, look for an exact match in this directory.
            if specified_ext or local_exactMatchOnly:
                target = os.path.join(dir,COMMAND)
                if os.path.isfile(target):
                    print( '    ' + target )
                    count += 1
                    if args.firstMatchOnly:
                        raise FoundFirstMatch()
                    else:
                        # Move along to next directory in PATH.
                        continue
            # Now, try all extensions listed in PATHEXT.
            if not local_exactMatchOnly:
                for ext in PATHEXT:
                    target = os.path.join(dir,specified_command+ext)
                    if os.path.isfile(target):
                        print( '    ' + target )
                        count += 1
                        if args.firstMatchOnly:
                            raise FoundFirstMatch()
                        else:
                            # Move along to next extension in PATHEXT.
                            continue
        if count == 0:
            print( '    (not found)' )
    
    except FoundFirstMatch:
        pass
    finally:
        print

    return

#-------------------------------------------------------------------------------

#
# Parse command-line arguments
def parse_args():
    """Parse command-line arguments; fill in global variable 'args'."""
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--exact',   help='Print exact matches only.',            action='store_true', dest='exactMatchOnly' )
    parser.add_argument('-f', '--first',   help='Print just the first match.',          action='store_true', dest='firstMatchOnly' )
    parser.add_argument('-v', '--version', help='Print version and exit successfully.', action='version', version=VERSION)
    parser.add_argument('COMMANDS', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    return args

#
# Command-line arguments have already been parsed.
def main (args):
    if not args.COMMANDS:
        print USAGE
        return
    for COMMAND in args.COMMANDS:
        which(COMMAND)

if __name__ == '__main__':
    try:
        args = parse_args()
        main(args)
        sys.exit(0)
    except KeyboardInterrupt, e:    # Ctrl-C
        raise e
    except SystemExit, e:           # sys.exit()
        raise e
    except Exception, e:
        print( 'ERROR, UNEXPECTED EXCEPTION' )
        print( str(e) )
        traceback.print_exc()
        os._exit(1)
