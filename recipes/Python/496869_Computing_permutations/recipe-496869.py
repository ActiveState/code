"""
Compute permutations.
"""

def permute_next(values):
    """
    Alter the list of values in-place to produce to the next permutation
    in lexicographical order.
    
    'values' must support slicing and ::reverse().
    """
    last = len(values) - 1
    a = last
    while a > 0:
        b = a
        a -= 1
        if values[a] < values[b]:
            c = last
            while values[a] >= values[c]: # >= allows duplicates
                c -= 1
            values[a], values[c] = values[c], values[a] # Swap.
            values[b:] = values[:b-1:-1] # Reverse.
            return
    values.reverse()

def permute_prev(values):
    """
    Alter the list of values in-place to produce to the previous permutation
    in lexicographical order.
    
    'values' must support slicing and ::reverse().
    """
    last = len(values) - 1
    a = last
    while a > 0:
        b = a
        a -= 1
        if values[a] > values[b]:
            c = last
            while values[a] <= values[c]: # <= allows duplicates
                c -= 1
            values[a], values[c] = values[c], values[a] # Swap.
            values[b:] = values[:b-1:-1] # Reverse.
            return
    values.reverse()

import unittest
class PermutationTests(unittest.TestCase):
    def count(self, orig, expect):
        values = orig[:]
        seen = []
        while values not in seen:
            seen.append(values[:])
            permute_next(values)
        self.failUnless(list(reversed(orig)) in seen)
        self.failUnless(list(sorted(orig)) in seen)
        self.failUnless(list(reversed(sorted(orig))) in seen)
        values.sort()
        start = seen.index(values)
        for _ in range(len(orig)+1):
            current = values[:]
            permute_next(values)
            self.failUnless( current < values or values == seen[start] )
        for _ in range(len(orig)+1):
            current = values[:]
            permute_prev(values)
            self.failUnless( current > values or current == seen[start] )
        self.assertEqual(expect, len(seen))
     def test0(self):
        self.count( [], 1 )
    def test1(self):
        self.count( [42], 1 )
    def test2(self):
        self.count( [1,1], 1 )
        self.count( [1,2], 2 )
        self.count( [2,1], 2 )
    def test3(self):
        self.count( range(3), 6 )
        self.count( range(3,0,-1), 6 )
        self.count( [1,1,1], 1 )
        self.count( [1,1,2], 3 )
        self.count( [1,2,1], 3 )
        self.count( [2,1,1], 3 )
        self.count( [1,2,2], 3 )
        self.count( [2,1,2], 3 )
        self.count( [2,2,1], 3 )
    def test4(self):
        self.count( range(4), 24 )
        self.count( range(4,0,-1), 24 )
        self.count( [1,1,1,1], 1 )
        self.count( [1,1,1,2], 4 )
        self.count( [1,1,2,1], 4 )
        self.count( [1,2,1,1], 4 )
        self.count( [2,1,1,1], 4 )
        self.count( [1,2,2,2], 4 )
        self.count( [2,1,2,2], 4 )
        self.count( [2,2,1,2], 4 )
        self.count( [2,2,2,1], 4 )
        self.count( [1,1,2,2], 6 )
        self.count( [1,2,2,1], 6 )
        self.count( [2,2,1,1], 6 )
        self.count( [2,1,1,2], 6 )
        self.count( [1,2,1,2], 6 )
        self.count( [2,1,2,1], 6 )
    def test5(self):
        self.count( ['c', 'a', 'a', 'a', 'c', 'd', 'd'], 210 )

def _test():
    unittest.main()

def run(values):
    seen = []
    while values not in seen:
        print values
        seen.append(values[:])
        permute_prev(values)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] x y z ...',
                            description='Show all permutations.')
    parser.add_option('-t', '--test', action='store_true', help='Run tests.')
    opts, extras = parser.parse_args()
    if opts.test:
        import sys
        sys.argv[1:] = extras
        _test()
    try:
        run(map(int, extras))
    except ValueError:
        run(extras)
