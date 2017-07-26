#!/usr/bin/env python
#
# sorteddict.py
# Sorted dictionary (implementation for Python 2.x)
#
# Copyright (c) 2010 Jan Kaliszewski (zuo)
#
# The MIT License:
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from bisect import bisect_left, insort
from itertools import izip, repeat


def dictdoc(method):
    "A decorator making reuse of the ordinary dict's docstrings more concise."
    dict_method = getattr(dict, method.__name__)
    if hasattr(dict_method, '__doc__'):
        method.__doc__ = dict_method.__doc__
    return method


class SortedDict(dict):
    '''Dictionary with sorted keys.

    The interface is similar to the ordinary dict's one, but:
    * methods: __repr__(), __str__(), __iter__(), iterkeys(), itervalues(),
      iteritems(), keys(), values(), items() and popitem() -- return results
      taking into consideration sorted keys order;
    * new methods: largest_key(), largest_item(), smallest_key(),
      smallest_item() added.
    '''

    def __init__(self, *args, **kwargs):
        '''Like with the ordinary dict: from a mapping, from an iterable
        of (key, value) pairs, or from keyword arguments.'''
        dict.__init__(self, *args, **kwargs)
        self._sorted_keys = sorted(dict.iterkeys(self))

    @dictdoc
    def __repr__(self):
        return 'SortedDict({%s})' % ', '.join('%r: %r' % item
                                              for item in self.iteritems())
                                              
    @dictdoc
    def __str__(self):
        return repr(self)

    @dictdoc
    def __setitem__(self, key, value):
        key_is_new = key not in self
        dict.__setitem__(self, key, value)
        if key_is_new:
            insort(self._sorted_keys, key)

    @dictdoc
    def __delitem__(self, key):
        dict.__delitem__(self, key)
        del self._sorted_keys[bisect_left(self._sorted_keys, key)]

    def __iter__(self, reverse=False):
        '''D.__iter__() <==> iter(D) <==> D.iterkeys() -> an iterator over
        sorted keys (add reverse=True for reverse ordering).'''
        if reverse:
            return reversed(self._sorted_keys)
        else:
            return iter(self._sorted_keys)

    iterkeys = __iter__

    def itervalues(self, reverse=False):
        '''D.itervalues() -> an iterator over values sorted by keys
        (add reverse=True for reverse ordering).'''
        return (self[key] for key in self.iterkeys(reverse))

    def iteritems(self, reverse=False):
        '''D.iteritems() -> an iterator over (key, value) pairs sorted by keys
        (add reverse=True for reverse ordering).'''
        return ((key, self[key]) for key in self.iterkeys(reverse))

    def keys(self, reverse=False):
        '''D.keys() -> a sorted list of keys
        (add reverse=True for reverse ordering).'''
        return list(self.iterkeys(reverse))

    def values(self, reverse=False):
        '''D.values() -> a list of values sorted by keys
        (add reverse=True for reverse ordering).'''
        return list(self.itervalues(reverse))

    def items(self, reverse=False):
        '''D.items() -> a list of (key, value) pairs sorted by keys
        (add reverse=True for reverse ordering).'''
        return list(self.iteritems(reverse))

    @dictdoc
    def clear(self):
        dict.clear(self)
        del self._sorted_keys[:]

    def copy(self):
        '''D.copy() -> a shallow copy of D (still as a SortedDict).'''
        return self.__class__(self)

    @classmethod
    @dictdoc
    def fromkeys(cls, seq, value=None):
        return cls(izip(seq, repeat(value)))

    @dictdoc
    def pop(self, key, *args, **kwargs):
        if key in self:
            del self._sorted_keys[bisect_left(self._sorted_keys, key)]
        return dict.pop(self, key, *args, **kwargs)

    def popitem(self):
        '''D.popitem() -> (k, v). Remove and return a (key, value) pair with
        the largest key; raise KeyError if D is empty.'''
        try:
            key = self._sorted_keys.pop()
        except IndexError:
            raise KeyError('popitem(): dictionary is empty')
        else:
            return key, dict.pop(self, key)

    @dictdoc
    def setdefault(self, key, default=None):
        if key not in self:
            insort(self._sorted_keys, key)
        return dict.setdefault(self, key, default)

    @dictdoc
    def update(self, other=()):
        if hasattr(other, 'keys') and hasattr(other, 'values'):
            # mapping
            newkeys = [key for key in other if key not in self]
        else:
            # iterator/seqence of pairs
            other = list(other)
            newkeys = [key for key, _ in other if key not in self]
        dict.update(self, other)
        for key in newkeys:
            insort(self._sorted_keys, key)

    def largest_key(self):
        '''D.largest_key() -> the largest key; raise KeyError if D is empty.'''
        try:
            return self._sorted_keys[-1]
        except IndexError:
            raise KeyError('largest_key(): dictionary is empty')

    def largest_item(self):
        '''D.largest_item() -> a (key, value) pair with the largest key;
        raise KeyError if D is empty.'''
        key = self.largest_key()
        return key, self[key]

    def smallest_key(self):
        '''D.smallest_key() -> the smallest key; raise KeyError if D is empty.'''
        try:
            return self._sorted_keys[0]
        except IndexError:
            raise KeyError('smallest_key(): dictionary is empty')

    def smallest_item(self):
        '''D.smallest_item() -> a (key, value) pair with the smallest key;
        raise KeyError if D is empty.'''
        key = self.smallest_key()
        return key, self[key]
