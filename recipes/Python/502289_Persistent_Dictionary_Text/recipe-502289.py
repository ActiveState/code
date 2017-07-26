"""
A persistent dict object that uses a text file for storage.

Saved values will update arguments passed to constructor with:
PersistentTextDict(<path>, dict={'a':10}, foo='baz', bla=10)
This behavior allows setting defaults that can be overridden
in a text file on disk.

NOTE: str, int, float, list, dict et. el. support only.
"""
import UserDict

class PersistentTextDict(UserDict.UserDict):
    """
    >>> d = PersistentTextDict('test.dict')
    >>> d['username'] = 'jsmith'
    >>> del d
    >>> d1 = PersistentTextDict('test.dict')
    >>> d1['username']
    'jsmith'
    >>> d1['a'] = 10000
    >>> d1['a']
    10000
    >>> d2 = PersistentTextDict('test.dict')
    >>> d2['a']
    10000
    >>> del d2['a']
    >>> del d2
    >>> d3 = PersistentTextDict('test.dict')
    >>> d3.has_key('a')
    False
    >>> d3.update({'a':9999})
    >>> d3['a']
    9999
    """
    def __init__(self, path, dict=None, **kwargs):
        UserDict.UserDict.__init__(self)
        self.path = path
        try:
            self.isLoad = True
            if dict is not None:
                self.update(dict)
            if len(kwargs):
                self.update(kwargs)
            self.update(eval(open(path, 'r').read()))
            self.isLoad = False
        except IOError:
            self.isLoad = False

    def sync(self):
        import pprint
        open(self.path, 'w').write(pprint.pformat(self.data) + '\n')

    def __setitem__(self, key, item):
        self.data[key] = item
        self.sync()

    def __delitem__(self, key):
        del self.data[key]
        self.sync()

    def update(self, dict=None, **kwargs):
        UserDict.UserDict.update(self, dict=dict, **kwargs)
        if not self.isLoad:
            self.sync()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
