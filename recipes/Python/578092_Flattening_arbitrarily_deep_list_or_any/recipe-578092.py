class iter2(object):
    '''Takes in an object that is iterable.  Allows for the following method
    calls (that should be built into iterators anyway...)
    calls:
        - append - appends another iterable onto the iterator.
        - insert - only accepts inserting at the 0 place, inserts an iterable
         before other iterables.
        - adding.  an iter2 object can be added to another object that is
         iterable.  i.e. iter2 + iter (not iter + iter2).  It's best to make
         all objects iter2 objects to avoid syntax errors.  :D
    '''
    def __init__(self, iterable):
        self._iter = iter(iterable)
    
    def append(self, iterable):
        self._iter = itertools.chain(self._iter, iter(iterable))
        
    def insert(self, place, iterable):
        if place != 0:
            raise ValueError('Can only insert at index of 0')
        self._iter = itertools.chain(iter(iterable), self._iter)
    
    def __add__(self, iterable):
        return itertools.chain(self._iter, iter(iterable))
        
    def next(self):
        return self._iter.next()
    
    def __iter__(self):
        return self

def flatten(iterable):
    '''flatten a list of any depth'''
    iterable = iter2(iterable)
    for e in iterable:
        if hasattr(e, '__iter__'):
            iterable.insert(0, e)
        else:
            yield e
