#!/usr/bin/env python
"""
    Visual Source Safe Integration Module.
    
    Notes:
    
        Early stages of this module - GLV, check in and check out only. Some resource management stuff, but not
        iron-tight, so would recommend calling dispose() explicitly on all objects!
    
    Known issues:
    
    *   Doesn't seem to like UNC paths on my two boxes (+ lapdog); would recommend mapping a network drive and pointing to that.
    
"""
__author__  = "Tim Watson"
__version__ = "$Revision: 1.1 $"
__license__ = "Python"

import win32com.client as com;
import pywintypes as win32;

#internal constants
VSS_ROOT_FOLDER         = "$/";
#vs constants
VSSFILE_CHECKEDOUT      =0x1        # from enum VSSFileStatus
VSSFILE_CHECKEDOUT_ME   =0x2        # from enum VSSFileStatus
VSSFILE_NOTCHECKEDOUT   =0x0        # from enum VSSFileStatus
VSSITEM_FILE            =0x1        # from enum VSSItemType
VSSITEM_PROJECT         =0x0        # from enum VSSItemType
VSSFLAG_RECURSNO        =0x1000     # from enum VSSFlags
VSSFLAG_RECURSYES       =0x2000     # from enum VSSFlags

class ObjectDisposedException(Exception): pass
class ComException(Exception, win32.com_error): pass

class Disposable(object):
    def __init__(self):
        super(Disposable, self).__init__();
    
    def __del__(self):
        self.dispose();
    
    def dispose(self): pass
    
    def guard(self):
        if self.disposed == True: raise ObjectDisposedException("Object disposed!");

class Searchable:
    """Only works in conjunction with classes that implement the Node interface."""
    def __init__(self):
        super(Searchable, self).__init__();
        
    def __contains__(self, item):
        return self.contains(item);
    
    def contains(self, item):
        foundItem = None;
        try:
            foundItem = self.__getitem__(item);
            if foundItem:
                return True;
            else:
                return False;
        finally:
            foundItem.dispose();
    
    def __getitem__(self, key):
        item = None;
        if hasattr(self.vssItem, "Items"): 
            try:
                #do a quick search of the current branch
                item = self.vssItem.Items.Item(key);
            except win32.com_error:
                #try a recursive search for the item
                searches = [];
                try:
                    for child in self.descendants():
                        if child.name == key:
                            return Node(child);
                        searches.append(child);
                finally:
                    for n in searches: n.dispose();
        return Node(item);

class Node(Disposable, Searchable):
    def __init__(self, comobject):
        self.vssItem = comobject;
    
    def __call__(self):
        return self.__repr__();

    #are these really needed on subclasses?
    def __del__(self):
        self.dispose();

    def __iter__(self):
        return self.iterkeys();
    
    def __nonzero__(self):
        return self.vssItem is not None;
    
    def __repr__(self):
        return "<Node.%s>" % str(self.name);

    def iterkeys(self):
        """Gets the immediate descendants of the current node."""
        if self.vssItem is not None:
            if not hasattr(self.vssItem, "Items"): return;
            for item in self.vssItem.Items:
                yield Node(item);

    def descendants(self):
        """Iterates over all the descendants of the current node,
            in order, to the leaf level."""
        if self.vssItem is not None:
            for item in self.__gen(self.vssItem):
                yield Node(item);
    
    def __gen(self, root):
        yield root;
        if hasattr(root, "Items"):
            for node in root.Items:
                for item in self.__gen(node):
                    yield item;

    #todo: sort out this hideous duplication!
    def checkout(self, local=None, flags=None):
        if self.vssItem is not None:
            if local is not None:
                if flags is not None:
                    self.vssItem.Checkout(Local=local, iFlags=flags);
                else:
                    self.vssItem.Checkout(Local=local);
            else:
                if flags is not None:
                    self.vssItem.Checkout(iFlags=flags);
                else:
                    self.vssItem.Checkout();
    
    #todo: sort out this hideous duplication!
    def checkin(self, local=None, flags=None):
        if self.vssItem is not None:
            if local is not None:
                if flags is not None:
                    self.vssItem.Checkin(Local=local, iFlags=flags);
                else:
                    self.vssItem.Checkin(Local=local);
            else:
                if flags is not None:
                    self.vssItem.Checkin(iFlags=flags);
                else:
                    self.vssItem.Checkin();
    
    def get(self, local, flags=None):
        if local is None: return;
        if self.vssItem is not None:
            if flags is not None:
                self.vssItem.Get(Local=local, iFlags=flags);
            else:
                self.vssItem.Get(Local=local);
    
    def __process(self, function, local=None, flags=None):
        if function is None: return;
        if local is not None:
                if flags is not None:
                    function(Local=local, iFlags=flags);
                else:
                    function(iFlags=flags);
        else:
            if flags is not None:
                function(iFlags=flags);
            else:
                function();
    
    def __checkedOut(self):
        if not self.__isFile(): return False;
        return self.vssItem.IsCheckedOut == VSSFILE_CHECKEDOUT or self.vssItem.IsCheckedOut == VSSFILE_CHECKEDOUT_ME;
    
    def __checkedOutToMe(self):
        if self.__checkedOut():
            return self.vssItem.IsCheckedOut == VSSFILE_CHECKEDOUT_ME;
    
    def dispose(self):
        self.vssItem = None;

    def __getName(self):
        if self.vssItem is None:
            return "None";
        else:
            return self.vssItem.Name;

    def hasItems(self):
        return not hasattr(self.vssItem, "Items");
    
    def __isProject(self):
        return self.vssItem is not None and self.vssItem.Type == VSSITEM_PROJECT;
    
    def __isFile(self):
        return not self.__isProject();

    def __deleted(self):
        if self.vssItem is not None: 
            return self.vssItem.Deleted;
    
    def __parent(self):
        if self.vssItem is not None:
            try:
                return Node(self.vssItem.Parent);
            except: pass
        return Node(None);
    
    def __path(self):
        if self.vssItem is not None: return self.vssItem.Spec;
        return "None";

    #todo: figure out how to access self from a lambda!

    vsspath = property (fget=__path);

    deleted = property (
            fget=__deleted,
            doc="""Indicates whether or not the current instance has been deleted."""
        )

    name = property (
            fget=__getName,
            doc="""Returns the name of the underlying node object"""
        );
    
    parent = property (
            fget=__parent,
            doc="""Gets the parent for the current item."""
        );
    
    isCheckedOut = property (
            fget=__checkedOut,
            doc="""
                Indicates whether or not a file is checkout out.
                Returns false is the current item is a folder.
                """
        );
    
    isMine = property (
            fget=__checkedOutToMe,
            doc="""
                Indicates whether or not a file is checked out to the currently logged in user.
                """
        );
    
    isLeaf = property (
            fget=hasItems,
            doc="""Indicates whether or not this instance is at the leaf level."""
        );

    isFile = property (
            fget=__isFile,
            doc="""Indicates whether or not this instance represents a file."""
        );
    
    isProject = property (
            fget=__isProject,
            doc="""Indicates whether or not this instance represents a project."""
        );

