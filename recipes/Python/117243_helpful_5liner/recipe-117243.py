#!/usr/bin/env python

def makepath(path):

    """ creates missing directories for the given path and
        returns a normalized absolute version of the path.

    - if the given path already exists in the filesystem
      the filesystem is not modified.

    - otherwise makepath creates directories along the given path
      using the dirname() of the path. You may append
      a '/' to the path if you want it to be a directory path.

    from holger@trillke.net 2002/03/18
    """

    from os import makedirs
    from os.path import normpath,dirname,exists,abspath

    dpath = normpath(dirname(path))
    if not exists(dpath): makedirs(dpath)
    return normpath(abspath(path))

#
#
####### some usages
#
#

if __name__=='__main__':

        # simple use
        abspath = makepath('tmp/log.txt')

        # nice use for making some directories 
        dirs = map (makepath, ('var/log/', 'var/db/', 'tmp/logfile'))

        # nice for just using it like this
        file = open(makepath('/tmp/dir/hallo'), 'w')
        file.write("hello world\n")
        file.close()
