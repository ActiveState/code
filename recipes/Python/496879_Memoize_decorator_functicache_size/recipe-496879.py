import cPickle

__all__ = ["memoize"]

def memoize(function, limit=None):
    if isinstance(function, int):
        def memoize_wrapper(f):
            return memoize(f, function)

        return memoize_wrapper

    dict = {}
    list = []
    def memoize_wrapper(*args, **kwargs):
        key = cPickle.dumps((args, kwargs))
        try:
            list.append(list.pop(list.index(key)))
        except ValueError:
            dict[key] = function(*args, **kwargs)
            list.append(key)
            if limit is not None and len(list) > limit:
                del dict[list.pop(0)]

        return dict[key]

    memoize_wrapper._memoize_dict = dict
    memoize_wrapper._memoize_list = list
    memoize_wrapper._memoize_limit = limit
    memoize_wrapper._memoize_origfunc = function
    memoize_wrapper.func_name = function.func_name
    return memoize_wrapper

# Example usage
if __name__ == "__main__":
    # Will cache up to 100 items, dropping the least recently used if
    # the limit is exceeded.
    @memoize(100)
    def fibo(n):
        if n > 1:
            return fibo(n - 1) + fibo(n - 2)
        else:
            return n

    # Same as above, but with no limit on cache size
    @memoize
    def fibonl(n):
        if n > 1:
            return fibo(n - 1) + fibo(n - 2)
        else:
            return n
