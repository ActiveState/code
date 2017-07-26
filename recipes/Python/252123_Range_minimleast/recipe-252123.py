"""lca.py

Range minimization and tree least common ancestor data structures
with linear space and preprocessing time, and constant query time,
from Bender and Farach-Colton, "The LCA Problem Revisited",
Proc. LATIN 2000 (pp.88-94), http://www.cs.sunysb.edu/~bender/pub/lca.ps

Some experimentation would be needed to determine how large a query
range needs to be to make this faster than computing the min of the range
directly, and how much input data is needed to make the linear space
version pay off compared to the much simpler LogarithmicRangeMin that
it uses as a subroutine.

D. Eppstein, November 2003.
"""

# maintain Python 2.2 compatibility
if 'True' not in globals():
    globals()['True'] = not None
    globals()['False'] = not True

class RangeMin:
    """If X is any list, RangeMin(X)[i:j] == min(X[i:j]).
    Initializing RangeMin(X) takes time and space linear in len(X),
    and querying the minimum of a range takes constant time per query.
    """

    def __init__(self,X):
        """Set up structure with sequence X as data.
        Uses an LCA structure on a Cartesian tree for the input."""
        self._data = list(X)
        if len(X) > 1:
            big = map(max, self._ansv(False), self._ansv(True))
            parents = dict([(i,big[i][1]) for i in range(len(X)) if big[i]])
            self._lca = LCA(parents)
        
    def __getslice__(self,left,right):
        """Return min(X[left:right])."""
        right = min(right, len(self._data))  # handle omitted right index
        if right <= left:
            return None     # empty range has no minimum
        return self._data[self._lca(left,right-1)]
    
    def __len__(self):
        """How much data do we have?  Needed for negative index in slice."""
        return len(self._data)

    def _ansv(self,reversed):
        """All nearest smaller values.
        For each x in the data, find the value smaller than x in the closest
        position to the left of x (if not reversed) or to the right of x
        (if reversed), and return list of pairs (smaller value,position).
        Due to our use of positions as a tie-breaker, values equal to x
        count as smaller on the left and larger on the right.
        """
        stack = [None]   # protect stack top with sentinel
        output = [0]*len(self._data)
        for xi in _pairs(self._data,reversed):
            while stack[-1] > xi:
                stack.pop()
            output[xi[1]] = stack[-1]
            stack.append(xi)
        return output
        
    def _lca(self,first,last):
        """Function to replace LCA when we have too little data."""
        return 0

class LCA:
    """Structure for finding least common ancestors in trees.
    Tree nodes may be any hashable objects; a tree is specified
    by a dictionary mapping nodes to their parents.
    LCA(T)(x,y) finds the LCA of nodes x and y in tree T.
    """
    def __init__(self,parent):
        """Construct LCA structure from tree parent relation."""
        children = {}
        for x in parent:
            children.setdefault(parent[x],[]).append(x)
        root = [x for x in children if x not in parent]
        if len(root) != 1:
            raise ValueError("LCA input is not a tree")
 
        levels = []
        self._representatives = {}
        self._visit(children,levels,root[0],0)
        if [x for x in parent if x not in self._representatives]:
            raise ValueError("LCA input is not a tree")
        self._rangemin = _RestrictedRangeMin(levels)
            
    def __call__(self,*nodes):
        """Find least common ancestor of a set of nodes."""
        r = [self._representatives[x] for x in nodes]
        return self._rangemin[min(r):max(r)+1][1]

    def _visit(self,children,levels,node,level):
        """Perform Euler traversal of tree."""
        self._representatives[node] = len(levels)
        pair = (level,node)
        levels.append(pair)
        for child in children.get(node,[]):
            self._visit(children,levels,child,level+1)
            levels.append(pair)

