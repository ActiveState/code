# Full implementation: http://sourceforge.net/projects/pynetwork/

class _GetterSetter(object):
    def __init__(self, g, n1):
        self._g = g
        self._n1 = n1
    def __setitem__(self, n2, arcw):
        self._g.addArc(self._n1, n2, arcw)
    def __getitem__(self, n2):
        return self._g.getArcw(self._n1, n2)
    def __str__(self):
        return "<Getter/setter of the arc starting from node: " + repr(self._n1) + ">"

class Graph(object):
    def __init__(self, nodesGraph=None, nodeData=None):
        if isinstance(nodesGraph, Graph):
            self.o = {}
            self.i = {}
            self_o = self.o
            self_i = self.i
            for n,a in nodesGraph.o.iteritems():
                self_o[n] = dict(a)
            for n,a in nodesGraph.i.iteritems():
                self_i[n] = dict(a)
            self.nodeData = dict(nodesGraph.nodeData)
            self.arcCount = nodesGraph.arcCount
            self.nextNode = nodesGraph.nextNode
        else:
            self.o = {} # Outbound arcs. Node name => outbound name arcs => arc weights.
            self.i = {} # Inbound arcs. Node name => inbound arc names => arc weights (oa transposed).
            self.nodeData = {} # Node data. Node name => optional data associated with the node
                               #   (not present means None).
            self.arcCount = 0  # Total number of directed arcs. Each self-loop is counted two times.
            self.nextNode = 0 # Next number that can be used by createID.
            if nodesGraph: # This can be made faster, but here controls are important.
                for n1, arcs in nodesGraph.iteritems():
                    self.addNode(n1)
                    for n2, w in arcs.iteritems():
                        self.addArc(n1, n2, w)
                if nodeData:
                    for node,data in nodeData.iteritems():
                        if node in self.o:
                            self.nodeData[node] = data

    def addNode(self, n, nodeData=None):
        if n not in self.o:
            self.o[n] = {}
            self.i[n] = {}
        if nodeData is None:
            if n in self.nodeData:
                del self.nodeData[n] # Not present nodeData is equivalent to None.
        else:
            self.nodeData[n] = nodeData

    add = addNode

    def __contains__(self, node):
        return node in self.o

    def getNodeData(self, n):
        if n in self.o and n in self.nodeData:
            return self.nodeData[n]

    def changeNodeData(self, n, newnd):
        if newnd is None:
            self.nodeData.pop(n, 0)
        elif n in self.o:
            self.nodeData[n] = newnd

    def renameNode(self, oldnode, newnode):
        self_o = self.o
        self_i = self.i
        if oldnode in self_o and oldnode in self_i and newnode not in self_o:
            self_o[newnode] = dict(self_o[oldnode])
            self_i[newnode] = dict(self_i[oldnode])
            for n,w in self_i[oldnode].iteritems():
                self_o[n][newnode] = w
                del self_o[n][oldnode]
            for n,w in self_o[oldnode].iteritems():
                self_i[n][newnode] = w
                del self_i[n][oldnode]
            if oldnode in self.nodeData:
                self.nodeData[newnode] = self.nodeData[oldnode]
                del self.nodeData[oldnode]
            del self_o[oldnode]
            del self_i[oldnode]

    def firstNode(self):
        if not self.o: return None
        return self.o.iterkeys().next()

    def delNode(self, n):
        self_o = self.o
        self_i = self.i
        if n in self_o and n in self_i:
            arcCount = self.arcCount
            if n in self_o[n]:
                del self_o[n][n]
                arcCount -= 2
            if n in self_i[n]:
                del self_i[n][n]
            for n1 in self_i[n].iterkeys():
                if n1 in self_o and n in self_o[n1]:
                    del self_o[n1][n]
                    arcCount -= 1
            for n1 in self_o[n].iterkeys():
                if n1 in self_i and n in self_i[n1]:
                    del self_i[n1][n]
            self.arcCount = arcCount - len(self_o[n])
            del self_o[n]
            del self_i[n]
            if n in self.nodeData:
                del self.nodeData[n]

    def popNode(self):
        if not self.o:
            raise IndexError("No items to select.")
        node = self.o.iterkeys().next()
        self.delNode(node) # remove it.
        return node

    def xinNodes(self, n):
        if n in self.i:
            return self.i[n].iterkeys()
        else:
            return []

    def xoutNodes(self, n):
        if n in self.o:
            return self.o[n].iterkeys()
        else:
            return []

    def __iter__(self):
        return self.o.iterkeys()

    def addArc(self, n1, n2, w=None):
        self_o = self.o
        self_i = self.i
        if n1 not in self_o:
            self_o[n1] = {}
            self_i[n1] = {}
        if n2 not in self_o:
            self_o[n2] = {}
            self_i[n2] = {}
        if n2 not in self_o[n1]:
            if n1 == n2:
                self.arcCount += 2
            else:
                self.arcCount += 1
        self_o[n1][n2] = w
        self_i[n2][n1] = w

    def __getitem__(self, n1):
        return _GetterSetter(self, n1)

    def hasArc(self, n1, n2):
        self_o = self.o
        self_i = self.i
        return ( n1 in self_o and n2 in self_o and n1 in self_i and n2 in self_i and
                 n2 in self_o[n1] and n1 in self_i[n2] )

    def getArcw(self, n1, n2):
        if n1 not in self.o:
            raise KeyError, repr(n1)
        if n2 not in self.o[n1]:
            raise KeyError, repr(n1) + " -> " + repr(n2)
        return self.o[n1][n2]

    def setArcw(self, n1, n2, neww):
        if n1 in self.o and n2 in self.o[n1]:
            self.o[n1][n2] = neww
        if n2 in self.i and n1 in self.i[n2]:
            self.i[n2][n1] = neww

    def delArc(self, n1, n2):
        if n1 in self.o and n2 in self.o[n1]:
            del self.o[n1][n2]
            if n1 == n2:
                self.arcCount -= 2
            else:
                self.arcCount -= 1
        if n2 in self.i and n1 in self.i[n2]:
            del self.i[n2][n1]

    def xinArcs(self, n):
        if n in self.i:
            return ((n1, n) for n1 in self.i[n].iterkeys())
        else:
            return []

    def xoutArcs(self, n):
        if n in self.o:
            return ((n, n1) for n1 in self.o[n].iterkeys())
        else:
            return []

    def xarcsw(self):
        self_o = self.o
        return ( (n1,n2,w) for n1,a in self_o.iteritems() for n2,w in a.iteritems() )

    def firstArc(self):
        if not self.arcCount: return None
        for n1,a in self.o.iteritems():
            if a: return n1, a.iterkeys().next()

    def copy(self):
        "copy(): return a shallow copy of the graph."
        return self.__class__(self)

    __copy__ = copy # For the copy module

    def clear(self):
        self.i.clear()
        self.o.clear()
        self.arcCount = 0
        self.nodeData.clear()
        self.nextNode = 0

    def __hash__(self):
        raise TypeError, "A Graph is a mutable, and cannot be hashed."

    def addUpdate(self, other):
        self._testBinary(other, "addUpdate")
        for n in other.o.iterkeys():
            if n not in self.o:
                self.o[n] = dict( other.o[n] )
                self.i[n] = dict( other.i[n] )
            else:
                self.o[n].update( other.o[n] )
                self.i[n].update( other.i[n] )
        self.nodeData.update( other.nodeData )
        self.nextNode = max(self.nextNode, other.nextNode)
        self._recountArcs()

    def subUpdate(self, other):
        self._testBinary(other, "subUpdate")
        for n1, a1 in other.o.iteritems():
            if n1 in self.o:
                for n2 in a1.iterkeys():
                    self.delArc(n1,n2)
                if not self.o[n1]:
                    self.delNode(n1)
        self._recountArcs()

    def intersection(self, other):
        self._testBinary(other, "intersection")
        common = self.__class__() # Necessary for a good subclassing.
        for n1 in set(self.o).intersection(other.o): # filter(d1_has_key, d2)
            if n1 not in common.o:
                common.o[n1] = {} # add empty node.
                common.i[n1] = {}
            for n2 in set(self.o[n1]).intersection(other.o[n1]):
                if n2 not in common.o:
                    common.o[n2] = {} # add empty node.
                    common.i[n2] = {}
                aux = self.o[n1][n2]
                if aux == other.o[n1][n2]:
                    w = aux
                else:
                    w = None
                common.o[n1][n2] = w
                common.i[n2][n1] = w
                if n1 == n2:
                    common.arcCount += 2
                else:
                    common.arcCount += 1
            nd = self.nodeData.get(n1)
            if nd != None and nd == other.nodeData.get(n1):
                common.nodeData[n1] = nd
        common.nextNode = max(self.nextNode, other.nextNode)
        return common

    def nodeIntersection(self, other):
        self._testBinary(other, "nodeIntersection")
        self_o_has_key = self.o.has_key
        other_o = other.o
        return filter(self_o_has_key, other_o)

    def __eq__(self, other):
        if isinstance(other, Graph):
            return self.o == other.o and self.i == other.i and \
                   self.arcCount == other.arcCount and self.nodeData == other.nodeData
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Graph):
            return self.o != other.o or self.i != other.i or \
                   self.arcCount != other.arcCount or self.nodeData != other.nodeData
        else:
            return True

    def _testBinary(self, other, sop):
        if not isinstance(other, type(self.__class__())):
            raise TypeError, sop + " only permitted between graphs."

    def order(self):
        return len(self.o)

    def size(self):
        return self.arcCount

    def __len__(self):
        return len(self.o)

    def __nonzero__(self):
        return bool(self.o)

    def __repr__(self):
        return "".join(["Graph(", repr(self.o), ", ", repr(self.nodeData), ")"])


# -------------------------
# A small demo, towns less then 1000 Km from Amsterdam:
table = (("Amsterdam", "Nijmegen",    122),
         ("Paris",     "Amsterdam",   490),
         ("Paris",     "Rome",       1140),
         ("Berlin",    "Amsterdam",   705),
         ("Amsterdam", "Kobenhaven",  764),
         ("Amsterdam", "Rome",       1640),
         ("Moscow",    "Amsterdam",  2523))
g = Graph()
for n1, n2, dist in table:
    g[n1][n2] = dist
    g[n2][n1] = dist
print g, "\n"
for city in g.xoutNodes("Amsterdam"):
    if g["Amsterdam"][city] < 1000:
        print city, g["Amsterdam"][city]
