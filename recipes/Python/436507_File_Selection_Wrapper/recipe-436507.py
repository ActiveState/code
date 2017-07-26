class Action:
    """
    Actions are things that can be executed.
    """
        
    def execute(self):
        pass

class PatternSet:
    """
    Pattern set provides the interface and abstract functionality to provide the include and exclude
    semantics for any classes that want to filter their results based on include and exclude criteria
    """

    def __init__(self):
        self.includeList = []
        self.excludeList = []
        
    def include(self, pattern):
        """
        Patterns should only defined on a single target to match so that we can use the fast fail
        functionality when matching. If you need multiple patterns, call .include() multiple
        times with each expression
        """
        self.includeList.append(re.compile(pattern))
    
    def __isIncluded(self, name):
        result = False
        if len(self.includeList) > 0:
            for pattern in self.includeList:
                if pattern.match(name) != None:
                    result = True
                    break
        return result 

    def exclude(self, pattern):
        """
        Patterns should only defined on single target to match so that we can use the fast fail
        functionality when matching. If you need multiple patterns, call .include() multiple
        times with each expression
        """
        self.excludeList.append(re.compile(pattern))
    
    def __isNotExcluded(self,name):
        result = True
        if len(self.excludeList) > 0:
            for pattern in self.excludeList:
                if pattern.match(name) != None:
                    result = False
                    break
        return result

class FileSet(PatternSet, Action):
    """
    This class allows the user to define a set of files to work on using simple include/exclude semantics
    coupled with the full power of regular expressions
    """    
    def __init__(self, rootDir):
        PatternSet.__init__(self)
        self.rootDir = rootDir

    def execute(self):
        """
        This implementation walks the filesystem from the rootDir and creates a list of
        fully qualified files and returns them.
        """
        results = []
        # walk the dirs from the rootDir and build the results
        for root, dirs, files in os.walk(self.rootDir):
            # if the name is not on the include list or is on the exclude
            # list remove it from the results
            for name in files:
                fqname = join(root,name)
                if self._PatternSet__isIncluded(fqname) and self._PatternSet__isNotExcluded(fqname):
                    results.append(fqname)
        return results
