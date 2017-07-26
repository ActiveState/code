## Title: movefiles.py
## Author: Shawn Kirsch (www.shawnkirsch.com)
## Description: Recoursively delete all sub directorys while preserving
##              files to the root directory.
## Version: 1.1
## Date: Sept, 28th 2010

import os, shutil

rootdir = os.getcwd()
scriptname = 'movefiles.py'
numofdirs = 0
numofiles = 0

def printcount():
    print '-' * 40
    print "Number of Directories: " + str(numofdirs)
    print "Number of Files: " + str(numofiles)
    print '-' * 40

def exploretree():
    global numofdirs, numofiles

    for x in os.listdir(os.getcwd()):
        if os.path.isdir(x):
            ##print 'Dir : ' + x
            numofdirs += 1
            os.chdir(x)
            exploretree()
            os.chdir('..')
        else:
            ##print 'File: ' + x
            if(x != scriptname):
                numofiles += 1

def movefiles():
    print '.',##just lets the user know it hasn't crashed for large batches
    for x in os.listdir(os.getcwd()):
        if os.path.isdir(x):
            os.chdir(x)
            movefiles()
            os.chdir('..')
        if os.path.isfile(x) and os.getcwd() != rootdir:
            shutil.move(x, '..')

def deletedirs():
    global numofdirs

    for x in os.listdir(os.getcwd()):
        if os.path.isdir(x):
            os.chdir(x)
            deletedirs()
            os.chdir('..')
        try:
            os.rmdir(x)
            #print 'Removed Directory: ' + x
            numofdirs -= 1
        except:
            pass
            #print "Couldn't Delete Directory: " + x


exploretree()
printcount()

while(numofdirs!=0):
    movefiles()
    deletedirs()
    

print '\nFinished: All Files moved to the root folder.'
