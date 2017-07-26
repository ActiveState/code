class CompactSet:

    def __init__(self, numbers = None, bits = None):
        self.bits = bits or 0       
        if numbers:
            for n in numbers:
                self.add(n)

    def add(self, n):
        self.bits |= 1 << n

    def remove(self, n):
        self.bits &= ~(1 << n)

    def clear(self):
        self.bits = 0

    def union(self, other):
        return CompactSet(bits = self.bits | other.bits)

    __or__ = union

    def intersection(self, other):
        return CompactSet(bits = self.bits & other.bits)

    __and__ = intersection

    def difference(self, other):
        return CompactSet(bits = self.bits & ~other.bits)

    __sub__ = difference
    
    def union_update(self, other):
        self.bits |= other.bits

    def intersection_update(self, other):
        self.bits &= other.bits

    def difference_update(self, other):
        self.bits &= ~other.bits

    def numbers(self):
        return list(self)

    def isdisjoint(self, other):
        return not (self.bits & other.bits)
    
    def __eq__(self, other):
        return (self.bits == other.bits)

    def __ne__(self, other):
        return not (self == other)

    def issubset(self, other):
        return (self.bits | other.bits == other.bits)

    __le__ = issubset

    def issuperset(self, other):
        return (other <= self)

    __ge__ = issuperset
    
    def __lt__(self, other):
        return (self <= other and self != other)

    def __gt__(self, other):
        return (other < self)

    def __len__(self):
        bits = self.bits
        count = 0
        while bits:
            bits &= bits - 1
            count += 1
        return count
        
    def __contains__(self, n):
        return self.bits & (1 << n)

    def __iter__(self):
        if self.bits == 0:
            raise StopIteration
        mask = 1
        for n in range(self.bits.bit_length()):
            if self.bits & mask:
                yield n
            mask <<= 1
        
    def __repr__(self):
        return ''.join(["CompactSet(", str(self.numbers()), ")"])


if __name__ == '__main__':

    s = CompactSet([3, 7, 10])
    t = CompactSet([5, 2, 3])

    assert 7 in s
    assert s & t
    assert s | t == CompactSet([2, 3, 5, 7, 10])

    s.remove(3)
    assert not s & t

    assert CompactSet([2, 3]) < t

    print 'OK'
    

    import sys
    
    s = set(xrange(10000))
    cs = CompactSet(xrange(10000))
    print 'Size of set(xrange(10000)) is ', sys.getsizeof(s) # this is actually underestimated
    print 'Size of CompactSet(xrange(10000)) is ', sys.getsizeof(cs.bits)
