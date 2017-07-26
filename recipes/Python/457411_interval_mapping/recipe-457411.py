from bisect import bisect_left, bisect_right
from itertools import izip

class intervalmap(object):
    """
        This class maps a set of intervals to a set of values.
        
        >>> i = intervalmap()
        >>> i[0:5] = '0-5'
        >>> i[8:12] = '8-12'
        >>> print i[2]
        0-5
        >>> print i[10]
        8-12
        >>> print repr(i[-1])
        None
        >>> print repr(i[17])
        None
        >>> i[4:9] = '4-9'
        >>> print [(j,i[j]) for j in range(6)]
        [(0, '0-5'), (1, '0-5'), (2, '0-5'), (3, '0-5'), (4, '4-9'), (5, '4-9')]
        >>> print list(i.items())
        [((0, 4), '0-5'), ((4, 9), '4-9'), ((9, 12), '8-12')]
        >>> i[:0] = 'less than 0'
        >>> i[-5]
        'less than 0'
        >>> i[0]
        '0-5'
        >>> print list(i.items())
        [((None, 0), 'less than 0'), ((0, 4), '0-5'), ((4, 9), '4-9'), ((9, 12), '8-12')]
        >>> i[21:] = 'more than twenty'
        >>> i[42]
        'more than twenty'
        >>> i[10.5:15.5] = '10.5-15.5'
        >>> i[11.5]
        '10.5-15.5'
        >>> i[0.5]
        '0-5'
        >>> print list(i.items())
        [((None, 0),... ((9, 10.5), '8-12'), ((10.5, 15.5), '10.5-15.5'), ((21, None),...
        >>> i = intervalmap()
        >>> i[0:2] = 1
        >>> i[2:8] = 2
        >>> i[4:] = 3
        >>> i[5:6] = 4  
        >>> i
        {[0, 2] => 1, [2, 4] => 2, [4, 5] => 3, [5, 6] => 4, [6, None] => 3}
    """

    def __init__(self):
        """
            Initializes an empty intervalmap.
        """
        self._bounds = []
        self._items = []
        self._upperitem = None
        
    def __setitem__(self,_slice,_value):
        """
            Sets an interval mapping.
        """
        assert isinstance(_slice,slice), 'The key must be a slice object'
    
        if _slice.start is None:
            start_point = -1
        else:
            start_point = bisect_left(self._bounds,_slice.start)
        
        if _slice.stop is None:
            end_point = -1
        else:
            end_point = bisect_left(self._bounds,_slice.stop)
        
        if start_point>=0:
            if start_point < len(self._bounds) and self._bounds[start_point]<_slice.start:
                start_point += 1 

            if end_point>=0:        
                self._bounds[start_point:end_point] = [_slice.start,_slice.stop]
                if start_point < len(self._items):
                    self._items[start_point:end_point] = [self._items[start_point],_value]
                else:
                    self._items[start_point:end_point] = [self._upperitem,_value]
            else:
                self._bounds[start_point:] = [_slice.start]
                if start_point < len(self._items):
                    self._items[start_point:] = [self._items[start_point],_value]
                else:
                    self._items[start_point:] = [self._upperitem]
                self._upperitem = _value
        else:
            if end_point>=0:
                self._bounds[:end_point] = [_slice.stop]
                self._items[:end_point] = [_value]
            else:
                self._bounds[:] = []
                self._items[:] = []
                self._upperitem = _value
    
    def __getitem__(self,_point):
        """
            Gets a value from the mapping.
        """
        assert not isinstance(_point,slice), 'The key cannot be a slice object'  
            
        index = bisect_right(self._bounds,_point)
        if index < len(self._bounds):
            return self._items[index]
        else:
            return self._upperitem

    def items(self):
        """
            Returns an iterator with each item being
            ((low_bound,high_bound), value). The items are returned
            in order.
        """
        previous_bound = None
        for b,v in izip(self._bounds,self._items):
            if v is not None:
                yield (previous_bound,b), v
            previous_bound = b
        if self._upperitem is not None:
            yield (previous_bound,None), self._upperitem

    def values(self):
        """
            Returns an iterator with each item being a stored value. The items
            are returned in order.
        """
        for v in self._items:
            if v is not None:
                yield v
        if self._upperitem is not None:
            yield self._upperitem

    def __repr__(self):
        s = []
        for b,v in self.items():
            if v is not None:
                s.append('[%r, %r] => %r'%(
                    b[0],
                    b[1],
                    v
                ))
        return '{'+', '.join(s)+'}'
        
