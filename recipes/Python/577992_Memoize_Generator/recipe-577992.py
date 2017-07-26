from functools import partial
from itertools import count

class MemoizedGenerator(object):
    """Memoize a generator to avoid computing any term more than once.
    """
    
    def __init__(self, gen):
        # The underlying generator
        self.__gen = gen
        # Memoization fields
        self.__cache = []
        self.__iter = None
        self.__empty = False
    
    def __call__(self, *args, **kwargs):
        """Make instances of this class callable.
        
        This method must be present, and must be a generator
        function, so that class instances work the same as their
        underlying generators.
        """
        if not (self.__empty or self.__iter):
            self.__iter = self.__gen(*args, **kwargs)
        for n in count():
            # First check the cache
            if n < len(self.__cache):
                yield self.__cache[n]
            # See if another copy of the generator emptied it
            # since our last iteration
            elif self.__empty:
                break
            # If none of the above, advance the generator
            # (which may empty it)
            else:
                try:
                    term = next(self.__iter)
                except StopIteration:
                    self.__empty = True
                    break
                else:
                    self.__cache.append(term)
                    yield term


# This creates a decorator that works if applied to a method
# (the above will only work on an ordinary generator function)
# -- requires the Delayed Decorator recipe at
# http://code.activestate.com/recipes/577993-delayed-decorator/
memoize_generator = partial(DelayedDecorator, MemoizedGenerator)
