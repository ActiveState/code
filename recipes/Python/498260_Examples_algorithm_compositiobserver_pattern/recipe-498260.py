"""tsort module

Implements the toposort and strongly_connected_components graph
algorithms, as a demonstration of how to use the recipe, 'Implementing
the observer pattern yet again: this time with coroutines and the with
statement'
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/498259)

Requires Python 2.5
Author: Jim Baker (jbaker@zyasoft.com)
"""

from __future__ import with_statement
from observer import consumer, observation
from collections import deque
import unittest


# Colors used by the traversal (DFS) to mark if it has visited all
# vertices leading out of a given vertex.  WHITE is implicit.
# Alternatively use an enumeration as supported by this recipe,
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/413486

GRAY = 'gray'   # currently visiting this vertex
BLACK = 'black' # all adjacent vertices visited

def toposort(G):
    """Returns the topological sort of the input graph G.

    The algorithm toposort is described in Cormen, Leiserson, Rivest,
    *Introduction to Algorithms* [CLR].  The code here is explicitly
    modeled on their pseudocode.
    
    David Eppstein's PADS library employs an alternative strategy of
    'shadowing' the Searcher class methods via inheritance
    (http://www.ics.uci.edu/~eppstein/PADS/DFS.py).  His strategy
    makes the preorder, postorder, and backedge events more explicit
    than the implicit usage presented here based on coloring changes.
    """

    ordering = deque()
    seen = set()
    coloring = dict()

    @consumer
    def finishing(order):
        """Returns the vertices in the reverse of their finishing time.

        This function is implemented as a coroutine so that it can be
        decoupled from the actual setting of the vertice's color in
        the DFS. So the only protocol that requires agreement is this
        marking of a coloring.

        It's critical that this function be decorated with the
        @consumer decorator so that it's advanced to waiting on any
        data.
        """

        while True:
            v, old_color, new_color = (yield)
            if new_color == BLACK:
                order.appendleft(v)

    with observation(observe=coloring,
                     notify=[finishing(ordering)]) as coloring:
        for v in DFS(G, coloring):
            # In this code, the real work is in the finishing
            # function.  For now, we will just verify that the vertex
            # is touched at *most* once.
            assert(v not in seen)
            seen.add(v)

    # Now verify that each vertex was touched at *least* once
    assert(seen == set(vertices(G)))
        
    return ordering


def strongly_connected_components(G):
    """Returns the strongly connnected components of G as frozensets.

    SCC is a good test of the toposort algorithm just described. See
    [CLR] for more details. Constructing the components as frozensets
    simplifies their use.

    The following iterator pipeline will return the components in
    order of decreasing size:

    sorted(strongly_connected_components(G), key=len, reverse=True)
    """
    
    ordering = toposort(G)
    R = reverse(G)
    coloring = dict()
    for v in ordering:
        component = frozenset(w for w in DFS_visit(R, coloring, v))
        if component:
            yield component



######################################################################
# What follows is just support code and unit testing.
######################################################################

# Please note, since this is just to illustrate the use of the
# observer pattern, we don't manage reverse edges efficiently.

def edges(G):
    """Returns the edge set of G as pairs (v, w)"""
    for v, adj in G.iteritems():
        for w in adj:
            yield v, w

def vertices(G):
    """Returns the vertex set of G"""
    return iter(G)

def adjacent(G, v):
    """Returns the adjacent vertices to v, if any"""
    for w in G.get(v, ()):
        yield w

def graph_equal(G, H):
    """Tests the equality of graphs"""
    return set(edges(G)) == set(edges(H)) and \
           set(vertices(G)) == set(vertices(H))

def reverse(G):
    """Reverses the edges in a graph.

    Always returns an adjacency list representation, using the GvR
    model. Empty vertices are maintained.
    """

    R = {}
    for v in vertices(G): R[v] = []
    for v, w in edges(G): R[w].append(v)
    return R


def DFS(G, coloring=None, roots=None):
    """Performs a depth-first search of the graph `G`"""
    
    if coloring is None:
        coloring = dict()
    if roots is None:
        roots = vertices(G)
        
    for v in roots:
        for w in DFS_visit(G, coloring, v):
            yield w


def DFS_visit(G, coloring, v):
    """A recursive generator implementation of a depth-first search visitor.

    Please note that as a recursive function, it may exhaust Python's
    stack. Consider using NetworkX or PADS instead. Results are
    produced incrementally, a nice benefit of using a generator.
    """
    
    if v in coloring:
        return
        
    yield v
    coloring[v] = GRAY

    for w in adjacent(G, v):
        if w not in coloring:
            for descendant in DFS_visit(G, coloring, w):
                yield descendant
    coloring[v] = BLACK




def pairwise(iterable):
    from itertools import tee, izip
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    try:
        b.next()
    except StopIteration:
        pass
    return izip(a, b)

class TsortTestCase(unittest.TestCase):

    # from itertools recipes

    def testTopoSort(self):
        def verify_partial_ordering(G, ordering):
            """Verifies that `ordering` is a partial ordering of graph `G`."""

            ordering = tuple(ordering)
            assert(set(ordering) == set(vertices(G)))
            for v, w in pairwise(ordering):
                # need to ensure that v > w, from a graph theoretic perspective
                self.assert_(v not in adjacent(G,w))

        # Prof. Bumstead's dependency graph from CLR
        Bumstead = {
            'undershorts':['pants', 'shoes'],
            'socks': ['shoes'],
            'watch': [],
            'pants': ['belt'],
            'shirt': ['belt', 'tie'],
            'belt': ['jacket'],
            'jacket': [],
            'shoes': [],
            'tie':  [],
            }

        verify_partial_ordering(Bumstead, toposort(Bumstead))
        verify_partial_ordering(reverse(Bumstead), toposort(reverse(Bumstead)))

    def testSCC(self):
        def verify_strongly_connected(precomputed, computed):
            # turn components into a set of frozensets, simplifies the comparison
            self.assertEquals(set(frozenset(component) for component in precomputed),
                              set(frozenset(component) for component in computed))

        # from Eppstein's tests
        G1 = { 0:[1], 1:[2,3], 2:[4,5], 3:[4,5], 4:[6], 5:[], 6:[] }
        C1 = [[0],[1],[2],[3],[4],[5],[6]]

        G2 = { 0:[1], 1:[2,3,4], 2:[0,3], 3:[4], 4:[3] }
        C2 = [[0,1,2],[3,4]]

        C1_computed = sorted(strongly_connected_components(G1), key=len, reverse=True)
        C2_computed = sorted(strongly_connected_components(G2), key=len, reverse=True)

        verify_strongly_connected(C1, C1_computed)
        verify_strongly_connected(C2, C2_computed)

if __name__ == "__main__":
    unittest.main()
