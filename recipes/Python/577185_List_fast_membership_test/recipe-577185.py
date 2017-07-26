## {{{ http://code.activestate.com/recipes/577185/ (r2)
class MembershipTestList(list):
    def __init__(self, *args, **kwargs):
        super(MembershipTestList, self).__init__(*args, **kwargs)
        self._members = set(*args, **kwargs)

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))
    def __setslice__(self, i, j, seq):
        return self.__setitem__(slice(i, j), seq)
    def __delslice__(self, i, j):
        return self.__delitem__(slice(i, j))
    
    def __getitem__(self, k):
        if isinstance(k, slice):
            indices = k.indices(len(self))
            return [self.__getitem__(i) for i in xrange(*indices)]
        return super(MembershipTestList, self).__getitem__(k)
                    
    def __setitem__(self, k, seq):
        if isinstance(k, slice):
            indices = k.indices(len(self))
            posgen = iter(xrange(*indices))
            for v in seq:
                try:
                    pos = posgen.next()
                except:
                    pos += 1
                    posgen = itertools.count(pos+1)
                self.__setitem__(posgen.next(), v)
        else:
            self._members.add(seq)
            super(MembershipTestList, self).__setitem__(k, seq)
        
    def __delitem__(self, k):
        if isinstance(k, slice):
            indices = k.indices(len(self))
            for i in xrange(*indices):
                self.__delitem__(i)
        else:
            v = super(MembershipTestList, self).__getitem__(k)
            self._members.remove(v)
            super(MembershipTestList, self).__delitem__(k)

    def append(self, value):
        self._members.add(value)
        return super(MembershipTestList, self).append(value)

    def insert(self, pos, value):
        self._members.add(value)
        return super(MembershipTestList, self).insert(pos, value)

    def remove(self, value):
        self._members.remove( value )
        return super(MembershipTestList, self).remove(value)
    
    def extend(self, iterable):
        for x in iterable:
            self.append(x)
    
    def pop(self, index=None):
        if index is None:
            index = len(self)
        v = self[index]
        self.__delitem__(index)
        return v
        
    def __contains__(self, v):
        return v in self._members
## end of http://code.activestate.com/recipes/577185/ }}}
