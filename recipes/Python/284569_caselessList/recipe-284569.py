#  17-05-04
# v1.1.1
#

# caselessList
# A case insensitive list that only permits strings as keys.

# Implemented for ConfigObj
# Requires Python 2.2 or above

# Copyright Michael Foord
# Not for use in commercial projects without permission. (Although permission will probably be given).
# If you use in a non-commercial project then please credit me and include a link back.
# If you release the project non-commercially then let me know (and include this message with my code !)

# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# E-mail fuzzyman AT atlantibots DOT org DOT uk (or michael AT foord DOT me DO

class caselessList(list):
    """A case insensitive lists that has some caseless methods. Only allows strings as list members.
    Most methods that would normally return a list, return a caselessList. (Except list() and lowercopy())
    Sequence Methods implemented are :
    __contains__, remove, count, index, append, extend, insert,
    __getitem__, __setitem__, __getslice__, __setslice__
    __add__, __radd__, __iadd__, __mul__, __rmul__
    Plus Extra methods:
    findentry, copy , lowercopy, list
    Inherited methods :
    __imul__, __len__, __iter__, pop, reverse, sort
    """
    def __init__(self, inlist=[]):
        list.__init__(self)
        for entry in inlist:
            if not isinstance(entry, str): raise TypeError('Members of this object must be strings. You supplied \"%s\" which is \"%s\"' % (entry, type(entry)))
            self.append(entry)

    def findentry(self, item):
        """A caseless way of checking if an item is in the list or not.
        It returns None or the entry."""
        if not isinstance(item, str): raise TypeError('Members of this object must be strings. You supplied \"%s\"' % type(item))
        for entry in self:
            if item.lower() == entry.lower(): return entry
        return None
    
    def __contains__(self, item):
        """A caseless way of checking if a list has a member in it or not."""
        for entry in self:
            if item.lower() == entry.lower(): return True
        return False
        
    def remove(self, item):
        """Remove the first occurence of an item, the caseless way."""
        for entry in self:
            if item.lower() == entry.lower():
                list.remove(self, entry)
                return
        raise ValueError(': list.remove(x): x not in list')
    
    def copy(self):
        """Return a caselessList copy of self."""
        return caselessList(self)

    def list(self):
        """Return a normal list version of self."""
        return list(self)
        
    def lowercopy(self):
        """Return a lowercase (list) copy of self."""
        return [entry.lower() for entry in self]
    
    def append(self, item):
        """Adds an item to the list and checks it's a string."""
        if not isinstance(item, str): raise TypeError('Members of this object must be strings. You supplied \"%s\"' % type(item))
        list.append(self, item)
        
    def extend(self, item):
        """Extend the list with another list. Each member of the list must be a string."""
        if not isinstance(item, list): raise TypeError('You can only extend lists with lists. You supplied \"%s\"' % type(item))
        for entry in item:
            if not isinstance(entry, str): raise TypeError('Members of this object must be strings. You supplied \"%s\"' % type(entry))
            list.append(self, entry)        

    def count(self, item):
        """Counts references to 'item' in a caseless manner.
        If item is not a string it will always return 0."""
        if not isinstance(item, str): return 0
        count = 0
        for entry in self:
            if item.lower() == entry.lower():
                count += 1
        return count    

    def index(self, item, minindex=0, maxindex=None):
        """Provide an index of first occurence of item in the list. (or raise a ValueError if item not present)
        If item is not a string, will raise a TypeError.
        minindex and maxindex are also optional arguments
        s.index(x[, i[, j]]) return smallest k such that s[k] == x and i <= k < j
        """
        if maxindex == None: maxindex = len(self)
        minindex = max(0, minindex)-1
        maxindex = min(len(self), maxindex)
        if not isinstance(item, str): raise TypeError('Members of this object must be strings. You supplied \"%s\"' % type(item))
        index = minindex
        while index < maxindex:
            index += 1
            if item.lower() == self[index].lower():
                return index
        raise ValueError(': list.index(x): x not in list')
    
    def insert(self, i, x):
        """s.insert(i, x) same as s[i:i] = [x]
        Raises TypeError if x isn't a string."""
        if not isinstance(x, str): raise TypeError('Members of this object must be strings. You supplied \"%s\"' % type(x))
        list.insert(self, i, x)

    def __setitem__(self, index, value):
        """For setting values in the list.
        index must be an integer or (extended) slice object. (__setslice__ used for simple slices)
        If index is an integer then value must be a string.
        If index is a slice object then value must be a list of strings - with the same length as the slice object requires.
        """
        if isinstance(index, int):
            if not isinstance(value, str): raise TypeError('Members of this object must be strings. You supplied \"%s\"' % type(value))
            list.__setitem__(self, index, value)
        elif isinstance(index, slice):
            if not hasattr(value, '__len__'): raise TypeError('Value given to set slice is not a sequence object.')
            for entry in value:
                if not isinstance(entry, str): raise TypeError('Members of this object must be strings. You supplied \"%s\"' % type(entry))
            list.__setitem__(self, index, value)
        else:
            raise TypeError('Indexes must be integers or slice objects.')

    def __setslice__(self, i, j, sequence):
        """Called to implement assignment to self[i:j]."""
        for entry in sequence:
            if not isinstance(entry, str): raise TypeError('Members of this object must be strings. You supplied \"%s\"' % type(entry))
        list.__setslice__(self, i, j, sequence)

    def __getslice__(self, i, j):
        """Called to implement evaluation of self[i:j].
        Although the manual says this method is deprecated - if I don't define it the list one is called.
        (Which returns a list - this returns a caselessList)"""
        return caselessList(list.__getslice__(self, i, j))

    def __getitem__(self, index):
        """For fetching indexes.
        If a slice is fetched then the list returned is a caselessList."""
        if not isinstance(index, slice):
            return list.__getitem__(self, index)
        else:
            return caselessList(list.__getitem__(self, index))
            
    def __add__(self, item):
        """To add a list, and return a caselessList.
        Every element of item must be a string."""
        return caselessList(list.__add__(self, item))

    def __radd__(self, item):
        """To add a list, and return a caselessList.
        Every element of item must be a string."""
        return caselessList(list.__add__(self, item))
    
    def __iadd__(self, item):
        """To add a list in place."""
        for entry in item: self.append(entry)        

    def __mul__(self, item):
        """To multiply itself, and return a caselessList.
        Every element of item must be a string."""
        return caselessList(list.__mul__(self, item))

    def __rmul__(self, item):
        """To multiply itself, and return a caselessList.
        Every element of item must be a string."""
        return caselessList(list.__rmul__(self, item))

