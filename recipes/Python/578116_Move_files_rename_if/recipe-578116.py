#!/usr/bin/env python

#
# Copyright John Reid 2012
#

"""
A python script that renames (moves) files to a destination
directory. However it will not overwrite existing files. The
script uses a renaming strategy where a count is incremented
in order to avoid naming conflicts.

Example usage::

    mv-rename a.ext b.ext target-dir/

would mv a.ext and b.ext into the target directory. If::

    target-dir/a.ext
    target-dir/b.ext

already exist, the newly moved files would be named::

    target-dir/a-<N>.ext
    target-dir/b-<M>.ext

where <N> and <M> are the lowest numbers such that there
is no conflict.
"""



import sys, os

def show_options(exitval):
    "Show the options and exit."
    print 'USAGE: %s files... [destination directory]' % sys.argv[0]
    sys.exit(exitval)

#
# Parse arguments
#
if len(sys.argv) < 3:
    show_options(-1)
dst_dir = sys.argv[-1]
files = sys.argv[1:-1]
if not os.path.isdir(dst_dir):
    print '%s is not a directory.' % dst_dir
    show_options(-2)
for file in files:
    if not os.path.exists(file):
        print '%s does not exist.' % file
        show_options(-3)


#
# Move files
#
for file in files:
    basename = os.path.basename(file)
    head, tail = os.path.splitext(basename)
    dst_file = os.path.join(dst_dir, basename)
    # rename if necessary
    count = 0
    while os.path.exists(dst_file):
        count += 1
        dst_file = os.path.join(dst_dir, '%s-%d%s' % (head, count, tail))
    #print 'Renaming %s to %s' % (file, dst_file)
    print dst_file
    os.rename(file, dst_file)
