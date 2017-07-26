"""
Walker encapsulates os.walk's directory traversal as an object with 
the added features of excluded directories and a hook for calling 
an outside function to act on each file.  Walker can easily be 
subclassed for more functionality.

ReWalker filters filenames in traversal by a regular expression.

Jack Trainor 2007
"""
import os, os.path
import re

class Walker(object):
    def __init__(self, dir, executeHook=None, excludeDirs=[]):
        self.dir = dir
        self.executeHook = executeHook
        self.excludeDirs = excludeDirs
        
    def isValidFile(self, fileName):
        return True
        
    def isValidDir(self, dir):
        head, tail = os.path.split(dir)
        valid = (not tail in self.excludeDirs)
        return valid
                  
    def executeFile(self, path):
        if self.executeHook:
            self.executeHook(self, path)
        # else subclass Walker and override executeFile
            
    def execute(self):
        for root, dirs, fileNames in os.walk(self.dir):
            for fileName in fileNames:
                if self.isValidDir(root) and self.isValidFile(fileName):
                    path = os.path.join(root, fileName)
                    self.executeFile(path)
        return self 
    
class ReWalker(Walker):
    def __init__(self, dir, fileMatchRe, executeHook=None, excludeDirs=[]):
        Walker.__init__(self, dir, executeHook, excludeDirs)
        self.fileMatchPat = re.compile(fileMatchRe)

    def isValidFile(self, fileName):
        return self.fileMatchPat.match(fileName)

#######################################################
""" For testing: """
def RenameFile(path, matchRe, subRe):
    dir, name = os.path.split(path)
    newName = re.sub(matchRe, subRe, name)
    if newName != name:
        print "%s -> %s" % (name, newName)
        newPath = os.path.join(dir, newName)
        os.rename(path, newPath)

def Rename1(walker, path):
    RenameFile(path, r"(.*)\.pyc$", r"#\1.pyc#")

def Rename2(walker, path):
    RenameFile(path, r"#(.*)\.pyc#$", r"\1.pyc")

def Test():
    """ renames pyc files to #.*pyc# then restores them back again """
    walker = ReWalker(r"C:\Dev\Copy of PyUtils", r".*\.pyc$", Rename1, [".svn"]).execute()
    walker = ReWalker(r"C:\Dev\Copy of PyUtils", r".*\.pyc#$", Rename2, [".svn"]).execute()


if __name__ == "__main__":
    Test()
    