if __name__ == "__main__":
    # Test 1
    i = intervalmap()
    i[9:] = "!"
    assert repr(i) == "{[9, None] => '!'}"
    i[:5] = "Hello"
    i[6:7] = "World"
    assert repr(i) == "{[None, 5] => 'Hello', [6, 7] => 'World', [9, None] => '!'}"
    i[8:10] = "(Test)"
    assert repr(i) == "{[None, 5] => 'Hello', [6, 7] => 'World', [8, 10] => '(Test)', [10, None] => '!'}"
    i[:3] = 'My,'
    assert repr(i) == "{[None, 3] => 'My,', [3, 5] => 'Hello', [6, 7] => 'World', [8, 10] => '(Test)', [10, None] => '!'}"
    i[5.5:6] = "Cruel"
    assert repr(i) == "{[None, 3] => 'My,', [3, 5] => 'Hello', [5.5, 6] => 'Cruel', [6, 7] => 'World', [8, 10] => '(Test)', [10, None] => '!'}"
    i[6:6.5] = "And Harsh"
    assert repr(i) == "{[None, 3] => 'My,', [3, 5] => 'Hello', [5.5, 6] => 'Cruel', [6, 6.5] => 'And Harsh', [6.5, 7] => 'World', [8, 10] => '(Test)', [10, None] => '!'}"
    i[5.9:6.6] = None
    assert repr(i) == "{[None, 3] => 'My,', [3, 5] => 'Hello', [5.5, 5.9000000000000004] => 'Cruel', [6.5999999999999996, 7] => 'World', [8, 10] => '(Test)', [10, None] => '!'}"
    assert ' '.join(i.values()) == "My, Hello Cruel World (Test) !"
    print 'Test 1 OK'

    # Test 2
    i = intervalmap()
    i[:0] = 'A'
    i[2:5] = 'B'
    i[8:10] = 'C'
    i[12:] = 'D'
    assert repr(i) == "{[None, 0] => 'A', [2, 5] => 'B', [8, 10] => 'C', [12, None] => 'D'}"
    i[:] = 'K'
    assert repr(i) == "{[None, None] => 'K'}"
    assert i[5] == 'K'
    i[0:10] = 'L'
    i[6:8] = 'M'
    i[20:] = 'J'
    assert i[-1] == 'K'
    assert i[5] == 'L'
    assert i[7] == 'M'
    assert i[9] == 'L'
    assert i[15] == 'K'
    assert i[42] == 'J'
    print 'Test 2 OK'
    
    # Test 3
    try:
        from datetime import datetime
    except:
        print 'Test 3 skipped'
    else:
        i = intervalmap()
        i[:datetime(2005,10,24)] = 'A'
        i[datetime(2005,11,11):datetime(2005,11,17)] = 'B'
        i[datetime(2005,11,30):] = 'C'
        assert i[datetime(2005,9,25)] == 'A'
        assert i[datetime(2005,10,23)] == 'A'
        assert i[datetime(2005,10,26)] == None
        assert i[datetime(2005,11,9)] == None
        assert i[datetime(2005,11,16)] == 'B'
        assert i[datetime(2005,11,23)] == None
        assert i[datetime(2005,11,29)] == None
        assert i[datetime(2005,11,30)] == 'C'
        assert i[datetime(2005,12,3)] == 'C'
        print 'Test 3 OK'

    try:
        import doctest
    except:
        print 'Skipping the doctests'
    else:
        print 'And now, the doctests'    
        doctest.testmod(optionflags=doctest.ELLIPSIS)
