import operator

def factorial(n):
    """Calculate n factorial"""
    return reduce(operator.mul, range(2, n+1), 1)

def intersection(*sets):
    """Get the intersection of all input sets"""
    return reduce(set.intersection, sets)

def union(*sets):
    """Get the union of all input sets"""
    return reduce(set.union, sets)

def join(*seqs):
    """Join any input sequences that support concatenation"""
    return reduce(operator.concat, seqs)

"""
Some usage:
    
>>> factorial(3)
6

>>> factorial(10)
3628800

>>> a = set([1, 2, 3, 4, 5])
>>> b = set([5, 6, 3, 7])
>>> c = set([8, 7, 5])
>>> intersection(a, b, c)
set([5])

>>> union(a, b, c)
set([1, 2, 3, 4, 5, 6, 7, 8])

>>> join("one", "two", "three", "four")
'onetwothreefour'

>>> join([1, 2, 3], [5, 6], [6, 7])
[1, 2, 3, 4, 5, 6, 7]
"""