class Database(Node):
    """ A vss database instance. """
    def __init__(self):
        "Database init";
        self.__vss = com.Dispatch("SourceSafe");
        super(Database, self).__init__(None);
        self.disposed = lambda: self.__vss is None;
        self.isOpen = lambda: self.vssItem is not None;
    
    def __del__(self):
        self.dispose();
    
    def __iter__(self):
        return self.iterkeys();
    
    def iterkeys(self):
        super(Database, self).guard();
        for item in self.__getRoot().Items:
            yield Node(item);

    def open(self, iniFile, username, password=None):
        """
            Opens a new instance of vss database.
        """
        super(Database, self).guard();
        self.__vss.Open(iniFile, username);
        self.vssItem = self.__vss.VSSItem(VSS_ROOT_FOLDER, False);
    
    @staticmethod
    def openProject(iniFile, projectName, username, password=None):
        """
            Opens and returns the project at the specified location in vss.
            If you pass an absolute path (e.g. a path including the vss separator character '/',
            will attempt to load the project from the exact path specified (adding the root namespace
            declaration '$/' if missing). If this attempt fails (or if you simply pass the name of the project,
            such as 'my project'), will create a new database at the root position and recursively search for the
            specified project.            
            
            Returns a new project node, or 'None', if the search fails. The recursive search is quite
            slow, so pass the full path if you can.
        """
        prName = projectName;
        if projectName.find("/") != -1:
            if not projectName.startswith(VSS_ROOT_FOLDER):
                prName = VSS_ROOT_FOLDER + projectName;
            try:
                vss = com.Dispatch("SourceSafe");
                vss.Open(iniFile, username);
                try:
                    p = vss.VSSItem(prName);
                    return Node(p);
                except: pass
            finally:
                vss = None;
            #out of luck - try stripping out the project name and doing a 'normal' search
            if projectName.endswith("/"):
                prName = projectName.rstrip("/");
            lastSepChar = prName.rfind("/");
            if lastSepChar == -1:
                raise Exception("I Can't be bothered parsing this mess :- put in a proper project name you blithering idiot!");
            prName = prName[lastSepChar, len(prName) - lastSepChar];
            if prName.startswith("/"):
                prName = prName.lstrip("/");
                #todo: all of the above with a nice, clean regex instead.
        ##regular search method:
        toplevels = [];
        db = None;
        try:
            try:
                db = Database();
                db.open(iniFile, username, password);
                #minimum depth search first:            
                for topLevelProj in db:
                    if topLevelProj.name == projectName:
                        return Node(topLevelProj);
                    toplevels.append(topLevelProj);
                #now try increasing the search depth exponentially:
                for proj in toplevels:
                    for child in proj.descendants():
                        if child.name == projectName: return Node(child);
                        else: child.dispose();
                #todo: do this (above) with a list comprehension instead!
            finally:
                db.dispose();
        finally:
            for p in toplevels:
                p.dispose();
    
    def dispose(self):
        """Disposes of the current instance."""
        self.__vss = None;
        super(Database, self).dispose();
   
    def hasItems(self):
        return True;
   
    def __getRoot(self):
        super(Database, self).guard();
        return self.vssItem;

