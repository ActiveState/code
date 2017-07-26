# Copyright (c) 2011, Roger Lew 
# This software is funded in part by NIH Grant P20 RR016454.
"""This module contains the DictSet class"""

__version__ = 'V0.3.1.2'

# Python 2 to 3 workarounds
import sys
if sys.version_info[0] == 2:
    _xrange = xrange
elif sys.version_info[0] == 3:
    from functools import reduce
    _xrange = range

from copy import copy, deepcopy    

# for unique_combinations method
def _rep_generator(A, times, each):
    """like r's rep function, but returns a generator

      Examples:
        >>> g=_rep_generator([1,2,3],times=1,each=3)
        >>> [v for v in g]
        [1, 1, 1, 2, 2, 2, 3, 3, 3]

        >>> g=_rep_generator([1,2,3],times=3,each=1)
        >>> [v for v in g]
        [1, 2, 3, 1, 2, 3, 1, 2, 3]
        
        >>> g=_rep_generator([1,2,3],times=2,each=2)
        >>> [v for v in g]
        [1, 1, 2, 2, 3, 3, 1, 1, 2, 2, 3, 3]
    """
    return (a for t in _xrange(times) for a in A for e in _xrange(each))


class DictSet(dict):
    """A dictionary of sets that behaves like a set."""
    def __init__(*args, **kwds): # args[0] -> 'self'
        """
            DictSet() -> new empty dictionary of sets
            DictSet(mapping) -> new dictionary of sets initialized from a
                mapping object's (key, value) pairs.
                Because the values become sets they must be iterable
                
            DictSet(iterable) -> new dictionary of sets initialized as if via:
                d = DictSet()
                for k, v in iterable:
                    d[k] = set(v)
                    
            DictSet(**kwargs) -> new dictionary of sets initialized with the
                name=value pairs in the keyword argument list.
                For example:  DictSet(one=[1], two=[2])
        """
        # passing self with *args ensures that we can use
        # self as keyword for initializing a DictSet
        # Example: DictSet(self='abc', other='efg')

        # call update or complain about having too many arguments
        if len(args) == 1:
            args[0].update({}, **kwds)
            
        elif len(args) == 2:
            args[0].update(args[1], **kwds)

        elif len(args) > 2:
            raise TypeError(
            'DictSet expected at most 1 arguments, got %d' % (len(args) - 1))
        
    def update(*args, **kwds): # args[0] -> 'self'
        """
        DS.update(E, **F) -> None.

        Update DS from the union of DictSet/dict/iterable E and F.
        
        If E has a .keys() method, does:
            for k in E:
                DS[k] |= set(E[k])
            
        If E lacks .keys() method, does:
            for (k, v) in E:
                DS[k] |= set(v)
            
        In either case, this is followed by:
            for k in F:
                DS[k] |= set(F[k])

        DS|=E  <==> DS.update(E)
        """
        # check the length of args
        if len(args) > 2:
            raise TypeError(
            'DictSet expected at most 1 arguments, got %d' % (len(args) - 1))

        # Make sure args can be mapped to a DictSet before
        # we start adding them.
        elif len(args) == 2:
            obj = args[1]

            # if obj is a DictType we can avoid checking
            # to make sure it is hashable an iterable
            if type(obj) == DictSet:
                pass
            
            # Check using duck typing
            elif hasattr(obj, '__getitem__'):

                # obj is dict or dict subclass
                if hasattr(obj, 'keys'):
                    for k, val in obj.items():
                        if not hasattr(k,'__hash__'):
                            raise TypeError(
                                "unhashable type: '%s'" % type(k).__name__)
                        
                        if not hasattr(val,'__iter__'):
                            if not isinstance(val, str):
                                raise TypeError(
                        "'%s' object is not iterable" % type(val).__name__)

                # obj is list/tuple or list/tuple subclass
                else:
                    for item in obj:
                        try:
                            (k, val)=item
                        except:
                            raise TypeError(
                                  'could not unpack arg to key/value pairs')

                        if not hasattr(k,'__hash__'):
                            raise TypeError(
                                "unhashable type: '%s'" % type(k).__name__)
                        
                        if not hasattr(val,'__iter__'):
                            if not isinstance(val, str):
                                raise TypeError(
                        "'%s' object is not iterable" % type(val).__name__)

            # obj is not iterable, e.g. an int, float, etc.
            else:
                raise TypeError(
                         "'%s' object is not iterable" % type(obj).__name__)
                    
        # check the keyword arguments
        for (k, val) in kwds.items():
            # unhashable keyword argumnents don't make it to the point 
            # so we just need to check that the values are iterable
            if not hasattr(val,'__iter__'):
                if not isinstance(val, str):
                    raise TypeError(
                         "'%s' object is not iterable" % type(val).__name__)

        # At this point we can be fairly certain the args and kwds 
        # will successfully initialize. Now we can go back through
        # args and kwds and add them to ds
        if len(args) == 2:
            obj = args[1]

            # obj is dict or dict subclass
            if hasattr(obj, 'keys'):
                for k, val in obj.items():
                    if not k in args[0].keys():
                        args[0][k] = set(val)
                    args[0][k] |= set(val)

            # obj is list/tuple or list/tuple subclass
            else:
                for item in obj:
                    (k, val) = item
                    if not k in args[0].keys():
                        args[0][k] = set(val)
                    args[0][k] |= set(val)

        # Now add keyword arguments
        for (k, val) in kwds.items():
            if not k in args[0].keys():
                args[0][k] = set(val)
            args[0][k] |= set(val)

    def __ior__(self, E): # overloads |=
        """
        DS.update(E, **F) -> None.

        Update DS from the union of DictSet/dict/iterable E and F.
        
        If E has a .keys() method, does:
            for k in E:
                DS[k] |= set(E[k])
            
        If E lacks .keys() method, does:
            for (k, v) in E:
                DS[k] |= set(v)
            
        In either case, this is followed by:
            for k in F:
                DS[k] |= set(F[k])

        DS|=E  <==> DS.update(E)
        """
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))
            
        return self.union(E)
    
    def __eq__(self, E): # overloads ==
        """
        Returns the equality comparison of DS with E typed
        as a DictSet. If E cannot be broadcast into a DictSet
        returns False.

        DS==E  <==> DS.__eq__(E)
        """
        # Fails of d is not mappable with iterable values
        try:
            E = DictSet(E)
        except:
            return False

        # check to see if self and E have the same keys
        # if they don't we know they aren't equal and
        # can return False
        if len(set(k for (k, v) in self.items() if len(v) != 0)  ^
               set(k for (k, v) in    E.items() if len(v) != 0)) > 0:
            return False

        # at this point we know they have the same keys
        # if all the non-empty set differences have 0 cardinality
        # the sets are equal
        s = 0
        for k in self.keys():
            s += len(self.get(k, []) ^ E.get(k, []))
        return s == 0

    def __ne__(self, E): # overloads !=
        """
        Returns the non-equality comparison of ES with E type
        as a DictSet. If E cannot be broadcast into a DictSet
        returns False.

        DS==E  <==> DS.__ne__(E)
        """
        # Fails of d is not mappable with iterable values
        try:
            E = DictSet(E)
        except:
            return True

        # check to see if self and d have the same keys
        # if they don't we know they aren't equal and
        # can return False
        if len(set(k for (k, v) in self.items() if len(v) != 0)  ^
               set(k for (k, v) in    E.items() if len(v) != 0)) > 0:
            return True

        # at this point we know they have the same keys
        # if all the set differences have 0 cardinality
        # the sets are equal
        s = 0
        for k in self.keys():
            s += len(self.get(k, []) ^ E.get(k, []))
        return s != 0
        
    def issubset(self, E):
        """
        Report whether all the sets of this DictSet are subsets of the E.

        DS<=E  <==> DS.issubset(E)
        """
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))
            
        if self == E == {}:
            return True

        b = True
        for k in set(self) | set(E):
            if not self.get(k, []) <= E.get(k, []):
                b = False
            
        return b

    def __le__(self, E): # overloads <=
        """
        Report whether all the sets of this DictSet are subsets of the E.

        DS<=E  <==> DS.issubset(E)
        """        
        return self.issubset(E)

    def issuperset(self, E):
        """
        Report whether all the sets of this DictSet are supersets of the E.

        DS>=E  <==> DS.issuperset(E)
        """        
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))
            
        if self == E == {}:
            return True

        b = True
        for k in set(self) | set(E):
            if not self.get(k, []) >= E.get(k, []):
                b = False
            
        return b
    
    def __ge__(self, E): # overloads >=
        """
        Report whether all the sets of this DictSet are supersets of the E.

        DS>=E  <==> DS.issuperset(E)
        """        
        return self.issuperset(E)
        
    def union(self, E):
        """
        Return the union of the sets of self with the sets of E.
        
        (i.e. all elements that are in either sets of the DictSets.)

        DS|E  <==> DS.union(E)
        """        
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))
            
        foo = deepcopy(self)
        for k in set(foo.keys()) | set(E.keys()):
            foo.setdefault(k, [])
            foo[k].update(E.get(k, []))
            if not foo[k]:
                del foo[k] # delete if empty set

        return foo

    def __or__(self, E): # overloads |
        """
        Return the union of the sets of self with the sets of E.
        
        (i.e. all elements that are in either sets of the DictSets.)

        DS|E  <==> DS.union(E)
        """    
        return self.union(E)

    def intersection(self, E):
        """
        Return the intersection of the sets of self with the sets of E.
        
        (i.e. elements that are common to all of the sets of the
         DictSets.)

        DS&E  <==> DS.intersection(E)
        """           
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))

        # handle case where d=={}
        if E == {}:
            return DictSet()
        
        foo = deepcopy(self)
        for k in set(foo.keys()) | set(E.keys()):
            foo.setdefault(k, [])
            foo[k].intersection_update(E.get(k, []))
            if not foo[k]:
                del foo[k] # delete if empty set

        return foo

    def __and__(self, E): # overloads &
        """
        Return the intersection of the sets of self with the sets of E.
        
        (i.e. elements that are common to all of the sets of the
         DictSets.)

        DS&E  <==> DS.intersection(E)
        """   
        return self.intersection(E)

    def difference(self, E):
        """
        Return the difference of the sets of self with the sets of E.
        
        (i.e. all elements that are in the sets of this DictSet but
         not the others.)

        DS-E  <==> DS.difference(E)
        """   
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))

        foo = deepcopy(self)
        for k in set(foo.keys()) | set(E.keys()):
            foo.setdefault(k, [])
            foo[k].difference_update(E.get(k, []))
            if not foo[k]:
                del foo[k] # delete if empty set

        return foo

    def __sub__(self, E): # overloads -
        """
        Return the difference of the sets of self with the sets of E.
        
        (i.e. all elements that are in the sets of this DictSet but
         not the others.)

        DS-E  <==> DS.difference(E)
        """         
        return self.difference(E)

    def symmetric_difference(self, E):
        """
        Return the symmetric difference of the sets of self with the
        sets of E.
        
        (i.e. for each DictSet all elements that are in exactly one
         of the sets .)

        DS^E  <==> DS.symmetric_difference(E)
        """        
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))

        foo = deepcopy(self)
        for k in set(foo.keys()) | set(E.keys()):
            foo.setdefault(k, [])
            foo[k].symmetric_difference_update(E.get(k, []))
            if not foo[k]:
                del foo[k] # delete if empty set

        return foo

    def __xor__(self, E): # overloads ^
        """
        Return the symmetric difference of the sets of self with the
        sets of E.
        
        (i.e. for each DictSet all elements that are in exactly one
         of the sets .)

        DS^E  <==> DS.symmetric_difference(E)
        """
        return self.symmetric_difference(E)

    def intersection_update(self, E):
        """
        Update a DictSet with the intersection of itself and E.

        DS&=E  <==> DS.intersection_update(E)
        """        
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))
        
        for k in set(self) | set(E):
            self.setdefault(k, [])
            self[k].intersection_update(E.get(k, []))
            if len(self[k]) == 0:
                del self[k]

    def __iand__(self, E): # overloads &=
        """
        Update a DictSet with the intersection of itself and E.

        DS&=E  <==> DS.intersection_update(E)
        """   
        return self.intersection(E)
        
    def difference_update(self, E):
        """
        Update a DictSet with the difference of itself and E.

        DS-=E  <==> DS.difference_update(E)
        """     
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))
        
        for k in set(self)|set(E):
            self.setdefault(k, [])
            self[k].difference_update(E.get(k, []))
            if len(self[k]) == 0:
                del self[k]

    def __isub__(self, E): # overloads -=
        """
        Update a DictSet with the difference of itself and E.

        DS-=E  <==> DS.difference_update(E)
        """     
        return self.difference(E)
        
    def symmetric_difference_update(self, E):
        """
        Update a DictSet with the symmetric difference of
        itself and E.

        DS^=E  <==> DS.symmetric_difference_update(E)
        """     
        if not isinstance(E, DictSet):
            E = DictSet(copy(E))
        
        for k in set(self) | set(E):
            self.setdefault(k, [])
            self[k].symmetric_difference_update(E.get(k, []))
            if len(self[k]) == 0:
                del self[k]

    def __ixor__(self, E): # overloads ^=
        """
        Update a DictSet with the symmetric difference of
        itself and E.

        DS^=E  <==> DS.symmetric_difference_update(E)
        """    
        return self.symmetric_difference(E)

    def add(self, k, v=None):
        """
        Add an element v to a set DS[k].
        This has no effect if the element v is already present in DS[k].
        
        When v is not supplied adds a new set at DS[k].
        Raises KeyError if k is not hashable.
        """

        if k not in self.keys():
            self[k] = set()
            
        if v != None:
            self[k].add(v)

    def __setitem__(self, k, v):
        """DS.__setitem__(k, v) <==> x[k]=set(v)"""
        if isinstance(v, set):
            super(DictSet, self).__setitem__(k, v)
        else:
            try:
                super(DictSet, self).__setitem__(k, set(v))
            except:
                raise

    def __contains__(self, k):
        """
        True if DS has a key k and len(DS[k])!=0, else False
        
        DS.__contains__(k) <==> k in D 
        """

        return k in [key for (key, val) in self.items() if len(val) > 0]

    def __iter__(self):
        """
        Iterate over keys with non-zero lengths.
        
        DS.__iter__(k) <==> for k in D 
        """
        for (key, val) in self.items():
            if len(val) > 0:
                yield key
                    
    def get(self, k, v=None):
        """
        DS.get(k[,v]) -> DS[v] if k in DS, else set(v).
        v defaults to None.
        """
        if k in self:
            return self[k]
        if v == None:
            return

        try:
            return set(v)
        except:
            raise

    def setdefault(self, k, v=None):
        """
        DS.setdefault(k[,v]) -> DS.get(k, v), also set DS[k]=set(v)
        if k not in D.  v defaults to None.
        """
        if k in self:
            return self[k]

        if v == None:
            return
        else:
            try:
                super(DictSet, self).__setitem__(k, set(v))
            except:
                raise
            return self[k]
        
    def copy(self):
        """DS.copy() -> a shallow copy of DS."""
        return copy(self)
    
    def remove(self, k, v=None):
        """
        Remove element v from a set DS[k]; it must be a member.
        If the element v is not a member of D[k], raise a KeyError.
            
        If v is not supplied removes DS[k]; it must be an item.
        if D[k] is not an item, raise a KeyError.
        """
        if k not in self.keys():
            raise KeyError(k)
        
        if v != None:
            self[k].remove(v)
        else:
            del self[k]
            
    def discard(self, k, v=None):
        """
        Remove element v from a set DS[k]; it must be a member.
        If the element v is not a member of D[k], do nothing.
            
        If v is not supplied removes DS[k].
        If D[k] is not an item, raise a KeyError.
        """

        if v != None:
            try:
                self[k].discard(v)
            except:
                pass
        else:
            try:
                del self[k]
            except:
                pass

    
    # borrowed from the collections.OrderedDict in the standard library 
    def __repr__(self):
        """DS.__repr__() <==> repr(DS)"""
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self.items()))

    def unique_combinations(self, keys=None):
        """
        Returns a generator yielding the unique combination of
        elements. Both the keys of DS and the elements of the
        sets are sorted.

        When a key list (the keys argument) is supplied only the
        unique combinations of the sets specified by the keys are
        yielded by the generator.

        The combinations are sorted by slowest repeating to fastest
        repeating.
        """
        # it the keys argument is not supplied assume the
        # user wants the unique combinations of all the
        # elements of all the sets
        if keys == None:
            keys = sorted(self.keys())

        # eliminate keys to sets that have zero cardinality
        try:
            keys = [k for k in keys if k in self]
        except:
            raise TypeError("'%s' object is not iterable"
                            %type(keys).__name__)

        # if the keys list is empty we can return an empty generator
        if len(keys) == 0:
            yield
        else:
            
            # the number of unique combinations is the product 
            # of the cardinalities of the non-zero sets
            N = reduce(int.__mul__,(len(self[k]) for k in keys))

            # now we need to build a dict of generators so we
            # can build a generator or generators. To do this
            # we need to figure out the each and times
            # parameters to pass to rep()
            gen_dict = {}
            each = 1
            times = 0
            prev_n = 0
            for i, k in enumerate(reversed(keys)):
                if i != 0:
                    each *= prev_n
                times = N / (len(self[k]) * each)
                prev_n = len(self[k])

                gen_dict[k] = _rep_generator(sorted(self[k]),
                                             int(times),int(each))

            # Now we just have to yield the results
            for i in _xrange(N):
                yield [next(gen_dict[k]) for k in keys]

    @classmethod
    def fromkeys(cls, seq, values=None):
        """
        Create a new DictSet with keys from seq and values set to
        set(values). When values is not supplied the values are
        initialized as empty sets.
        """
        d = cls()
        for key in seq:
            if values == None:
                d[key] = set()
            else:
                d[key] = set(values)
                
        return d