class _RestrictedRangeMin:
    """Linear-space RangeMin for integer data obeying the constraint
        abs(X[i]-X[i-1])==1.
    We don't actually check this constraint, but results may be incorrect
    if it is violated.  For the use of this data structure from LCA, the
    data are actually pairs rather than integers, but the minima of
    all ranges are in the same positions as the minima of the integers
    in the first positions of each pair, so the data structure still works.
    """
    def __init__(self,X):
        # Compute parameters for partition into blocks.
        # Position i in X becomes transformed into
        # position i&self._blockmask in block i>>self.blocklen
        self._blocksize = _log2(len(X))//2
        self._blockmask = (1 << self._blocksize) - 1
        blocklen = 1 << self._blocksize

        # Do partition into blocks, find minima within
        # each block, prefix minima in each block,
        # and suffix minima in each block
        blocks = []             # map block to block id
        ids = {}                # map block id to PrecomputedRangeMin
        blockmin = []           # map block to min value
        self._prefix = [None]   # map data index to prefix min of block
        self._suffix = []       # map data index to suffix min of block
        for i in range(0,len(X),blocklen):
            XX = X[i:i+blocklen]
            blockmin.append(min(XX))
            self._prefix += _PrefixMinima(XX)
            self._suffix += _PrefixMinima(XX,reversed=True)
            id = len(XX) < blocklen and -1 or self._blockid(XX)
            blocks.append(id)
            if id not in ids:
                ids[id] = PrecomputedRangeMin(_pairs(XX))
        self._blocks = [ids[b] for b in blocks]
        
        # Build data structure for interblock queries
        self._blockrange = LogarithmicRangeMin(blockmin)
        self._data = list(X)

    def __getslice__(self,left,right):
        firstblock = left >> self._blocksize
        lastblock = (right - 1) >> self._blocksize
        if firstblock == lastblock:
            i = left & self._blockmask
            position = self._blocks[firstblock][i:i+right-left][1]
            return self._data[position + (firstblock << self._blocksize)]
        else:
            best = min(self._suffix[left], self._prefix[right])
            if lastblock > firstblock + 1:
                best = min(best, self._blockrange[firstblock+1:lastblock])
            return best

    def _blockid(self,XX):
        """Return value such that all blocks with the same
        pattern of increments and decrements get the same id.
        """
        id = 0
        for i in range(1,len(XX)):
            id = id*2 + (XX[i] > XX[i-1])
        return id

class PrecomputedRangeMin:
    """RangeMin solved in quadratic space by precomputing all solutions."""

    def __init__(self,X):
        self._minima = [_PrefixMinima(X[i:]) for i in range(len(X))]
    
    def __getslice__(self,x,y):
        return self._minima[x][y-x-1]
        
    def __len__(self):
        return len(self._minima)
        
class LogarithmicRangeMin:
    """RangeMin in O(n log n) space and constant query time."""
    
    def __init__(self,X):
        """Compute min(X[i:i+2**j]) for each possible i,j."""
        self._minima = m = [list(X)]
        for j in range(_log2(len(X))):
            m.append(map(min, m[-1], m[-1][1<<j:]))

    def __getslice__(self,x,y):
        """Find range minimum by representing range as the union
        of two overlapping subranges with power-of-two lengths.
        """
        j = _logtable[y-x]
        row = self._minima[j]
        return min(row[x],row[y-2**j])
        
    def __len__(self):
        return len(self._minima[0])

def _PrefixMinima(X,reversed=False):
    """Compute table of prefix minima
    (or suffix minima, if reversed=True) of list X.
    """
    current = None
    output = [None]*len(X)
    for x,i in _pairs(X,reversed):
        if current is None:
            current = x
        else:
            current = min(current,x)
        output[i] = current
    return output

def _pairs(X,reversed=False):
    """Return pairs (x,i) for x in list X, where i is
    the index of x in the data, in forward or reverse order.
    """
    indices = range(len(X))
    if reversed:
        indices.reverse()
    return [(X[i],i) for i in indices]

_logtable = [None,0]
def _log2(n):
    """Make table of logs reach up to n and return floor(log_2(n))."""
    while len(_logtable) <= n:
        _logtable.extend([1+_logtable[-1]]*len(_logtable))
    return _logtable[n]

# if run as "python lca.py", run tests on random data
# and check that RangeMin's results are correct.
if __name__ == "__main__":
    import random
    for trial in range(100):
        data = [random.choice(xrange(1000000))
                for i in range(random.randint(1,1000))]
        R = RangeMin(data)
        for sample in range(100):
            i = random.randint(0,len(data)-1)
            j = random.randint(i+1,len(data))
            if R[i:j] != min(data[i:j]):
                print "Failed to find correct minimum."
                print "Position of minimum:",data.index(min(data[i:j]))
                print "Value of minimum:",min(data[i:j])
                print "Reported minimum:",R[i:j]
                print "Length of data:",len(data)
                print "Range:",i,":",j
                print "Data:",data
                raise SystemExit
        print "Trial",trial,"complete."
    print "Completed all trials without finding any bugs."
