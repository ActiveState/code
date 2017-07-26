from heapq import nlargest as _nlargest, nsmallest as _nsmallest
from __builtin__ import min as _min, max as _max
from itertools import tee, izip, imap, count
from operator import itemgetter

__all__ = ['nsmallest', 'nlargest', 'min', 'max']

def nsmallest(n, iterable, key=None):
    """Find the n smallest elements in a dataset.

    Equivalent to:  sorted(iterable, key=key)[:n]
    """
    if key is None:
        return _nsmallest(n, iterable)
    in1, in2 = tee(iterable)
    it = izip(imap(key, in1), count(), in2)                 # decorate
    result = _nsmallest(n, it)
    return map(itemgetter(2), result)                       # undecorate

def nlargest(n, iterable, key=None):
    """Find the n largest elements in a dataset.

    Equivalent to:  sorted(iterable, key=key, reverse=True)[:n]
    """
    if key is None:
        return _nlargest(n, iterable)
    in1, in2 = tee(iterable)
    it = izip(imap(key, in1), count(), in2)                 # decorate
    result = _nlargest(n, it)
    return map(itemgetter(2), result)                       # undecorate


def min(iterable, key=None):
    if key is None:
        return _min(iterable)
    it = iter(iterable)
    try:
        min_elem = it.next()
    except StopIteration:
        raise ValueError('min() arg is an empty sequence')
    min_k = key(min_elem)
    for elem in it:
        k = key(elem)
        if k < min_k:
            min_elem = elem
            min_k = k
    return min_elem

def max(iterable, key=None):
    if key is None:
        return _max(iterable)
    it = iter(iterable)
    try:
        max_elem = it.next()
    except StopIteration:
        raise ValueError('max() arg is an empty sequence')
    max_k = key(max_elem)
    for elem in it:
        k = key(elem)
        if k > max_k:
            max_elem = elem
            max_k = k
    return max_elem
