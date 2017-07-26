#!/usr/bin/env python
""" Convenience methods for list comparison & manipulation

Fast and useful, set/frozenset* only retain unique values,
duplicates are automatically removed.

    lr_union    union
        merge values, remove duplicates

    lr_diff     difference
        left elements, subtracting any in common with right

    lr_intr     intersection
        only common values found in both left and right

    lr_symm     symmetric_difference
        omit values found in both left and right

    lr_cont     issuperset
        test left contains all values from right

    * Unlike set, frozenset preserves its own order and is
        immutable. They do not preserve the source-order.

"""

lr_union = lambda l, r: list(set(l).union(r))
lr_diff = lambda l, r: list(set(l).difference(r))
lr_intr = lambda l, r: list(set(l).intersection(r))
lr_symm = lambda l, r: list(set(l).symmetric_difference(r))
lr_cont = lambda l, r: set(l).issuperset(r)

# silent example of lr_intr if None is passed instead of list
lrq_intr = lambda l, r: list(set(l).intersection(r or []))

# ------------ NOTHING BELOW HERE IS REQUIRED --------------

def tests():
    """ doctest tests/examples for set and set conveniences

    A few examples without the conveniences above.

    Strings are a form of list, they can be passed where apropriate
    >>> set('aabbcc') # only unique are returned
    set(['a', 'c', 'b'])

    Do the work and cast as list (switch to tuple if prefered)
    >>> list(set('aabbcc'))
    ['a', 'c', 'b']

    Using list does not remove duplicates
    >>> list('aabbcc') # list is not unique
    ['a', 'a', 'b', 'b', 'c', 'c']

    Simple join of lists, note the redundant values
    >>> ['a', 'a', 'b'] + ['b', 'c', 'c']
    ['a', 'a', 'b', 'b', 'c', 'c']

    Join both lists, return only unique values, join list before set (slower)
    >>> list(set(['a', 'a', 'b'] + ['b', 'c', 'c']))
    ['a', 'c', 'b']

    Join lists, as above, using built-in set library (faster)
    >>> lr_union(['a', 'a', 'b'], ['b', 'c', 'c'])
    ['a', 'c', 'b']

    Remove right values from left
    >>> lr_diff(['a', 'b'], ['b', 'c'])
    ['a']

    Remove as above, swapped/reordered inputs to remove left from right
    >>> lr_diff(['b', 'c'], ['a', 'b'])
    ['c']

    Common elements
    >>> lr_intr(['a', 'b'], ['b', 'c'])
    ['b']

    Unique elements (remove the common, intersecting, values)
    Note: similar to left-right + right-left.
    >>> lr_symm(['a', 'b'], ['b', 'c'])
    ['a', 'c']

    Is left a superset of (does it contain) the right
    >>> lr_cont(['a', 'b'], ['b', 'c'])
    False
    >>> lr_cont(['a', 'b', 'c'], ['b', 'c'])
    True

    Marginally less trite examples using words
    >>> lwords = 'the quick brown fox'.split()
    >>> rtags = 'brown,fox,jumps,over'.split(',')

    Return all unique words from both lists.
    >>> lr_union(lwords,rtags)
    ['brown', 'over', 'fox', 'quick', 'the', 'jumps']

    Return unique common, intersecting, words. Members of left AND right only.
    >>> lr_intr(lwords,rtags)
    ['brown', 'fox']

    Return unique uncommon words. Members of left OR right
    >>> lr_symm(lwords,rtags)
    ['quick', 'the', 'jumps', 'over']

    Note: intersection + symmetric = union, but don't count on their order!

    """

def insecure_demo():
    """Compact method to demo functionality"""

    left, right = list('aab'), list('bcc')
    both = left + right
    both.sort()

    lamb_dict = {'Difference (Remainder of subtract: left - right)': 'lr_diff',
                'Intersection (Only in left AND right)': 'lr_intr',
                'Symmetric Difference (Only in left OR right)': 'lr_symm',
                'Union (Unique list of ALL values)': 'lr_union'}

    print "Demo methods for comparing lists using set/frozenset\n"
    print "'left' list: %s" % repr(left)
    print "'right' list: %s" % repr(right)
    print "'both' lists: %s\n" % repr(both)
    print '-' * 30

    for lamb_desc, lamb_name in lamb_dict.items():
        lamb_func = globals().get(lamb_name)
        resp = lamb_func(left, right)
        resp.sort()

        print lamb_desc #'Obtain the %s of two lists' % lamb_name.split('_')[-1]
        print '>>> %s(%r, %r)' % (lamb_name, left, right)
        print resp
        print '-' * 30

if __name__ == '__main__':

    import doctest
    doctest.testmod()

    insecure_demo()

    URL = 'http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset'
    print "\nBe sure to visit:\n", URL
