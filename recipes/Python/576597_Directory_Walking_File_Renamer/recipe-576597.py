#
#   Dir Walking File Renamer
#   by Mickey Hadick
#   Created: December 27, 2008
#   Copyright (C) 2008 Mickey Hadick
#   Free to copy, correct, and use at your discretion.
#   Inspired by several recipes, especially:
#   http://code.activestate.com/recipes/105873/
#
#   This module reads a file that contains a list of directory names.
#   It visits each directory in that file, and renames the files found
#   in those directories.
#   The base path is the path where the file was found.
#   The files are renamed based the directory name, with some unique
#   identifier added onto the end of that name.
#
#   I use this for the photos I download from my camera. I rename the
#   directory to reflect the subject (creating new directories if
#   necessary--like when I take multiple photos on a particular day)
#   and then let all the photos take that name.  The date of the photo
#   is part of the directory name (a setting from the camera software)
#   and then I upload everything to Fotki (in general, not in this
#   module) and all the photos have the date and the subject in their
#   file name.
#

import os, sys, optparse

class NoFile(Exception):
    def __init__(self,msg):
        self.msg = msg


def renameFilesInDir( dir_name ):
    """
    given a directory
    rename all the files therein with the pattern:
    dir_name_nnnn
    where nnnn is a unique number (just count up from 1)
    NOTE: the file extension is preserved!
    NOTE: it does not recurse through sub directories!!
    """
    i = 1   # index used to create unique name in directory

    print 'dir_name is: ', dir_name

    for f in os.listdir( dir_name):

        print 'file: ', f, '--',
        
        if os.path.isdir(f):
            print 'skipping'
            continue

        # if, for example, dir_name is: "d:\pictures\2008\2008_11_01_family"
        # f, at this point, is d:\pictures\2008\2008_11_01_family\img0001.jpg
        # dir_basename needs to be 2008_11_01_family
        # then we rename f to be 2008_11_01_family_0001.jpg (in that same dir)

        froot, ext = os.path.splitext(f)        #get the extension
        # (froot is d:\pictures\2008\2008_11_01_family\img0001)
        # (ext is jpg)

        if ext.lower() != '.jpg':
            print 'skipping'
            continue                # we only work on JPEGs

        dir_root, fname = os.path.split(froot)  #get the dir and base names
        # (dir_root is d:\pictures\2008\2008_11_01_family)
        # (fname is img0001)

        dir_basename = os.path.basename( dir_name)
        # (dir_basename is 2008_11_01_family) <= that's the one I really want!

        new_base = dir_basename + str.format('{i:04}',i=i) + ext
        new_name = os.path.join(dir_name, new_base)
        # uses the new string formatting, to generate the "0001" numbering

        file_to_rename = os.path.join(dir_name, f)

        print 'Renaming %s to %s.' % (f,new_base)
        os.rename(file_to_rename, new_name)
        
        i += 1      # 1 becomes 2, etc.

        # that should do it.


def myMain( file_of_dirs ):
    """
    reads the file (name passed)
    visits each dir
    renames the files therein
    """
    try:
        #test whether the file passed exists, and the path is good
        if not os.path.exists( file_of_dirs ):
            raise NoFile("File does not exist")
        dname, fod_name = os.path.split (file_of_dirs )

        with open( file_of_dirs, 'r') as f:
            for fname in f:
                fname = fname.rstrip('\n')
                dir_to_walk = os.path.join(dname, fname)
                if not os.path.exists( dir_to_walk ):
                    print "Directory %s does not exist--can't process" % dir_to_walk
                else:
                    renameFilesInDir( dir_to_walk )
    except NoFile, err:
        print err.msg
    except:
       exc_info = sys.exc_info()
       print "unhandled exception in DirWalkRenameFile: %s %s %s" % (exc_info[0],exc_info[1],exc_info[2])

if __name__ == '__main__':

    parser=optparse.OptionParser()
    parser.add_option('-f','--filename',dest='input_filename',
                type="string",
                default="d:/pictures/2008test/nov_files.txt",
                help="Filename of file with directories to rename.")
    (options, args) = parser.parse_args()
    
    myMain( options.input_filename )
    
