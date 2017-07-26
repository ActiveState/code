from collections import deque


class BrowserHistory(object):
    '''Class for keeping track of the history while moving to different locations,
    as implemented in Web browsers.
    
    Both back and forward history are supported and each of them can be bounded
    or unbounded.
        
    >>> h = BrowserHistory(max_back=3, max_forward=3)
    >>> h.location = 'http://www.google.com/'
    >>> h.location = 'http://www.python.org/'
    >>> h.location = 'http://xkcd.com/'
    >>> h.location = 'http://www.slashdot.org/'
    >>> h.location = 'http://www.digg.com/'    
    >>> h.back()
    'http://www.slashdot.org/'
    >>> h.forward()
    'http://www.digg.com/'
    >>> h.go(-2)
    'http://xkcd.com/'
    >>> # max_back=3 so any result more than 3 pages back is deleted
    >>> for i_loc in h.indexed_locations():
    ...     print '%+d: %s' % i_loc
    +2: http://www.digg.com/
    +1: http://www.slashdot.org/
    +0: http://xkcd.com/
    -1: http://www.python.org/
    >>> # visiting a new location erases the forward history
    >>> h.location = 'http://en.wikipedia.org/'
    >>> for i_loc in h.indexed_locations():
    ...     print '%+d: %s' % i_loc
    +0: http://en.wikipedia.org/
    -1: http://xkcd.com/
    -2: http://www.python.org/
    '''
    
    def __init__(self, location=None, max_back=None, max_forward=None):
        '''Initialize a new BrowserHistory instance.
        
        :param location: If not None, the initial location.
        :param max_back: The maximum number of back locations to remember
            (default: no limit)
        :param max_forward: The maximum number of forward locations to remember
            (default: no limit)
        '''
        if max_back is not None:
            max_back += 1   # +1 for storing the current location
        self._back = deque(maxlen=max_back)
        self._forward = deque(maxlen=max_forward)
        if location is not None:
            self.location = location
    
    @property
    def location(self):
        '''The current location, i.e. the last location set or went to by
        :meth:`back`, :meth:`forward` or :meth:`go`.
        '''
        if self._back:
            return self._back[-1]
        raise AttributeError('location has not been set')

    @location.setter
    def location(self, value):
        '''Go to a new location. Any existing forward history is erased.'''
        self._back.append(value)
        self._forward.clear()
    
    def back(self, i=1):
        '''Jump to a location in history ``i`` steps back.
        
        :param i: The number of steps to jump back.
        :type i: positive int
        :returns: The current :attr:`location`.
        '''
        if i > 0:
            push_forward = self._forward.appendleft
            pop_back = self._back.pop
            for _ in xrange(min(i, len(self._back)-1)):
                push_forward(pop_back())
        return self.location

    def forward(self, i=1):
        '''Jump to a location in history ``i`` steps forward.
        
        :param i: The number of steps to jump forward.
        :type i: positive int
        :returns: The current :attr:`location`.
        '''
        if i > 0:
            push_back = self._back.append
            pop_forward = self._forward.popleft
            for _ in xrange(min(i, len(self._forward))):
                push_back(pop_forward())
        return self.location    

    def go(self, i):
        '''Jump to a location in history ``i`` steps back or forward.
        
        :param i: The number of steps to jump forward (if positive) or back (if negative).
        :type i: int
        :returns: The current :attr:`location`.
        '''
        if i < 0:
            return self.back(-i)
        if i > 0:
            return self.forward(i)
        return self.location

    def indexed_locations(self):
        '''Return a list of ``(index,location)`` tuples for each location in history.
        
        The index ``i`` of a location ``l`` is defined so that ``go(i) == l``.
        Therefore indexes are positive for forward locations, negative for back
        locations and zero for the current :attr:`location`.
        '''
        result = []
        # back and current locations
        n = len(self._back)-1
        result.extend((i-n, location) for i,location in enumerate(self._back))
        # forward locations
        result.extend((i+1, location) for i,location in enumerate(self._forward))
        result.reverse()
        return result


if __name__ == '__main__':
    import doctest; doctest.testmod()
