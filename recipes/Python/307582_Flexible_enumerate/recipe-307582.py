from itertools import izip, count

def enumerate(a, b=None):
    "enumerate([start,] iterable)"
    if b is None:
        start, iterable = 0, a
    else:
        start, iterable = a, b
    return izip(count(start), iterable)
