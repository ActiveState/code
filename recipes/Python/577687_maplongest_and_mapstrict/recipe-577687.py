from itertools import zip_longest

def map_longest(func, *iterables, fillvalue=None):
    for t in zip_longest(*iterables, fillvalue=fillvalue):
        yield func(*t)

def map_strict(func, *iterables, exception=None):
    sentinel = object()
    for t in zip_longest(*iterables, fillvalue=sentinel):
        if sentinel in t:
            if exception is None:
                exception = ValueError('too few items in iterable')
            raise exception
        yield func(*t)
