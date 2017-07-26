# Example:
# >>> nest(range(12),[2,2,3])
# [[[0, 1, 2], [3, 4, 5]], [[6, 7, 8], [9, 10, 11]]]

def nest(flat,levels):
    '''Turn a flat list into a nested list, with a specified number of lists per nesting level.
    Excess elements are silently ignored.'''
    return _nest(flat,levels).next()

def _nest(flat,levels):
    if levels:
        it = _nest(flat,levels[1:])
        while 1:
            yield list(itertools.islice(it,levels[0]))
    else:
        for d in flat:
            yield d
