import collections
import operator
import sys
import itertools
import reprlib

# a wrapper to make an object hashable, while preserving equality
class AutoHash:
    # for each known container type, we can optionally provide a tuple
    # specifying: type, transform, aggregator
    # even immutable types need to be included, since their items
    # may make them unhashable

    # transformation may be used to enforce the desired iteration
    # the result of a transformation must be an iterable
    # default: no change; for dictionaries, we use .items() to see values
    
    # usually transformation choice only affects efficiency, not correctness
    
    # aggregator is the function that combines all items into one object
    # default: frozenset; for ordered containers, we can use tuple
    
    # aggregator choice affects both efficiency and correctness
    # e.g., using a tuple aggregator for a set is incorrect,
    # since identical sets may end up with different hash values
    # frozenset is safe since at worst it just causes more collisions
    # unfortunately, no collections.ABC class is available that helps
    # distinguish ordered from unordered containers
    # so we need to just list them out manually as needed
    
    type_info = collections.namedtuple('type_info', 'type transformation aggregator')
    ident = lambda x: x
    # order matters; first match is used to handle a datatype
    known_types = (
        type_info(dict, lambda d: d.items(), frozenset), # also handles defaultdict
        type_info(collections.OrderedDict, ident, tuple),
        type_info(tuple, ident, tuple),
        type_info(list, ident, tuple),
        type_info(collections.deque, ident, tuple),
        type_info(collections.Iterable, ident, frozenset) # other iterables
    )
    
    # hash_func can be set to replace the built-in hash function
    # cache can be turned on; if it is, cycles will be detected,
    # otherwise cycles in a data structure will cause failure
    def __init__(self, data, hash_func=hash, cache=False, verbose=False):
        self._data=data
        self.hash_func=hash_func
        self.verbose=verbose
        self.cache=cache
        # cache objects' hashes for performance and to deal with cycles
        if self.cache:
            self.seen={}
    
    def hash_ex(self, o):
        # note: isinstance(o, Hashable) won't check inner types
        try:
            if self.verbose:
                print(type(o), reprlib.repr(o), self.hash_func(o), file=sys.stderr)
            return self.hash_func(o)
        except TypeError:
            pass
    
        # we let built-in hash decide if the hash value is worth caching
        # so we don't cache the built-in hash results
        if self.cache and id(o) in self.seen:
            return self.seen[id(o)][0] # found in cache
        
        # check if o can be handled by decomposing it into components
        for typ, transformation, aggregator in AutoHash.known_types:
            if isinstance(o, typ):
                # another option is:
                # result = reduce(operator.xor, map(_hash_ex, handler(o)))
                # but collisions are more likely with xor than with frozenset
                # e.g. hash_ex([1,2,3,4])==0 with xor
                
                try:
                    # try to frozenset the actual components, it's faster
                    h = self.hash_func(aggregator(transformation(o)))
                except TypeError:
                    # components not hashable with built-in;
                    # apply our extended hash function to them
                    h = self.hash_func(aggregator(map(self.hash_ex, transformation(o))))
                if self.cache:
                    # storing the object too, otherwise memory location will be reused
                    self.seen[id(o)] = (h, o)
                if self.verbose:
                    print(type(o), reprlib.repr(o), h, file=sys.stderr)
                return h

        raise TypeError('Object {} of type {} not hashable'.format(repr(o), type(o)))
    
    def __hash__(self):
        return self.hash_ex(self._data)

    def __eq__(self, other):
        # short circuit to save time
        if self is other:
            return True
        
        # 1) type(self) a proper subclass of type(other) => self.__eq__ will be called first
        # 2) any other situation => lhs.__eq__ will be called first
        
        # case 1. one side is a subclass of the other, and AutoHash.__eq__ is not overridden in either
        # => the subclass instance's __eq__ is called first, and we should compare self._data and other._data
        # case 2. neither side is a subclass of the other; self is lhs
        # => we can't compare to another type; we should let the other side decide what to do, return NotImplemented
        # case 3. neither side is a subclass of the other; self is rhs
        # => we can't compare to another type, and the other side already tried and failed;
        # we should return False, but NotImplemented will have the same effect
        # any other case: we won't reach the __eq__ code in this class, no need to worry about it
        
        if isinstance(self, type(other)): # identifies case 1
            return self._data == other._data
        else: # identifies cases 2 and 3
            return NotImplemented
    
if __name__ == '__main__':
    d = {'a':[1,2], 2:{3:4}, frozenset((1,2,3)):5, frozenset((5,6)): {5,6}}
    d = AutoHash(d, verbose=True, cache=True)
    print(hash(d))