class SourceSafe:
    """Simple vss wrapper, to make lifetime management easier."""
    def __init__(self, iniFile, username):
        self.iniFile = iniFile;
        self.username = username;
        self.checked_out = False;
        self.project = None;
        self.releaseFolder = None;
        self.verbose = False;
    
    def checkout(self, projectRoot, checkoutFolder, iflags=None):
        if self.verbose: print "Attempting to check out files...";
        if self.project is None:
            self.project = Database.openProject(str(self.iniFile), projectRoot, str(self.username));
        assert self.project is not None;
        if projectRoot == checkoutFolder:
            self.releaseFolder = self.project;
        else:
            self.releaseFolder = self.project[checkoutFolder];
        assert self.releaseFolder, "Failed to locate vss folder %s!" % checkoutFolder;
        try:
            self.releaseFolder.checkout(flags=iflags);
            self.checked_out = True;
            if self.verbose: print "Check out successful.";
        except:
            print "Check out failed...";

    def checkin(self, iflags=None):
        if self.checked_out:
            if self.verbose: print "Attempting to check in files...";
            try:
                self.releaseFolder.checkin(flags=iflags);
                if self.verbose: print "Check in successful.";
            except:
                print "Check in failed..";
    
    def get(self, project, local=None, iflags=None):
        try:
            if self.project is None:
                if project is None: return;
                self.project = Database.openProject(str(self.iniFile), project, str(self.username));
            if self.verbose: print "Attempting [Get Latest Version]...";
            self.releaseFolder = self.project;
            self.releaseFolder.get(local, iflags);
            if self.verbose: print "[Get Latest Version] complete...";
        except:
            print "[Get Latest Version] failed...";

    def dispose(self):
        if self.project is not None: self.project.dispose();
        self.project = None;
        if self.releaseFolder is not None: self.releaseFolder.dispose();
        self.releaseFolder = None;

###########################################################################

#!/usr/bin/env python
"""
    Unit test module for vss module.
"""
    
__author__  = "Tim Watson"
__version__ = "$Revision: 1.1 $"
__license__ = "Python"

import unittest;
from vss import *;

DATABASE    = "C:\\BUILD_TEST\\srcsafe.ini";
USER        = "scripting.client"
PROJECT     = "ICBFData";
PROJECT_PARTIAL = "BI_Build/" + PROJECT;
PROJECT_FULL    = "$/" + PROJECT_PARTIAL;

class ServerFixture(unittest.TestCase):
    
    def setUp(self):
        self.db = Database();
        self.db.open(DATABASE, USER);
    
    def tearDown(self):
        self.db.dispose();
    
    def testConnect(self):
        "Tests the ability to create a new server instance."
        self.db.dispose();
        self.assert_(self.db.disposed, "not disposed!");
    
    def testGetRootProjectAndIter(self):
        for project in self.db:
            self.failIf(project.name is None, "Project name cannot be None");
    
    def testRecursiveIterProjects(self):
        MAX_COUNT = 100;
        count = 0;
        for proj in self.db:
            for node in proj.descendants():
                if count > MAX_COUNT: return;
                count += 1;
                self.failIf(node.name is None);
                print node.name;
                if node.isLeaf:
                    self.failIf(hasattr(node, "Items"), "Node %s was supposed to be a leaf!" % node.name);
    
    def testContainmentCheckSucceeds(self):
        BAD_ITEM_NAME = "Doesn't Exist!";
        GOOD_ITEM_NAME = "IABuild";
        self.assertFalse(BAD_ITEM_NAME in self.db);
        self.failIf(not GOOD_ITEM_NAME in self.db);
        
    def testGetBadProjectYieldsNone(self):
        BAD_PROJECT = "Not Real";
        self.assertEqual(Database.openProject(DATABASE, BAD_PROJECT, USER), None);
      
    def testPartialProjectOk(self):
        self.doProjectLoad(PROJECT_PARTIAL);
    
    def testFullProjectOk(self):
        self.doProjectLoad(PROJECT_FULL);
    
    def doProjectLoad(self, project):
        proj = Database.openProject(DATABASE, project, USER);
        self.assertFalse(proj is None, "Failed to locate project");
        self.assertEqual(proj.name, PROJECT);

if __name__ == "__main__":
    unittest.main();
