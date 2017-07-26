#!/usr/local/bin/python

"""
Make this scriptfile executible
by issuing

     chmod +x assoc.py

and include the path to assoc.py to the PATH environment string.
To use, type

     assoc.py  flag  filename  extra_args

where flag may be absent (default would then be -v)  or takes on the
following suggested values in the table.

flag    action
-----------------------
        view
  -v    view
  -e    edit
  -c    compile
  -r    run or execute
  -p    print
-----------------------

Example: 
   assoc.py  -e test.c
should fire-up emacs.
   assoc.py  -D
will dump the dictionary.

The optional  extra_args  allows you to add additional settings to the
command associated with the file extension. More complicated
actions may require Python functions instead of simple strings as dictionary
values.
"""

import os

# Up to two dots in extension  are allowed.
# Modify the dictionary to your needs.
Dassoc = {
    ('.doc', '-e'): 'soffice %s ',
    ('.jpg', '-v'): 'display %s ',
    ('.tex', '-e'): 'kile %s ',
    ('.pdf', '-v'): 'acroread %s ',
    ('.c',   '-e'): 'emacs %s ',
    ('.c',   '-c'): 'gcc -Wall -c %s ',
    ('.c',   '-v'): 'emacs %s ',
    ('.py',  '-r'): 'python %s ',
    ('.py',  '-e'): 'emacs %s ',
    ('.py',  '-v'): 'emacs %s ',
    ('.ps.gz', '-v'): 'gv %s '
    }


if __name__ == "__main__":
    argv     = os.sys.argv
    argc     = len(argv)
    flag     = ""
    filename = ""
    args     = ""

    isOk = True
    if (argc > 1):
        if argv[1][0] == '-':
            flag     = argv[1]
            if argc > 2:
                filename = argv[2]
                for i in range(3, argc):
                    args += ' ' + argv[i]
            else:
                if flag == "-D":  # Dump dictionary.
                    print "Dictionary contents:"
                    for key in Dassoc:
                        print key, Dassoc[key]
                # No filename ?
                isOk = False
        else:
            flag  = "-v"  # default viewer.
            filename = argv[1]
            for i in range(2, argc):
                args += ' ' + argv[i]
    else:
        # no arguments ?
        isOk = False

    if isOk:
        done = False
        extension = ""
        for i in range(2, 0, -1):
            fparts = filename.rsplit(".", i)
            if len(fparts) == 3:
                extension = "." + fparts[1] + "." + fparts[2]
            elif len(fparts) == 2:
                extension = "." + fparts[1]
            key = (extension, flag)
            if Dassoc.has_key(key):
                cmdstr = (Dassoc[key] % filename) + args
                os.system(cmdstr)
                done = True
                break
        if not done:
            print "error in assoc.py, no ", key, "found."
