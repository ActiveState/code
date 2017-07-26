#!/usr/bin/env python
#
# Looks through the given Favorites folder and
# prints out an HTML page with their links.
#
# (copyleft) Jose M Beas, 2003
#

import string, sys, os, ConfigParser

def processURL(filename):
    name = os.path.split(filename)[1]
    name = os.path.splitext(name)[0]
    config = ConfigParser.ConfigParser()
    config.read([filename])
    try:
        url = config.get("InternetShortcut","URL")
        print "<A HREF=\"%s\">%s<A/><BR/>" % (url,name)
    except ConfigParser.NoSectionError:
        print >>sys.stderr, "Could not found URL in %s" % (filename)
      
def processFile(filename):
    # Checks if it is a URL and process it (if so)
    if os.path.splitext(filename)[1] == ".url" :
        processURL(filename)
    
def processDir(dirname,level):
    try:
        filenames = os.listdir(dirname)
    except OSError, err:
        print >>sys.stderr, err
        return
    section = os.path.split(dirname)[1]
    files = []
    folders = []
    for filename in filenames:
        fullname = os.path.join(dirname, filename)
        if os.path.isdir(fullname):
            folders.append(fullname)
        else:
            files.append(fullname)
    print "<H%d>%s</H%d>" % (level,section,level)
    for i in files:
        processFile(i)
    for i in folders:
        print "<UL>"
        processDir(i,level+1)
        print "</UL>"
    
def main(argv):
    import getopt    
    try:
        args, dirname = getopt.getopt(argv[1], "h", ["help"])
    except getopt.error:
        args = "dummy"
    if args:
        print "Usage: %s <directory>" % (argv[0],)
        sys.exit(0)

    if not dirname:
        dirname = ["."]
    print "<HTML>"
    processDir(dirname,1)
    print "</HTML>"

if __name__ == "__main__":
    main(sys.argv)
