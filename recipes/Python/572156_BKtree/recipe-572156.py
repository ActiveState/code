"""
bktree.py, by bearophile

Fast Levenshtein distance and BK-tree implementations in Python.

The following functions are designed for Psyco, they are too much slow without it.
"""

def editDistance(s1, s2):
    """Computes the Levenshtein distance between two arrays (strings too).
    Such distance is the minimum number of operations needed to transform one array into
    the other, where an operation is an insertion, deletion, or substitution of a single
    item (like a char). This implementation (Wagner-Fischer algorithm with just 2 lines)
    uses O(min(|s1|, |s2|)) space.

    editDistance([], [])
    0
    >>> editDistance([1, 2, 3], [2, 3, 5])
    2
    >>> tests = [["", ""], ["a", ""], ["", "a"], ["a", "a"], ["x", "a"],
    ...          ["aa", ""], ["", "aa"], ["aa", "aa"], ["ax", "aa"], ["a", "aa"], ["aa", "a"],
    ...          ["abcdef", ""], ["", "abcdef"], ["abcdef", "abcdef"],
    ...          ["vintner", "writers"], ["vintners", "writers"]];
    >>> [editDistance(s1, s2) for s1,s2 in tests]
    [0, 1, 1, 0, 1, 2, 2, 0, 1, 1, 1, 6, 6, 0, 5, 4]
    """
    # This function is designed for Psyco
    if s1 == s2: return 0 # this is fast in Python
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    r1 = range(len(s2) + 1)
    r2 = [0] * len(r1)
    i = 0
    for c1 in s1:
        r2[0] = i + 1
        j = 0
        for c2 in s2:
            if c1 == c2:
                r2[j+1] = r1[j]
            else:
                a1 = r2[j]
                a2 = r1[j]
                a3 = r1[j+1]
                if a1 > a2:
                    if a2 > a3:
                        r2[j+1] = 1 + a3
                    else:
                        r2[j+1] = 1 + a2
                else:
                    if a1 > a3:
                        r2[j+1] = 1 + a3
                    else:
                        r2[j+1] = 1 + a1
            j += 1
        aux = r1; r1 = r2; r2 = aux
        i += 1
    return r1[-1]


def editDistanceFast(s1, s2, r1=[0]*35, r2=[0]*35):
    """Computes the Levenshtein distance between two arrays (strings too).
    Such distance is the minimum number of operations needed to transform one array into
    the other, where an operation is an insertion, deletion, or substitution of a single
    item (like a char). This implementation (Wagner-Fischer algorithm with just 2 lines)
    uses O(min(|s1|, |s2|)) space.

    This version is a bit faster but it works only with strings up to 34 items long.

    editDistanceFast([], [])
    0
    >>> editDistanceFast([1, 2, 3], [2, 3, 5])
    2
    >>> tests = [["", ""], ["a", ""], ["", "a"], ["a", "a"], ["x", "a"],
    ...          ["aa", ""], ["", "aa"], ["aa", "aa"], ["ax", "aa"], ["a", "aa"], ["aa", "a"],
    ...          ["abcdef", ""], ["", "abcdef"], ["abcdef", "abcdef"],
    ...          ["vintner", "writers"], ["vintners", "writers"]];
    >>> [editDistanceFast(s1, s2) for s1,s2 in tests]
    [0, 1, 1, 0, 1, 2, 2, 0, 1, 1, 1, 6, 6, 0, 5, 4]
    """
    # This function is designed for Psyco
    if s1 == s2: return 0 # this is fast in Python
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    len_s2 = len(s2)
    assert len(s2) <= 34, "Error: one input sequence is too much long (> 34), use editDistance()."
    for i in xrange(len_s2 + 1):
        r1[i] = i
        r2[i] = 0
    i = 0
    for c1 in s1:
        r2[0] = i + 1
        j = 0
        for c2 in s2:
            if c1 == c2:
                r2[j+1] = r1[j]
            else:
                a1 = r2[j]
                a2 = r1[j]
                a3 = r1[j+1]
                if a1 > a2:
                    if a2 > a3:
                        r2[j+1] = 1 + a3
                    else:
                        r2[j+1] = 1 + a2
                else:
                    if a1 > a3:
                        r2[j+1] = 1 + a3
                    else:
                        r2[j+1] = 1 + a1
            j += 1
        aux = r1; r1 = r2; r2 = aux
        i += 1
    return r1[len_s2]


import gc
try:
    import psyco
    psyco.bind(editDistance)
    psyco.bind(editDistanceFast)
    from psyco.classes import psyobj
except ImportError:
    psyobj = object


