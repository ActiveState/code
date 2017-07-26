from itertools import tee

class Iterator(object):
    """Intended to be used inside a while loop"""
    def __init__(self, iterable):
        self._a, self._b = tee(iter(iterable), 2)
        self._previous = None
        self._peeked   = self._b.next()
    
    def __iter__(self):
        return self
    
    def next(self):
        self._previous = self._a.next()
        self._current  = self._peeked
        try:
            self._peeked = self._b.next()
        except StopIteration:
            self._peeked = None
        return self._current
        
    def prev(self): return self._previous
    
    def peek(self): return self._peeked
