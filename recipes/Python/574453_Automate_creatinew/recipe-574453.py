"""
NewSvnProject creates a new Subversion repository, imports new files to it, then 
checks out those files back to original directory, with a single command or 
drag'n'drop.

Instructions
============
* Save source code as NewSvnProject.py
* Modify globals below for your system. [one-time]
    SVN_EXE
    SVN_ADMIN_EXE
    REPO_DIR
    REPO_URL
* Call from command line:
    Example: C:\Python24\python.exe C:\Dev\PyUtils\src\NewSvnProject.py C:\Dev\C++\A2Work
* Or setup a drag'n'drop shortcut according to your system.

Notes
=====
* Backup your work before trying this.
* Close applications accessing folder or files in project.
* Windows: Don't have project folder open in right Explorer pane.
* Original work files and old repositories are protected from loss by renaming 
  directories with a timestamp.
* Developed and tested under Windows, but does not use Windows calls, so it 
  should work from command lines on Unix and Macs. Let me know.
* Deletes old .svn dirs in project, if present.

Jack Trainor 2008
"""
import os, os.path
import sys
import time

# =====================================================================================
# !!! Modify these globals for your system !!!
SVN_EXE         = r'"C:\Program Files\Subversion\bin\svn.exe"'
SVN_ADMIN_EXE   = r'"C:\Program Files\Subversion\bin\svnadmin.exe"'
REPO_DIR        = r'c:\Data\svn'
REPO_URL        = r'file:///c:/Data/svn'
# =====================================================================================

# =====================================================================================
# File and System Utility calls
# =====================================================================================
def DeleteDir(path):
    try:
        #print "Deleting dir", path
        os.chmod(path, 0666)
        os.rmdir( path )
    except Exception, e:
        print 'DeleteDir failed:', path, e 
          
def DeleteFile(path):
    try:
        #print "Deleting file", path
        os.chmod(path, 0666)
        os.unlink( path )
    except Exception, e:
        print 'DeleteFile failed:', path, e   
        
def RenamePath(path, newPath): 
    try:
        absPath = os.path.abspath(path)
        #print 'Renaming path %s -> %s' % (absPath, newPath)
        os.chmod(absPath, 0666)
        os.rename( absPath, newPath )
    except Exception, e:
        print 'RenamePath failed:', path, newPath, e

def Execute(command):
    os.system(command)


# =====================================================================================
# Support for deleting previous .svn dirs
# =====================================================================================
class Walker(object):
    def __init__(self, dir):
        self.dir = dir

    def execute(self):
        if os.path.exists(self.dir):
            self.executeDir(self.dir)
        else:
            print 'Walker.execute dir doesn''t exist:', self.dir
        return self    

    def walk(self, dir):
        names = os.listdir(dir)
        for name in names:
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                if self.isValidFile(path):
                    self.executeFile(path)
            elif os.path.isdir(path):
                if self.isValidDir(path):
                     self.executeDir(path)
            else:
                print "Invalid path", path
                    
    def isValidDir(self, path):
        return True

    def isValidFile(self, path):
        return True
    
    def executeFile(self, path):
        pass
    
    def executeDir(self, path):
        self.walk(path)

class DirKiller(Walker):
    def __init__(self, dir):
        Walker.__init__(self, dir)
        
    def execute(self):
        Walker.execute(self)
        print "DirKiller complete:", self.dir
        return self
    
    def executeFile(self, path):
        DeleteFile( path)
        
    def executeDir(self, path):
        self.walk(path)
        DeleteDir(path)
        
class SelectiveDirKiller(Walker):
    def __init__(self, dir, killDirs=[]):
        Walker.__init__(self, dir)
        self.killDirs = killDirs
        
    def executeDir(self, path):
        head, tail = os.path.split(path)
        if tail in self.killDirs:
            DirKiller(path).execute()
        else:
            self.walk(path)
        
def TimestampDir(path):
    if os.path.exists(path):
        newPath = path +  '-' + time.strftime('%Y-%m-%d-%H%M%S')
        RenamePath(path, newPath)

def KillSvnDirs(path):
    if os.path.exists(path):
        SelectiveDirKiller(path, ['.svn']).execute()

# =====================================================================================
# Subversion Scripts
# =====================================================================================
def CreateRepository(repoDir):
    """ Creates a Subversion repository """
    try:
        TimestampDir(repoDir) # renames previous repository if it already exists 
        Execute(r'%s create %s --fs-type fsfs' % (SVN_ADMIN_EXE, repoDir))
        print 'Finished -- CreateRepository'
    except Exception, e:
        print 'Failed -- CreateRepository', e
        raise

def ImportProject(projDir, projUrl):
    """ Imports project directory to Subversion repository """
    try:
        KillSvnDirs(projDir) # kills old subversion directories if present
        head, tail = os.path.split(projDir)
        os.chdir(head) 
        command = r'%s import -m auto-import %s %s' % (SVN_EXE, tail, projUrl) #doesn't like dbl-quotes around -m arg
        #command = r'%s import %s %s' % (SVN_EXE, tail, projUrl)
        Execute(command)
        print 'Finished -- ImportProject'
    except Exception, e:
        print 'Failed -- ImportProject', e
        raise

def CheckoutProject(repoUrl, projDir):
    """ Checkout Subversion project to a directory """
    try:
        TimestampDir(projDir) # renames previous project directory if it exists, before installing fresh
        os.mkdir(projDir)
        Execute(r'%s checkout %s  %s' % (SVN_EXE, repoUrl, projDir))
        print 'Finished -- CheckoutProject'
    except Exception, e:
        print 'Failed -- CheckoutProject', e
        raise

def CommitProject(projDir):
    """ Commit changes to Subversion project """
    try:
        Execute(r'%s commit %s  -m ""' % (SVN_EXE, projDir))
        print 'Finished -- CommitProject'
    except Exception, e:
        print 'Failed -- CommitProject', projDir, e
        raise

def NewSvnProject(projDir):
    try:
        head, tail = os.path.split(projDir)
        repoDir = os.path.join(REPO_DIR, tail)
        repoUrl = REPO_URL + '/' + tail
    
        CreateRepository(repoDir)
        ImportProject(projDir, repoUrl)
        CheckoutProject(repoUrl, projDir)
    except Exception, e:
        print 'Failed -- NewSvnProject', e

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
        NewSvnProject(path)
        raw_input("Press a key")
