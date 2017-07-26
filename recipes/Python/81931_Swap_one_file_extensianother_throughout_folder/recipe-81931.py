# documentation is at http://www.outwardlynormal.com/python/swapextensions.htm
# send in 3 strings: directory path,  "before" extension, "after" extension

import os

def swapextensions(dir, before, after):
    if before[:1]!='.': before = '.'+before
    if after[:1]!='.': after = '.'+after
    os.path.walk(dir, callback, (before, -len(before), after))

def callback((before, thelen, after), dir, files):
    for oldname in files:
        if oldname[thelen:]==before:
            oldfile = os.path.join(dir, oldname)
            newfile = oldfile[:thelen] + after
            os.rename(oldfile, newfile)

if __name__=='__main__':
    import sys
    if len(sys.argv) != 4:
        print "Usage: swapext rootdir before after"
        sys.exit(100)
    swapextensions(sys.argv[1], sys.argv[2], sys.argv[3])
