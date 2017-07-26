import operator


class Set(set):
    def __mul__(self, other):
        if not isinstance(other, set):
            return NotImplemented
        return Set(self._join_elements(x, y) for x in self for y in other)

    def __pow__(self, amount):
        if not isinstance(amount, int):
            return NotImplemented
        return reduce(operator.mul, (self for _ in xrange(amount)))

    def _join_elements(self, x, y):
        if not isinstance(x, tuple):
            x = (x,)
        if not isinstance(y, tuple):
            y = (y,)
        return x + y

    def __repr__(self):
        s = set.__repr__(self)
        return '%s(%s' % (self.__class__.__name__, s.split('(', 1)[1])


def main():
    # binary numbers of 3 bits
    s = Set([0, 1])
    print s ** 3

if __name__ == '__main__':
    main()
 