class BKtree(psyobj):
    """
    BKtree(items, distance, usegc=False): inputs are an iterable of hashable items that
    must allow the next() method too, and a callable that computes the distance (that
    mets the positivity, symmetry and triangle inequality conditions) between two items.

    It allows a fast search of similar items. The indexing phase may be slow,
    so this is useful only if you want to perform many searches.

    It raises a AttributeError if items doesn't have the .next() method.

    It can be used with strings, using editDistance()/editDistanceFast()

    Once initialized, you can retrieve items using xfind/find, giving an item
    and a threshold distance.

    You can disable the GC during the indexing phase to speed it up (default disabled),
    enabling it you may save some memory.
    If you have Psyco you can use it to speed up editDistanceFast.
    You can speed up this class with (but not binding it with Psyco):
    from psyco.classes import __metaclass__
    You can also use the psyco metaclass just for this BKtree class, with psyobj.

    >>> t = BKtree([], distance=editDistanceFast)
    Traceback (most recent call last):
      ...
    AttributeError: 'list' object has no attribute 'next'
    >>> t = BKtree(iter([]), distance=editDistanceFast)
    >>> t.find("hello", 1), t.find("", 0)
    ([], [])

    >>> ws = "abyss almond clump cubic cuba adopt abused chronic abutted cube clown admix almsman"
    >>> t = BKtree(iter(ws.split()), distance=editDistanceFast)
    >>> [len(t.find("cuba", th)) for th in range(7)]
    [1, 2, 3, 4, 5, 9, 13]
    >>> [t.find("cuba", th) for th in range(4)]
    [['cuba'], ['cuba', 'cube'], ['cubic', 'cuba', 'cube'], ['clump', 'cubic', 'cuba', 'cube']]
    >>> [len(t.find("abyss", th)) for th in range(7)]
    [1, 1, 1, 2, 4, 12, 12]
    >>> [t.find("abyss", th) for th in range(4)]
    [['abyss'], ['abyss'], ['abyss'], ['abyss', 'abused']]
    """
    def __init__(self, items, distance, usegc=False):
        self.distance = distance
        self.nodes = {}
        try:
            self.root = items.next()
        except StopIteration:
            self.root = ""
            return

        self.nodes[self.root] = [] # the value is a list of tuples (word, distance)
        gc_on = gc.isenabled()
        if not usegc:
            gc.disable()
        for el in items:
            if el not in self.nodes: # do not add duplicates
                self._addLeaf(self.root, el)
        if gc_on:
            gc.enable()

    def _addLeaf(self, root, item):
        dist = self.distance(root, item)
        if dist > 0:
            for arc in self.nodes[root]:
                if dist == arc[1]:
                    self._addLeaf(arc[0], item)
                    break
            else:
                if item not in self.nodes:
                    self.nodes[item] = []
                self.nodes[root].append((item, dist))

    def find(self, item, threshold):
        "Return an array with all the items found with distance <= threshold from item."
        result = []
        if self.nodes:
            self._finder(self.root, item, threshold, result)
        return result

    def _finder(self, root, item, threshold, result):
        dist = self.distance(root, item)
        if dist <= threshold:
            result.append(root)
        dmin = dist - threshold
        dmax = dist + threshold
        for arc in self.nodes[root]:
            if dmin <= arc[1] <= dmax:
                self._finder(arc[0], item, threshold, result)

    def xfind(self, item, threshold):
        "Like find, but yields items lazily. This is slower than find if you need a list."
        if self.nodes:
            return self._xfinder(self.root, item, threshold)

    def _xfinder(self, root, item, threshold):
        dist = self.distance(root, item)
        if dist <= threshold:
            yield root
        dmin = dist - threshold
        dmax = dist + threshold
        for arc in self.nodes[root]:
            if dmin <= arc[1] <= dmax:
                for node in self._xfinder(arc[0], item, threshold):
                    yield node


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print "Tests finished."

    # You need a list of words
    #words = file("somewordlist.txt").read().split()

    words = iter("""periclean germs progressed laughing allying wasting
    harassing nonsynchronous grumbled ledgers schelling shod mutating
    statewide schuman following reddened nairobi cultivate malted
    overpowering mechanic paraphrase lucerne plugged wick complimented
    roarer supercomputer impromptu cormorant abandons equalized channing
    chill bacon nonnumerical cabana amazing rheumatism""".split())

    tree = BKtree(words, editDistanceFast)

    print tree.find("cube", 4) # ['cabana', 'wick', 'chill', 'shod']

    for thresh in xrange(12):
        print thresh, len(tree.find("cube", thresh))
