from itertools import chain, combinations

def partition(iterable, chain=chain, map=map):
    s = iterable if hasattr(iterable, '__getslice__') else tuple(iterable)
    n = len(s)
    first, middle, last = [0], range(1, n), [n]
    getslice = s.__getslice__
    return [map(getslice, chain(first, div), chain(div, last))
            for i in range(n) for div in combinations(middle, i)]


>>> from pprint import pprint
>>> pprint(partition('abcdef'))
[['abcdef'],
 ['a', 'bcdef'],
 ['ab', 'cdef'],
 ['abc', 'def'],
 ['abcd', 'ef'],
 ['abcde', 'f'],
 ['a', 'b', 'cdef'],
 ['a', 'bc', 'def'],
 ['a', 'bcd', 'ef'],
 ['a', 'bcde', 'f'],
 ['ab', 'c', 'def'],
 ['ab', 'cd', 'ef'],
 ['ab', 'cde', 'f'],
 ['abc', 'd', 'ef'],
 ['abc', 'de', 'f'],
 ['abcd', 'e', 'f'],
 ['a', 'b', 'c', 'def'],
 ['a', 'b', 'cd', 'ef'],
 ['a', 'b', 'cde', 'f'],
 ['a', 'bc', 'd', 'ef'],
 ['a', 'bc', 'de', 'f'],
 ['a', 'bcd', 'e', 'f'],
 ['ab', 'c', 'd', 'ef'],
 ['ab', 'c', 'de', 'f'],
 ['ab', 'cd', 'e', 'f'],
 ['abc', 'd', 'e', 'f'],
 ['a', 'b', 'c', 'd', 'ef'],
 ['a', 'b', 'c', 'de', 'f'],
 ['a', 'b', 'cd', 'e', 'f'],
 ['a', 'bc', 'd', 'e', 'f'],
 ['ab', 'c', 'd', 'e', 'f'],
 ['a', 'b', 'c', 'd', 'e', 'f']]
