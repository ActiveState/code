#!/usr/bin/python2.4
import types

class Table(object):
    """A structure which implements a list of dict's."""
    def __init__(self, *args):
        self.columns = args
        self.rows = []
        
    def _createRow(self, k,v):
        return dict(zip(k, v))
    
    def append(self, row):
        if type(row) == types.DictType:
            row = [row[x] for x in self.columns]
        row = tuple(row)
        if len(row) != len(self.columns):
            raise TypeError, 'Row must contain %d elements.' % len(self.columns)
        self.rows.append(row)
    
    def __iter__(self):
        for row in self.rows:
            yield self._createRow(self.columns, row)
    
    def __getitem__(self, i):
        return self._createRow(self.columns, self.rows[i])
    
    def __setitem__(self, i, row):
        if type(row) == types.DictType:
            row = [row[x] for x in self.columns]
        row = tuple(row)
        if len(row) != len(self.columns):
            raise TypeError, 'Row must contain %d elements.' % len(self.columns)
        self.rows[i] = row
    
    def __repr__(self):
        return ("<" + self.__class__.__name__ + " object at 0x" + str(id(self))
                + " " + str(self.columns) + ", %d rows.>" % len(self.rows))




if __name__ == "__main__":
    import pickle
    t = Table("a","b","c")
    for i in xrange(10000):
        t.append((1,2,3))
    print "Table size when pickled:",len(pickle.dumps(t))
    
    t = []
    for i in xrange(10000):
        t.append({"a":1,"b":2,"c":3})
    print "List size when pickled: ",len(pickle.dumps(t))
    

    
  
