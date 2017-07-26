from collections import namedtuple
from functools import wraps

_CacheInfo = namedtuple("CacheInfo", "hits misses maxsize currsize")

def cache():
    """Memoizing cache decorator.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits, misses maxsize, size) with
    f.cache_info().  Clear the cache and statistics with f.cache_clear().

    """

    def decorating_function(user_function,
                tuple=tuple, sorted=sorted, len=len, KeyError=KeyError):

        cache = dict()
        hits = misses = 0
        kwd_mark = object()             # separates positional and keyword args

        @wraps(user_function)
        def wrapper(*args, **kwds):
            nonlocal hits, misses
            key = args
            if kwds:
                key += (kwd_mark,) + tuple(sorted(kwds.items()))
            try:
                result = cache[key]
                hits += 1
            except KeyError:
                result = user_function(*args, **kwds)
                cache[key] = result
                misses += 1
            return result

        def cache_info():
            """Report cache statistics"""
            return _CacheInfo(hits, misses, None, len(cache))

        def cache_clear():
            """Clear the cache and cache statistics"""
            nonlocal hits, misses
            cache.clear()
            hits = misses = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper

    return decorating_function


# ----- Example ----------------------------------------------------------------

if __name__ == '__main__':

    @cache()
    def fib(n):
        if n < 2:
            return 1
        return fib(n-1) + fib(n-2)

    from random import shuffle
    inputs = list(range(30))
    shuffle(inputs)
    results = sorted(fib(n) for n in inputs)
    print(results)
    print(fib.cache_info())
        
    expected_output = '''[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 
         233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 
         46368, 75025, 121393, 196418, 317811, 514229, 832040]
         CacheInfo(hits=56, misses=30, maxsize=None, currsize=30)
    '''
