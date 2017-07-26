#!/usr/bin/env python
"""Execute a python function for a selected set of files.

The purpose of this script is to build a filelist, by:
- recursing over a directory, or
- selecting files having a common filename extension, or
- just accepting the filenames as command line arguments,
and then executing any user defined function over this list of files.

This would be the equivalent of something like:
    $ find -name "*ext" -exec <some python function> {} ';'
using the GNU find(1) command.

An example function (which was my primary motivation to write this script) is
also included. This function applies a set of regex rules to rename the files
in the selected filelist.

Please let me know if you find this script useful or if you find any bugs.

Note: Since this general purpose script meant to be customized for your own
specific requirements, I have not done more error handling than I thought
necessary.
"""
__author__ = "Steven Fernandez <lonetwin@yahoo.com>"

import os, sys
import re
import fileinput
import getopt

Usage="""

    %s [options] FILE [...]
where options can be:
    -h              | --help                    Show this help text.
    -r              | --recurse                 Operate on files recursively.
    -f [<type>|all] | --filetype=[<type>|all]   The extension of the files to
                                                operate on. By default, the 
                                                program operates on all files.
                    
Eg: %s --recurse -f mp3 * /my_songs/*
""" % (sys.argv[0], sys.argv[0])


# The rename function invokes this editor to allow the user to make additional
# modifications to the new filename.
EDITOR = 'vi'

def rename(root, filelist):
    """rename(root, filelist) -> None
    
    Sanitize the filenames given in 'filelist', which are rooted at 'root' by
    using a set of regex rules.
    !!! NOTE: This function calls os.tmpnam() which is insecure.
    """
    if not filelist:
        return
    def apply_rules(filename):
        rulez = [('_+'       , ' '),     # One or more underscores to spaces
                 ('-{2,}'    , '-'),     # Two or more hyphens to single hyphen
                 ('&'        , 'And'),   # An ampersand to 'And'
                 ('(-)(\w*)' ,r' \1 \2')]# Spaces around hyphen seperated words
                         
        for look_for, replacement in rulez:
            filename = re.sub(look_for, replacement, filename)
        # Capitalize first letter of every word
        filename = " ".join([ word.capitalize() for word in filename.split() ])
        return filename
    
    names = []
    for filename in filelist:
        basename = os.path.basename(filename)
        names.append(os.path.join(root, apply_rules(filename)))
    try:
        dest = os.tmpnam()
        fl = open(dest, 'w')
        fl.write("\n".join(names))
        fl.close()
        os.system("%s %s" % (EDITOR, dest))
        ans = 'no'
        for oldname, newname in zip(filelist, open(dest).readlines()):
            oldname = os.path.join(root, oldname)
            newname = newname.strip()
            if oldname == newname:
                print "No change from %s to %s ...skipping" % (oldname, newname)
            else:
                print "Changing %s to %s" % (oldname, newname)
                if not ans[0].lower == 'a':
                    ans = raw_input("Contine (Yes/No/All) ? [N] ") or 'no'
                    if ans[0].lower() in ('a', 'y'):
                        os.rename(oldname, newname)
                else:
                    os.rename(oldname, newname)
    finally:
        os.remove(dest)

def main(root, filelist):
    """main(root, filelist) -> None
    
    Override this function, to do whatever you please with the list of files
    passed in filelist. The default behaviour is to call the function rename(),
    which applies a set of rules to sanitize a filename.
    """
    #print "got %s: %s" % (root, filelist)
    rename(root, filelist)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print Usage
        sys.exit(0)

    recurse  = True
    filetype = "all"
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "f:r", \
                                        ['filetype=', 'recurse'])
    except getopt.GetoptError, msg:
        print msg
        print Usage
        sys.exit(1)
    for o, a in opts:
        if o in ('-h', '--help'):
            print Usage
            sys.exit(0)
        elif o in ('-f', "--filetype"):
            filetype = a
        elif o in ('-r', "--recurse"):
            recurse = True
    filelist = []
    for fl in args:
        if os.path.isfile(fl):
            filelist.append(fl)
        if os.path.isdir(fl) and recurse == True:
            for root, dirs, files in os.walk(fl):
                if filetype != 'all':
                    files = [ f for f in files if f.endswith(filetype) ]
                main(root, files)

    if filetype != 'all':
        filelist = [ f for f in filelist if f.endswith(filetype) ]
    main(os.getcwd(), filelist)
