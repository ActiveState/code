""" Two-pass pairing heap with multipass auxiliary list

This recipe adds a multipass auxiliary list to Tim Peter's code
for a two-pass pairing heap presented at:

    http://mail.python.org/pipermail/python-dev/2002-August/027531.html

The refinement produces a more balanced initial heap when fed with
random data.  This results in fewer comparisons than the basic
two-pass heap.  Details, analysis, and diagrams can be found at:

    http://www.cise.ufl.edu/~sahni/dsaaj/enrich/c13/pairing.htm

For random data, this implementation still makes more comparisons than
a sort using heapq or the builtin sort.  For partially ordered data, it
can perform better than the builtin sort.  Because of the list of lists
data structure, it always takes more memory than either heapq or the
builtin sort.

"""

from collections import deque

def _link(x, y):
    if x[0] <= y[0]:
        x.append(y)
        return x
    else:
        y.append(x)
        return y

def _merge(x):
    n = len(x)
    if n == 1:
        return []
    pairs = [_link(x[i], x[i+1]) for i in xrange(1, n-1, 2)]
    if n & 1 == 0:
        pairs.append(x[-1])
    pairs.reverse()
    x = pairs.pop()
    for i in pairs:
        x = _link(i, x)
    return x

class AuxList(deque):

    def multipass(self):
        while len(self) > 1:
            self.appendleft(_link(self.pop(), self.pop()))
        return self.pop()

class Heap:

    def __init__(self, iterable=[]):
        self.x = []
        self.aux = AuxList([[value] for value in iterable])

    def __nonzero__(self):
        return bool(self.x)

    def push(self, value):
        self.aux.append([value])

    def pop(self):
        if self.aux:
            self.x += self.aux.multipass()
        result = self.x[0]  # raises IndexError if empty
        self.x = _merge(self.x)
        return result

    def __getitem__(self, i):
        'Hack to make sorting as easy as:  list(Heap(input))'
        return self.pop()    

## Example call
>>> print list(Heap('abracadabra'))
['a', 'a', 'a', 'a', 'a', 'b', 'b', 'c', 'd', 'r', 'r']
