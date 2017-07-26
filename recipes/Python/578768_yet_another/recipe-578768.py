from itertools import chain, izip_longest

def roundrobin(*iterables):
    sentinel = object()
    return (x for x in chain(*izip_longest(fillvalue=sentinel, *iterables)) if x is not sentinel)