####################################################################################

# brief test stuff
if __name__ == '__main__':
    print
    print 'caselessList Tests :'
    a = caselessList(['hello', 'HELLO', 'HellO'])
    print 'A caselessList : ', a
    print 'a.findentry(\'hELLO\') = ', a.findentry('hELLO')
    print '(prints the first entry that matches this)', '\n'
    print '\'HeLLo\' in a : ', 'HeLLo' in a, '\n'                   # tests __contains__
    a.remove('HeLlO')
    print 'a.remove(\'HeLlO\'), print a : ', a
    print 'type(a.copy()) : ', type(a.copy())
    print 'type(a.list()) : ', type(a.list())
    print 'a.lowercopy() : ', a.lowercopy()
    a.append('HeLlO')
    print 'a.append(\'HeLlO\'), print a : ', a
    a.extend([char for char in 'AaAaA'])
    print 'a.extend([char for char in \'AaAaA\']), print a, type(a) : '
    print a, ',', type(a)
    print 'a.count(\'A\') : ', a.count('A')
    print 'a.index(\'A\') : ', a.index('a')
    a.insert(1, 'WisH')
    print 'a.insert(1, \'WisH\') : ',a
    print
    print 'The __setitem__ method is only novel for extended slice operations.'
    a[0:10:3] = ['Fish', 'fIsh', 'fiSh']
    print "a[0:10:3] = ['Fish', 'fIsh', 'fiSh'] : ", a
    print
    print 'Most interesting thing about __getitem__ is that if you ask for a slice - it will be an instance of caselessList'
    print 'type(a[0:4:1]) : ', type(a[0:4:1])
    
        
"""
15-05-04       Version 1.1.0
Added caselessList a caseless List implementation.
Lot more work than dict actually - more methods to implement for a sequence object.
Changed module name from caselessDict to caseless.
"""
