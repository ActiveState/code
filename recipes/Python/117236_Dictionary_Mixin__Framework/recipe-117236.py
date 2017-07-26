class DictMixin:
    '''Mixin defining all dictionary methods for classes that already have
       a minimum dictionary interface including getitem, setitem, delitem,
       and keys '''

    # first level definitions should be implemented by the sub-class
    def __getitem__(self, key):
        raise NotImplementedError
    def __setitem__(self, key, value):
        raise NotImplementedError
    def __delitem__(self, key):
        raise NotImplementedError    
    def keys(self):
        raise NotImplementedError
    
    # second level definitions which assume only getitem and keys
    def has_key(self, key):
         return key in self.keys()
    def __iter__(self):
        for k in self.keys():
            yield k

    # third level uses second level instead of first
    def __contains__(self, key):
        return self.has_key(key)            
    def iteritems(self):
        for k in self:
            yield (k, self[k])

    # fourth level uses second and third levels instead of first
    def iterkeys(self):
        return self.__iter__()
    def itervalues(self):
        for _, v in self.iteritems():
            yield v
    def values(self):
        return list(self.itervalues())
    def items(self):
        return list(self.iteritems())
    def clear(self):
        for key in self.keys():
            del self[key]
    def setdefault(self, key, default):
        if key not in self:
            self[key] = default
            return default
        return self[key]
    def popitem(self):
        key = self.keys()[0]
        value = self[key]
        del self[key]
        return (key, value)
    def update(self, other):
        for key in other.keys():
            self[key] = other[key]
    def get(self, key, default):
        if key in self:
            return self[key]
        return default
    def __repr__(self):
        return repr(dict(self.items()))

def MakeFullDict(tgt):
    'Extends the dictionary interface for existing classes'
    tgt.__bases__ = tuple(list(tgt.__bases__) + [DictMixin])


### Example of extending shelve.py to have a full dictionary interface
import shelve
MakeFullDict(shelve.Shelf)

s = shelve.open('a.shl')
s['name'] = 'john'
s['world'] = 'earth'
print s.has_key('name')
print s.__contains__('name')
print 'name' in s
for k in s: print k
for k,v in s.iteritems(): print k,v
for k in s.iterkeys(): print k
for v in s.itervalues(): print v
print s.values()
print s.setdefault( 'addr', 1 )
print s.setdefault( 'addr', 2 )
del s['addr']
print s.popitem()
s.update( {'age':38} )
print s.keys()
print s.get('age',17)
print s.get('salary', 2000)
print s
print `s`

### Example of a binary tree expanding to a full dictionary iterface
class TreeDict(object, DictMixin):
    __slots__ = [left, right, key, value]
    def __init__(self, key, value):
        self.left, self.right, self.key, self.value = None, None, key, value   
    def __getitem__(self, key):
        if key == self.key: return value
        next = self.left
        if key > self.key: next=self.right
        if next is None:  raise KeyError, key
        return next[key]
    def __setitem__(self, key, value):
        if key == self.key:
            self.value = value
            return
        if key < self.key:
            if self.left is None:
                self.left = TreeDict(key,value)
            else:
                self.left[key]=value
        else:
            if self.right is None:
                self.right = TreeDict(key,value)
            else:
                self.right[key]=value
    def keys(self):
        ans = [self.key]
        if self.left is not None: ans.extend(self.left.keys())
        if self.right is not None:  ans.extend(self.right.keys())
        return ans
    def items(self):
        'DictMixin does this; but it can be done faster by the base class'
        ans = [(self.key, self.value)]
        if self.left is not None: ans.extend(self.left.items())
        if self.right is not None:  ans.extend(self.right.items())
        return ans    
    def iteritems(self):
        'DictMixin does this; but it can be done faster by the base class'
        for item in self.items():
            yield item
