#!/usr/bin/env python             
# This file is licensed under the GNU General Public License found at <http://www.gnu.org/licenses>
# email:  Mark Janssen <dreamingforward@gmail.com>

"""Dictionary with default values, collision function, and sorted string output."""

import exceptions
import copy

class KeyAlreadyExists(exceptions.LookupError): pass
class _use_default_:
    """Dummy class used as value in function parameters to indicate
    no default value specified; i.e. use the value in DefDict._default.
    Created special class to avoid clashing with possible value passed
    by user."""
#XXX perhaps should have instantiate default which takes arbitrary
# number of parameters that will be passed to value stored in DefDict._default
# to allow object creation.  DefDict.add would check if isinstance(default, _use_default_)

#define some useful collision functions
#May wish to return an expression instead of setting ddict directly
#  to allow lambda functions to be passed as collision functions.
#  may sacrifice speed for cases when value modified in place or when old value lookup not needed.
_OVERWRITE_ = None   #i.e. will use standard dict overwrite semantics
def _RETAIN_(ddict, key, new_value): pass  #do nothing to the value
def _RAISE_(ddict, key, new_value): raise KeyAlreadyExists, repr(key)
def _ADD_(ddict, key, new_value): ddict[key] += new_value
def _MAX_(ddict, key, new_value): ddict[key] = max(ddict[key], new_value)
def _MIN_(ddict, key, new_value): ddict[key] = min(ddict[key], new_value)
def _OUTPUT_KEY_(ddict, key, new_value): print key   #should probably send to stderr


