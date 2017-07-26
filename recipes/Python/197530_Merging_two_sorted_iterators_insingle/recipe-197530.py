#!/usr/bin/env python

"""An extended example of generators in action.  Provides a function
called mergeiter that merges two iterators together.

Danny Yoo (dyoo@hkn.eecs.berkeley.edu)
"""


from __future__ import generators


def mergeiter(i1, i2, cmp=cmp):
    """Returns the "merge" of i1 and i2.  i1 and i2 must be iteratable
    objects, and we assume that i1 and i2 are both individually sorted.
    """
    left, right = ExtendedIter(i1), ExtendedIter(i2)
    while 1:
        if not left.has_next():
            while 1: yield ('r', right.next())
        if not right.has_next():
            while 1: yield ('l', left.next())
        comparison = cmp(left.peek(), right.peek())
        if comparison < 0:
            yield ('l', left.next())
        elif comparison == 0:
            right.next() ; yield ('=', left.next())
        else:
            yield ('r', right.next())


class ExtendedIter:
    """An extended iterator that wraps around an existing iterators.
    It provides extra methods:

        has_next(): checks if we can still yield items.

        peek(): returns the next element of our iterator, but doesn't
                pass by it."""
    def __init__(self, i):
        self._myiter = iter(i)
        self._next_element = None
        self._has_next = 0
        self._prime()


    def has_next(self):
        """Returns true if we can call next() without raising a
        StopException."""
        return self._has_next


    def peek(self):
        """Nonexhaustively returns the next element in our iterator."""
        assert self.has_next()
        return self._next_element


    def next(self):
        """Returns the next element in our iterator."""
        if not self._has_next:
            raise StopIteration
        result = self._next_element
        self._prime()
        return result


    def _prime(self):
        """Private function to initialize the states of
        self._next_element and self._has_next.  We poke our
        self._myiter to see if it's still alive and kicking."""
        try:
            self._next_element = self._myiter.next()
            self._has_next = 1
        except StopIteration:
            self.next_element = None
            self._has_next = 0




def _test():
    for item in mergeiter([2, 4, 6, 8], [1, 3, 4, 7, 9, 10]):
        print item


if __name__ == '__main__':
    ##  _test()
    import sys
    f1, f2 = open(sys.argv[1]), open(sys.argv[2])
    for item in mergeiter(f1, f2):
        print item
