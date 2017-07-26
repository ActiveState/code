def irange(start, stop=None, step=None):
    '''Return a range - as iterator.'''
    if stop == None:
        start, stop = 0, start
    if stop > start:
        _comp = lambda x, y: x <= y
        step = step or 1
    else:
        _comp = lambda x, y: x >= y
        step = step or -1
    if _comp(step, 0): # Safeguard: Wrong way => empty range
        raise StopIteration
    while _comp(start, stop):
        yield start
        start += step
