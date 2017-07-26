NOTATION10 = '0123456789'
NOTATION70 = "!'()*-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz~"

class BaseConvert:
    def __init__(self):
        self.notation = NOTATION10

    def _convert(self, n=1, b=10):
        '''
        Private function for doing conversions; returns a list
        '''
        if True not in [ isinstance(n, x) for x in [long, int, float] ]:
            raise TypeError, 'parameters must be numbers'
        converted = []
        quotient, remainder = divmod(n, b)
        converted.append(remainder)
        if quotient != 0:
            converted.extend(self._convert(quotient, b))
        return converted

    def convert(self, n, b):
        '''
        General conversion function
        '''
        nums = self._convert(n, b)
        nums.reverse()
        return self.getNotation(nums)

    def getNotation(self, list_of_remainders):
        '''
        Get the notational representation of the converted number
        '''
        return ''.join([ self.notation[x] for x in list_of_remainders ])

class Base70(BaseConvert):
    '''
    >>> base = Base70()
    >>> base.convert(10)
    '4'
    >>> base.convert(510)
    '1E'
    >>> base.convert(1000)
    '8E'
    >>> base.convert(10000000)
    'N4o4'
    '''
    def __init__(self):
        self.notation = NOTATION70

    def convert(self, n):
        "Convert base 10 to base 70"
        return BaseConvert.convert(self, n, 70)

def _test():
    import doctest, base
    return doctest.testmod(base)

if __name__ == '__main__':
    _test()
