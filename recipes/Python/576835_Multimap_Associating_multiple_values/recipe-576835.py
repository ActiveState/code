"""  
The multimap data structure associates multiple values to a key. 

In this module the multimap is implemented by a dictionary in which each key is  
associated to a container, which can be a list, a dictionary, or a set. 

These containers are created, accessed, and extended using the usual array 
notation, e.g. m["a"] = 1, m["a"] = 2 creates a container for key "a" 
containing 1 and 2. An item within a container can be removed using the 
"remove"  method.

Requires Python 2.5.  
"""

import collections
import sets

class Map(object):
    """ Map wraps a dictionary. It is essentially an abstract class from which
    specific multimaps are subclassed. """
    def __init__(self):
        self._dict = {}
        
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._dict))
    
    __str__ = __repr__
        
    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, value):
        self._dict[key] = value
    
    def __delitem__(self, key):
        del self._dict[key]
        
    def remove(self, key, value):
        del self._dict[key]
    
    def dict(self):
        """ Allows access to internal dictionary, if necessary. Caution: multimaps 
        will break if keys are not associated with proper container."""
        return self._dict

class ListMultimap(Map):
    """ ListMultimap is based on lists and allows multiple instances of same value. """
    def __init__(self):
        self._dict = collections.defaultdict(list)
        
    def __setitem__(self, key, value):
        self._dict[key].append(value)
    
    def remove(self, key, value):
        self._dict[key].remove(value)

class SetMultimap(Map):
    """ SetMultimap is based on sets and prevents multiple instances of same value. """
    def __init__(self):
        self._dict = collections.defaultdict(sets.Set)
        
    def __setitem__(self, key, value):
        self._dict[key].add(value)
    
    def remove(self, key, value):
        self._dict[key].remove(value)

class DictMultimap(Map):
    """ DictMultimap is based on dicts and allows fast tests for membership. """
    def __init__(self):
        self._dict = collections.defaultdict(dict)
        
    def __setitem__(self, key, value):
        self._dict[key][value] = True
    
    def remove(self, key, value):
        del self._dict[key][value]

def test():
    def test_multimap(m):
        print "__________________________________"
        print m["a"]
        m["a"] = 1
        m["a"] = 2
        m["a"] = 2
        m["a"] = 3
        m["a"] = 4
        print m
        m.remove("a", 4)
        print m
        print ("a" in m.dict())
        print m["a"]
        m["a"] = 5
        m["b"] = 6
        print m
        del m["b"]
        print m
        print (3 in m["a"])
        
    test_multimap(ListMultimap())
    test_multimap(SetMultimap())
    test_multimap(DictMultimap())

if __name__ == "__main__":
    test()
