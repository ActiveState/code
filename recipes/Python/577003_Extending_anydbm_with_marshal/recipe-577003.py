import anydbm
import marshal

class marshaldbm(object):
    """
    Incorporating marshalling capabilities into anydbm module to store
    marshallable objects as values. The keys and values in anydbm must be
    strings. Marshalling capability is added for the values.
    
    >>> d = open('test.db', 'c')
    >>> d['a list'] = ['a', 'b']
    >>> d.close()
    """
    def __init__(self, dbfile, flag):
        """
        Constructor method - opens database file or creates new database file.
        @param dbfile: path of database file
        @param flag: file opening mode for anydbm
        """
        self.dbfile = anydbm.open(dbfile, flag)

    def __setitem__(self, key, item):
        """
        Method to put items into the database file.
        """
        item = marshal.dumps(item)
        self.dbfile[key] = item

    def __getitem__(self, key):
        """
        Method to get items from the databasde file using its key
        """
        return marshal.loads(self.dbfile[key])

    def __len__(self):
        """
        Returns the row count of the database file
        """
        return len(self.dbfile)

    def close(self):
        """
        Closes the database file
        """
        self.dbfile.close()

    def keys(self):
        """
        Returns a list of keys in the database file
        """
        return [key for key in self.dbfile.keys()]
