import cStringIO;
from zipfile import *

class ZipString(ZipFile):
    def __init__(self, string=None):
        if string==None:
            raise RuntimeError, 'must pass a string to constructor';
        self.fp = cStringIO.StringIO( str(string) );
        self._filePassed = 0;
        self.debug = 0  # Level of printing: 0 through 3
        self.NameToInfo = {}    # Find file info given name
        self.filelist = []      # List of ZipInfo instances for archive
        #self.compression = compression  # Method of compression
        self.mode = key = 'r';
        self.filename = "<string>"
        modeDict = {'r' : 'rb', 'w': 'wb', 'a' : 'r+b'}
        self._GetContents();
