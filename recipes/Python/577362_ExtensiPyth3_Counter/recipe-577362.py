import collections

class Counter(collections.Counter):

    def __xor__(self, other):
        ''' Subtract count, but keep only abs results with non-zero counts.

        >>> Counter('abbbc') ^ Counter('bccd')
        Counter({'b': 2, 'a': 1, 'c': 1, 'd': 1})
        >>> a, b = Counter('abbbc'), Counter('bccd')
        >>> (a-b) + (b - a) == a ^ b
        True

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount != 0:
                result[elem] = newcount if newcount > 0 else -newcount
        return result

    def __mul__(self, other):
        '''Multiply counts by an integer; or cartesioan product
        of two counters.

        >>> Counter('abbb') * 3
        Counter({'b': 9, 'a': 3})
        >>> Counter('12') * Counter('21')
        Counter({('2', '1'): 1, ('1', '2'): 1, ('1', '1'): 1, ('2', '2'): 1})
        >>> Counter('122') * Counter('211')
        Counter({('2', '1'): 4, ('1', '1'): 2, ('2', '2'): 2, ('1', '2'): 1})
        '''
        if isinstance(other, int):
            return Counter(**dict((k, v*other)
                                  for k,v in self.items()))
        elif isinstance(other, Counter):
            return Counter( (x, y)
                            for x in self.elements()
                            for y in other.elements() )
        else:
            return NotImplemented

    def __rmul__(self, other):
        '''Multiply counts by an integer; or cartesioan product
        of two counters.

        >>> 3 * Counter('abbb')
        Counter({'b': 9, 'a': 3, 'c': 3})
        '''
        return self.__mul__(other)
