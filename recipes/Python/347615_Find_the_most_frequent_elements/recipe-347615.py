from operator import itemgetter
from heapq import nlargest

def mostcommon(iterable, n=None):
    """Return a sorted list of the most common to least common elements and
    their counts.  If n is specified, return only the n most common elements.

    """
    bag = {}
    bag_get = bag.get
    for elem in iterable:
        bag[elem] = bag_get(elem, 0) + 1
    if n is None:
        return sorted(bag.iteritems(), key=itemgetter(1), reverse=True)
    it = enumerate(bag.iteritems())
    nl = nlargest(n, ((cnt, i, elem) for (i, (elem, cnt)) in it))
    return [(elem, cnt) for cnt, i, elem in nl]

>>> mostcommon((word for line in open('in.txt') for word in line.split()), n=5)
[('to', 80), ('for', 75), ('the', 61), ('in', 57), ('of', 54)]
