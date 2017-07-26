from itertools import count


class indexediterator(object):
    # Helper class to be returned as the actual generator with
    # indexing; wraps the generator in an iterator that also
    # supports item retrieval by index.
    
    def __init__(self, gen):
        self.__gen = gen  # the generator that created us
        self.__iter = gen._iterable()
    
    def __iter__(self):
        # Return the generator function; note that we return
        # the same one each time, which matches the semantics
        # of actual generators (i.e., once the generator function
        # is called, iter(gen) returns the same iterator and does
        # not reset the state)
        return self.__iter
    
    def next(self):
        # Return next item from generator
        term = next(self.__iter)
        if term == self.__gen.sentinel:
            raise StopIteration
        return term
    
    def __len__(self):
        # If the generator is exhausted, we know its length, so
        # we can use that information; if not, we raise TypeError,
        # just like any other object with no length
        result = self.__gen._itemcount()
        if result is None:
            raise TypeError, "object of type %s has no len()" % \
                self.__class__.__name__
        return result
    
    def __getitem__(self, index):
        # Return the item at index, advancing the generator if
        # necessary; if the generator is exhausted before index,
        # raise IndexError, just like any other sequence when an
        # index out of range is requested
        result = self.__gen._retrieve(index)
        if result is self.__gen.sentinel:
            raise IndexError, "sequence index out of range"
        return result


class IndexedGenerator(object):
    """Make a generator indexable like a sequence.
    """
    
    sentinel = object()
    
    def __init__(self, gen):
        # The underlying generator
        self.__gen = gen
        # Memoization fields
        self.__cache = []
        self.__iter = None
        self.__empty = False
    
    def _retrieve(self, n):
        # Retrieve the nth item from the generator, advancing
        # it if necessary
        
        # Negative indexes are invalid unless the generator
        # is exhausted, so check that first
        if n < 0:
            end = self._itemcount()
            if (end is None) or (end == 0):
                # No length known yet, or no items at all
                return self.sentinel
            else:
                return self.__cache[end + n]
        # Now try to advance the generator (which may empty it,
        # or it may already be empty)
        while (not self.__empty) and (n >= len(self.__cache)):
            try:
                term = next(self.__iter)
            except StopIteration:
                self.__empty = True
            else:
                self.__cache.append(term)
        if n < len(self.__cache):
            return self.__cache[n]
        return self.sentinel
    
    def _iterable(self):
        # Yield terms from the generator
        for n in count():
            term = self._retrieve(n)
            if term is self.sentinel:
                break
            yield term
    
    def _itemcount(self):
        # Once we are exhausted, the number of items in the
        # sequence is known, so we can provide it; otherwise
        # we return None
        if self.__empty:
            return len(self.__cache)
        return None
    
    def __call__(self, *args, **kwargs):
        """Make instances of this class callable.
        
        This method must be present, and must be a generator
        function, so that class instances work the same as their
        underlying generators.
        """
        if not (self.__empty or self.__iter):
            self.__iter = self.__gen(*args, **kwargs)
        return indexediterator(self)


# This creates a decorator that works if applied to a method
# (the above will only work on an ordinary generator function)
# -- requires the Delayed Decorator recipe at
# http://code.activestate.com/recipes/577993-delayed-decorator/
indexable_generator = partial(DelayedDecorator, IndexedGenerator)
