class LocalFTP(object):
    """
    Class adding recursive nlst() behavior to ftplib.FTP instance. The
    ftplib.FTP instance is available through the connection attribute, and
    is exposed through __getattr__.

    The behavior added by this class (recursive directory listing) is most
    appropriate for ftp connections on a local network over a fast connection, 
    or for small directories on remote ftp servers.

    The class relies on an externally defined callable, which can parse the
    lines returned by the ftplib.FTP.dir() method. This callable should be 
    bound to the 'dirparser' attribute on this object. The callable 'dirparser' 
    attribute can be initialized by passing it in to the constructor using the
    keyword argument 'dirparser', or by attaching the callable to the
    'dirparser' attribute after instantiation. 

    The callable should return parsed results as a dict. This class makes some
    assumptions about the contents of the dict returned by the user-defined 
    dirparser callable:

    -- the key 'trycwds' holds a list of booleans 

    -- the key 'names' holds a list of filenames in the dir() listing.
    
    -- The two lists should be the same length. A True value in the list
       referred to by the 'trycwds' key indicates the corresponding value
       in the list referred to by the 'names' key is a directory.

    -- The key names are based on fields in the ftpparse structure, from the   
       ftpparse module/C library.     
   
    -- Other keys can be included in the dict, but they are not used by the 
       rnlst() method.
      
    -- The callable should return an empty dict() if there is nothing to return
       from the dir listing.
       
    This module provides two parsers which seem to work ok, but it should
    be easy to create others if these don't work for some reason:

    -- parse_windows parses the dir listing from Windows ftp servers.
    -- parse_unix parses the dir listing from UNIX ftp servers.
    
    """
    
    def __init__(self, host='', user='', passwd='', acct='', 
                 dirparser=None):
        self.connection = ftplib.FTP(host, user, passwd, acct)
        self.remotepathsep = '/'
        self.dirparser = dirparser
        

    def __getattr__(self, name):
        """
        Delegate most requests to the underlying FTP object. 
        """

        return getattr(self.connection, name)


    def _dir(self,path):
        """
        Call dir() on path, and use callback to accumulate
        returned lines. Return list of lines.
        """

        dirlist = []
        try:
            self.connection.dir(path, dirlist.append)
        except ftplib.error_perm:
            warnings.warn('Access denied for path %s'%path)
        return dirlist


    def parsedir(self, path=''):
        """
        Method to parse the lines returned by the ftplib.FTP.dir(),
        when called on supplied path. Uses callable dirparser
        attribute. 
        """
        
        if self.dirparser is None:
            msg = ('Must set dirparser attribute to a callable '
                   'before calling this method')
            raise TypeError(msg)

        dirlines = self._dir(path)
        dirdict = self.dirparser(dirlines)
        return dirdict
        
        
    def _cleanpath(self, path):
        """
        Clean up path - remove repeated and trailing separators. 
        """
        
        slashes = self.remotepathsep*2
        while slashes in path:
            path = path.replace(slashes,self.remotepathsep)
            
        if path.endswith(self.remotepathsep):
            path = path[:-1]
            
        return path
        
        
    def _rnlst(self, path, filelist):
        """
        Recursively accumulate filelist starting at
        path, on the server accessed through this object's
        ftp connection.
        """
        
        path = self._cleanpath(path)
        dirdict = self.parsedir(path)
        
        trycwds = dirdict.get('trycwds', [])
        names = dirdict.get('names', [])
        
        for trycwd, name in zip(trycwds, names):           
            if trycwd: # name is a directory
                self._rnlst(self.remotepathsep.join([path, name]), filelist)
            else: 
                filelist.append(self.remotepathsep.join([path, name]))
                
        return filelist

                
    def rnlst(self, path=''):
        """
        Recursive nlst(). Return a list of filenames under path.
        """
      
        filelist = []
        return self._rnlst(path,filelist)
        

# Naive ftplib.FTP.dir() parsing functions, which may or may not work. (These
# happen to work for servers I connect to.) Create your own functions (perhaps
# using ftpparse) for more robust solutions.
       
def parse_windows(dirlines):
    """
    Parse the lines returned by ftplib.FTP.dir(), when called
    on a Windows ftp server. May not work for all servers, but it
    works for the ones I need to connect to.
    """

    typemap = {'<DIR>': True}
    
    if not dirlines:
        return dict()
    
    maxlen = max(len(line) for line in dirlines)
    columns = [slice(0, 9), slice(9, 17), slice(17, 29), slice(29, 38), 
               slice(38, maxlen+1)]

    fields = 'dates times trycwds sizes names'.split()

    values = []
    for line in dirlines:
        vals = [line[slc].strip() for slc in columns]
        vals[2] = typemap.get(vals[2], False)
        values.append(vals)
        
    lists = zip(*values)
    
    assert len(lists) == len(fields)

    return dict(zip(fields, lists))


def parse_unix(dirlines,startindex=1):
    """
    Parse the lines returned by ftplib.FTP.dir(), when called
    on a UNIX ftp server. May not work for all servers, but it
    works for the ones I need to connect to.
    """

    dirlines = dirlines[startindex:]
    if not dirlines:
        return dict()
   
    pattern = re.compile('(.)(.*?)\s+(.*?)\s+(.*?)\s+(.*?)\s+'
                         '(.*?)\s+(.*?\s+.*?\s+.*?)\s+(.*)')

    fields = 'trycwds tryretrs inodes users groups sizes dates names'.split()

    getmatches = lambda s:pattern.search(s)
    matches = filter(getmatches, dirlines)

    getfields = lambda s:pattern.findall(s)[0]
    lists = zip(*map(getfields, matches))
    
    # change the '-','d','l' values to booleans, where names referring
    # to directories get True, and others get False.
    lists[0] = ['d' == s for s in lists[0]]
    
    assert len(lists) == len(fields)
    
    return dict(zip(fields, lists))
    