class DefDict(dict):
    """Extends standard dictionary type by allowing user to
    specify a default value when a key is inserted.
    A 'collision' function can be provided to specify what should
    be done to the value when a key is added that already exists.

    User-defined collision function should take
    (defdict, key, new_value) as parameters.
    """
    #XXX may wish to have collision method instead of constantly passing as parameter

    __slots__ = ['_default']

    def __init__(self, init={}, default=None, collision=_OVERWRITE_):
        """Create dictionary and initialize with mapping or list of (key, value) pairs, if given.
        Sets a default value for the keys when no other specified.

        Initialization interface similar to standard dictionary:
        >>> dd = DefDict()  #create empty DefDict
        >>> print dd
        {}
        >>> print DefDict({1: 1, 2: 4, 3: 9}) #initialize with dict type
        {1: 1, 2: 4, 3: 9}

        Initialize with list of (key, value) pairs:
        >>> print DefDict([('a', 2), ('b', 3), ('c', 1), ('a', 5)], collision=_ADD_)
        {'a': 7, 'b': 3, 'c': 1}

        A sequence of (key, value) pairs may contain duplicate keys, like above.
        The resulting value of such "key collisions" can be specified
        by providing a collision function.  The collision function will
        be called with parameters (self, key, new_value) and should set the
        value of self[key] as desired.

        This module defines a few useful collision functions:

        _OVERWRITE_:  the default--standard dictionary semantics;
            i.e. if key already exists, new value overwrites existing
            key value.
        _RETAIN_:  value remains unchanged if key already exists.
        _RAISE_EXCEPTION_:  raise 'KeyAlreadyExists' exception if key already
            exists.  Value remains unchanged.
        _ADD_:  sets value to existing value + new value
        _MAX_:  sets to greater of old, new values
        _MIN_:  sets to lesser of old, new values
        """

        self._default = default
        dict.__init__(self)
        if isinstance(init, dict): #don't use dict(init) since derives classes have special setitem behavior
            init = init.iteritems()
        #list of (key, value) pairs may contain duplicates
        for key, value in init:
            self.setdefault(key, value, collision)

    def fromkeys(cls, iterable, default=None, collision=_OVERWRITE_):
        """Create dictionary from iterable with optional default value.

        One can initialize defdict with a sequence of keys.
        The dictionary values of the keys will be determined by the default value,
        if given, otherwise defaults to None.

        >>> print DefDict.fromkeys(["apple", "banana", "carrot"])
        {'apple': None, 'banana': None, 'carrot': None}
        >>> dd = DefDict.fromkeys(range(4), 0)   #initialize with values = 0
        >>> print dd
        {0: 0, 1: 0, 2: 0, 3: 0}
        >>> dd.update([0])  #default value retained?
        >>> print dd[0]     #Yes if output is 1
        1
        >>> print DefDict.fromkeys("abacab", 1, _ADD_)
        {'a': 3, 'b': 2, 'c': 1}
        """
        dd = cls(default=default)
        for key in iterable:
             dd.setdefault(key, default, collision)
        return dd

    fromkeys = classmethod(fromkeys)

    def update(self, other, collision=_OVERWRITE_):
        """Updates defdict from mapping type or iterable with optional collision function.

        >>> d = DefDict.fromkeys('ab', 1)
        >>> d.update({'a': 0, 'c': 2})
        >>> print d
        {'a': 0, 'b': 1, 'c': 2}

        As seen above, when updating a key which already exists and no
        collision function is specified, update defaults to standard dictionary
        OVERWRITE semantics.  This behavior can be modified by passing a
        collision function.

        >>> d.update({'b': 3, 'd': 9}, _ADD_)
        >>> print d
        {'a': 0, 'b': 4, 'c': 2, 'd': 9}

        >>> d._default = 5          #manually change default value
        >>> d.update(['b','c'])     #update from non-dict
        >>> d._default = 1          #set back to original
        >>> d.update('abd')         #string are iterated
        >>> print d
        {'a': 1, 'b': 1, 'c': 5, 'd': 1}
        >>> d.update('de', _ADD_)
        >>> print d
        {'a': 1, 'b': 1, 'c': 5, 'd': 2, 'e': 1}

        NOTE:  If collision function raises an exception, DefDict may be
        left in partially-updated state.
        """
        #perhaps should catch any exceptions that may be caused by collision
        #  and store aberrent keys in the exception to be reported later.
        if isinstance(other, dict):
            for key, value in other.iteritems():
                self.setdefault(key, value, collision)
        else:  #given iterable
            for key in other: 
                self.setdefault(key, self._default, collision)

    def setdefault(self, key, value = _use_default_, collision=_RETAIN_):
        """Behaves like standard dict.setdefault, but uses value in _default attribute 
        if no default parameter specified.

        >>> dd = DefDict(default=5)
        >>> dd.setdefault('a', 10), dd.setdefault('b'), dd.setdefault('b', 11)
        (10, 5, 5)
        >>> print dd
        {'a': 10, 'b': 5}

        A collision function can also be passed to override setdefault's
        standard RETAIN semantics.

        >>> dd.setdefault('a', collision=_OVERWRITE_), dd.setdefault('b', 6, _ADD_)
        (5, 11)
        >>> dd.setdefault('b', 12, _MAX_), dd.setdefault('b', 10, _MAX_)
        (12, 12)
        >>> dd.setdefault('c', 10, _RAISE_)
        10
        >>> dd.setdefault('c', 10, _RAISE_)
        Traceback (most recent call last):
        KeyAlreadyExists: 'c'
        >>> print dd
        {'a': 5, 'b': 12, 'c': 10}

        Default value is NOT copied if non-simple type (ex. list, dict).
        If values must be distinct objects, then you must subclass and
        override this method or __setitem__() to create a copy of the default.

        >>> dd = DefDict(default=[])
        >>> dd.setdefault(1), dd.setdefault(2)
        ([], [])
        >>> dd[1] is dd[2]  #keys 1 and 2 do have distinct list objects
        True
        >>> dd[2].append(42) #will also change value in dd[1]!!!
        >>> print dd
        {1: [42], 2: [42]}
        """
        key_absent = key not in self   #fail immediately if key unhashable
        if value == _use_default_: value = self._default #XXX should make copy for non-simple default, or rely on __setitem__() to make copy?
        if collision == _OVERWRITE_ or key_absent:
            self[key] = value #note: subclass may override setitem method so value may be modified
        else:
            collision(self, key, value)
        return dict.__getitem__(self, key)  #may wish to allow dd[key] to insert key in dd with default value

    def get(self, key, *args):
        """Behaves like standard dict.get, but uses value in _default attribute 
        if no default parameter specified.

        >>> dd = DefDict({'a': 10}, 0)
        >>> dd.get('a'), dd.get('b'), dd.get('b', 11)
        (10, 0, 11)
        >>> print dd
        {'a': 10}
        """
        if not args: args = (self._default,)
        return dict.get(self, key, *args)

    def copy(self):
        """Return shallow copy of dictionary.

        >>> dd = DefDict.fromkeys(range(5), 5)
        >>> ddcopy = dd.copy()
        >>> print ddcopy._default, isinstance(ddcopy, DefDict); print ddcopy
        5 True
        {0: 5, 1: 5, 2: 5, 3: 5, 4: 5}
        >>> ddcopy[0] = 7
        >>> print dd[0], ddcopy[0]
        5 7
        """
        return self.__class__(self, self._default)

    __copy__ = copy

    def __str__(self):
        """Convert self to string with keys in sorted order.

        >>> str(DefDict())
        '{}'
        >>> str(DefDict({9: 0, 'test': 0, 'a': 0, 0: 0}))
        "{0: 0, 9: 0, 'a': 0, 'test': 0}"
        """
        if not self: return '{}'    #nothing to sort
        keys = self.keys()
        keys.sort()
        return '{' + ', '.join(["%r: %s" % (k, self[k]) for k in keys]) + '}'


if __name__ == "__main__":
    import doctest
    print doctest.testmod()
