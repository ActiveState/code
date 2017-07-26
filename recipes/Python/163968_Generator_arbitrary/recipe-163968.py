def peel(iterable, arg_cnt=1):
    """Use ``iterable`` to return ``arg_cnt`` number of arguments
    plus the iterator itself.

    """
    iterator = iter(iterable)
    for num in xrange(arg_cnt):
        yield iterator.next()
    yield iterator
