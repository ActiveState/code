from cPickle import dumps, PicklingError # for memoize


class memoize(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated. Slow for mutable types."""
    # Ideas from MemoizeMutable class of Recipe 52201 by Paul Moore and
    # from memoized decorator of http://wiki.python.org/moin/PythonDecoratorLibrary
    # For a version with timeout see Recipe 325905
    # For a self cleaning version see Recipe 440678
    # Weak references (a dict with weak values) can be used, like this:
    #   self._cache = weakref.WeakValueDictionary()
    #   but the keys of such dict can't be int
    def __init__(self, func):
        self.func = func
        self._cache = {}
    def __call__(self, *args, **kwds):
        key = args
        if kwds:
            items = kwds.items()
            items.sort()
            key = key + tuple(items)
        try:
            if key in self._cache:
                return self._cache[key]
            self._cache[key] = result = self.func(*args, **kwds)
            return result
        except TypeError:
            try:
                dump = dumps(key)
            except PicklingError:
                return self.func(*args, **kwds)
            else:
                if dump in self._cache:
                    return self._cache[dump]
                self._cache[dump] = result = self.func(*args, **kwds)
                return result


if __name__ == "__main__": # Some examples
    @memoize
    def fibonacci(n):
       "Return the n-th element of the Fibonacci series."
       if n < 3:
          return 1
       return fibonacci(n-1) + fibonacci(n-2)

    print [fibonacci(i) for i in xrange(1, 101)]

    @memoize
    def pow(x, p=2):
        if p==1:
            return x
        else:
            return x * pow(x, p=p-1)

    print [pow(3, p=i) for i in xrange(1, 6)]

    @memoize
    def printlist(l):
        print l
    printlist([1,2,3,4])
