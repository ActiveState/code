# Graph Algorithms using basic python Constructs.
# Narayana Chikkam, Dec, 22, 2015.

from collections import defaultdict
from heapq import *
import itertools
import copy
from lib.unionfind import  (
    UnionFind
)
from lib.prioritydict import (
    priorityDictionary
)

class Vertex:
    def __init__(self, id):
        self.id = id
        self.neighbours = {}

    def addNeighbour(self, id, weight):
        self.neighbours[id] = weight

    def __str__(self):
        return str(self.id) + ': ' + str(self.neighbours.keys())

    def getNeighbours(self):
        return self.neighbours #.keys()

    def getName(self):
        return self.id

    def getWeight(self, id):
        return self.neighbours[id]

class Graph:

    def __init__(self):
        self.v = {}
        self.count = 0

    def addVertex(self, key):
        self.count += 1
        newV = Vertex(key)
        self.v[key] = newV

    def getVertex(self, id):
        if id in self.v.keys():
            return self.v[id]
        return None

    def __contains__(self, id):
        return id in self.v.keys()

    def addEdge(self, vertexOne, vertexTwo, weight=None): # vertexOne, vertexTwo, cost-of-the-edge
        if vertexOne not in self.v.keys():
            self.addVertex(vertexOne)
        if vertexTwo not in self.v.keys():
            self.addVertex(vertexTwo)

        self.v[vertexOne].addNeighbour(vertexTwo, weight)

    def updateEdge(self, vertexOne, vertexTwo, weight=None): # vertexOne, vertexTwo, cost-of-the-edge
       self.v[vertexOne].addNeighbour(vertexTwo, weight)

    def getVertices(self):
        return self.v.keys()

    def __str__(self):
        ret = "{ "
        for v in self.v.keys():
            ret += str(self.v[v].__str__()) + ", "

        return ret + " }"


    def __iter__(self):
        return iter(self.v.values())

    def getNeighbours(self,  vertex):
        if vertex not in self.v.keys():
            raise "Node %s not in graph" % vertex
        return self.v[vertex].neighbours #.keys()

    def getEdges(self):
        edges = []

        for node in self.v.keys():
            neighbours = self.v[node].getNeighbours()
            for w in neighbours:
                edges.append((node, w, neighbours[w])) #tuple, srcVertex, dstVertex, weightBetween
        return edges

    def findIsolated(self):
        isolated = []
        for node in self.v:
            deadNode = False
            reachable = True
            # dead node, can't reach any other node from this
            if len(self.v[node].getNeighbours()) == 0:
                deadNode = True

            # reachable from other nodes ?
            nbrs = [n.neighbours.keys() for n in self.v.values()]
            # flatten the nested list
            nbrs = list(itertools.chain(*nbrs))

            if node not in nbrs:
                reachable = False

            if deadNode == True and reachable == False:
                isolated.append(node)

        return isolated

    def getPath(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.v:
            return None
        for vertex in self.v[start].getNeighbours():
            if vertex not in path:
                extended_path = self.getPath(vertex,
                                            end,
                                            path)
                if extended_path:
                    return extended_path
        return None

    def getAllPaths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.v:
            return []

        paths = []
        for vertex in self.v[start].getNeighbours():
            if vertex not in path:
                extended_paths = self.getAllPaths(vertex,
                                                  end,
                                                  path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def inDegree(self, vertex):
        """
           how many edges coming into this vertex
        """
        nbrs = [n.neighbours.keys() for n in self.v.values()]
        # flatten the nested list
        nbrs = list(itertools.chain(*nbrs))

        return nbrs.count(vertex)

    def outDegree(self, vertex):
        """
           how many vertices are neighbours to this vertex
        """
        adj_vertices =  self.v[vertex].getNeighbours()
        return len(adj_vertices)

    """
       The degree of a vertex is the no of edges connecting to it.
       loop is counted twice
       for an undirected Graph deg(v) = indegree(v) + outdegree(v)
    """
    def getDegree(self, vertex):
        return self.inDegree(vertex) + self.outDegree(vertex)

    def verifyDegreeSumFormula(self):
        """Handshaking lemma - Vdeg(v) = 2 |E| """
        degSum = 0
        for v in self.v:
            degSum += self.getDegree(v)

        return degSum == (2* len(self.getEdges()))

    def delta(self):
        """ the minimum degree of the Graph V """
        min = 2**64
        for vertex in self.v:
            vertex_degree = self.getDegree(vertex)
            if vertex_degree < min:
                min = vertex_degree
        return min

    def Delta(self):
        """ the maximum degree of the Graph V """
        max = -2**64
        for vertex in self.v:
            vertex_degree = self.getDegree(vertex)
            if vertex_degree > max:
                max = vertex_degree
        return max

    def degreeSequence(self):
        """
           degree sequence is the reverse sorder of the vertices degrees
           Isomorphic graphs have the same degree sequence. However,
           two graphs with the same degree sequence are not necessarily
           isomorphic.
           More-Info:
           http://en.wikipedia.org/wiki/Graph_realization_problem
        """
        seq = []
        for vertex in self.v:
            seq.append(self.getDegree(vertex))
        seq.sort(reverse=True)
        return tuple(seq)

    # helper to check if the given sequence is in non-increasing Order ;)
    @staticmethod
    def sortedInDescendingOrder(seq):
        return all (x>=y for x,y in zip(seq, seq[1:]))

    @staticmethod
    def isGraphicSequence(seq):
      """
       Assumes that the degreeSequence is a list of non negative integers
       http://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Gallai_theorem
      """
      # Check to ensure there are an even number of odd degrees
      if sum(seq)%2 != 0: return False
      # Erdos-Gallai theorem
      for k in range(1, len(seq)+1):
        leftSum = sum(seq[:(k)])
        rightSum = k * (k-1) + sum([min(x, k) for x in seq[k:]])
        if leftSum > rightSum: return False
      return True

    @staticmethod
    def isGraphicSequenceIterative(s):
        # successively reduce degree sequence by removing node of maximum degree
        # as in Havel-Hakimi algorithm
        while s:
            s.sort()    # sort in increasing order
            if s[0]<0:
                return False  # check if removed too many from some node

            d=s.pop()             # pop largest degree
            if d==0: return True  # done! rest must be zero due to ordering

            # degree must be <= number of available nodes
            if d>len(s):   return False

            # remove edges to nodes of next higher degrees
            #s.reverse()  # to make it easy to get at higher degree nodes.
            for i in range(len(s)-1,len(s)-(d+1),-1):
                s[i]-=1

        # should never get here b/c either d==0, d>len(s) or d<0 before s=[]
        return False

    def density(self):
        """
        In mathematics, a dense graph is a graph in which the number of edges
        is close to the maximal number of edges. The opposite, a graph with
        only a few edges, is a sparse graph. The distinction between sparse
        and dense graphs is rather vague, and depends on the context.

        For undirected simple graphs, the graph density is defined as:
        D = (2*No-Of-Edges)/((v*(v-1))/2)
        For a complete Graph, the Density D is 1
        """
        """ method to calculate the density of a graph """
        V = len(self.v.keys())
        E = len(self.getEdges())
        return 2.0 * E / (V *(V - 1))

    """
        Choose an arbitrary node x of the graph G as the starting point
        Determine the set A of all the nodes which can be reached from x.
        If A is equal to the set of nodes of G, the graph is connected; otherwise
        it is disconnected.
    """
    def isConnected(self, start=None):
        if start == None:
            start = self.v.keys()[0]
        reachables = self.dfs(start, [])
        return len(reachables) == len(self.v.keys())

    """
        ToDo: USE CLR Approach for this Later
    """
    def dfs(self, start, path = []):
        path = path + [start]
        for v in self.v[start].getNeighbours().keys():
            if v not in path:
                path = self.dfs(v, path)
        return path

    """
       CLR Sytle
    """
    def CLR_Dfs(self):
        paths = []

        for v in self.v.keys():
            explored = self.dfs(v, [])
            if len(explored) == len(self.v.keys()):
                paths.append(explored)
        return paths

    def BFS(self, start):
        # initialize lists
        maxV = len(self.v.keys())
        processed = [False] * (maxV)   # which vertices have been processed
        discovered = [False] * (maxV)  # which vertices have been found
        parent= [-1] * (maxV)          # discovery relation

        q = []   # queue of vertices to visit */

        # enqueue(&q,start);
        q.append(start)

        discovered[start] = True

        while (len(q) != 0):
            v = q.pop(0)
            processed[v] = True

            nbrs = self.v[v].getNeighbours().keys()
            # print nbrs
            for n in nbrs:
                # if processed[n] == False
                if discovered[n] == False:
                    q.append(n)
                    discovered[n] = True
                    parent[n] = v

        return (discovered, parent)

    def findPath(self, start, end, parents, path):
        if ((start == end) or (end == -1)):
            path.append(start)
        else:
            self.findPath(start, parents[end], parents, path)
            path.append(end)

    """
       Find path between two given nodes
    """
    def find_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not self.v.has_key(start):
            return None
        for node in self.v[start].getNeighbours().keys():
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath: return newpath
        return None

    """
        Find all paths
    """
    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not self.v.has_key(start):
            return []
        paths = []
        for node in self.v[start].getNeighbours().keys():
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    """
        Find shorted path w.r.t no of vertices on the path
    """
    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not self.v.has_key(start):
            return None
        shortest = None
        for node in self.v[start].getNeighbours().keys():
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    """
        prim's algorithm - properties: tree could be not connected during
        the finding process as it finds edges with min cost - greedy strategy
        Prims always stays as a tree
        If you don't know all the weight on edges use
        Prim's algorithm
        f you only need partial solution on the graph
        use Prim's algorithm
    """
    def mspPrims(self):
        nodes = self.v.keys()
        edges = [(u, v, c) for u in self.v.keys() for v, c in self.v[u].getNeighbours().items()]

        return self.prim(nodes, edges)

    def prim(self, nodes, edges):
        conn = defaultdict( list )
        for n1,n2,c in edges:  # makes graph undirected
            conn[ n1 ].append( (c, n1, n2) )
            conn[ n2 ].append( (c, n2, n1) )

        mst = []
        used = set()
        used.add( nodes[0] )
        usable_edges = conn[ nodes[0] ][:]
        heapify( usable_edges )

        while usable_edges:
            cost, n1, n2 = heappop( usable_edges )
            if n2 not in used:
                used.add( n2 )
                mst.append( ( n1, n2, cost ) )

                for e in conn[ n2 ]:
                    if e[ 2 ] not in used:
                        heappush( usable_edges, e )
        return mst

    """
        Kruskals begins with forest and merge into a tree
    """
    def mspKrushkals(self):
        nodes = self.v.keys()
        edges = [(c, u, v) for u in self.v.keys() for v, c in self.v[u].getNeighbours().items()]

        return self.krushkal(edges)

    def pprint(self):
        print ("{ ", end=" ")
        for u in self.v.keys():
            print (u, end=" ")
            print (": { ", end=" ")
            for v in self.v[u].getNeighbours().keys():
                print (v, ":", self.v[u].getNeighbours()[v], end=" ")
            print(" }", end= " ")
        print (" }\n")





    def krushkal(self, edges):
        """
        Return the minimum spanning tree of an undirected graph G.
        G should be represented in such a way that iter(G) lists its
        vertices, iter(G[u]) lists the neighbors of u, G[u][v] gives the
        length of edge u,v, and G[u][v] should always equal G[v][u].
        The tree is returned as a list of edges.
        """
        # Kruskal's algorithm: sort edges by weight, and add them one at a time.
        # We use Kruskal's algorithm, first because it is very simple to
        # implement once UnionFind exists, and second, because the only slow
        # part (the sort) is sped up by being built in to Python.
        subtrees = UnionFind()
        tree = []
        for c,u,v in sorted(edges): # take from small weight to large in order
            if subtrees[u] != subtrees[v]:
                tree.append((u,v, c))
                subtrees.union(u,v)
        return tree

    def adj(self, missing=float('inf')):  # makes the adj dict will all possible cells, similar to matrix
        """
           G= { 0 : { 1 : 6, 2 : 4  }
                1 : { 2 : 3, 5 : 7  }
                2 : { 3 : 9, 4 : 1  }
                3 : { 4 : 1 }
                4 : { 5 : 5, 6 : 2  }
                5 : {  }
                6 : {  }
            }

            adj(G) >>
            { 0: {0: 0, 1: 6, 2: 4, 3: inf, 4: inf, 5: inf, 6: inf},
              1: {0: inf, 1: 0, 2: 3, 3: inf, 4: inf, 5: 7, 6: inf},
              2: {0: inf, 1: inf, 2: 0, 3: 9, 4: 1, 5: inf, 6: inf},
              3: {0: inf, 1: inf, 2: inf, 3: 0, 4: 1, 5: inf, 6: inf},
              4: {0: inf, 1: inf, 2: inf, 3: inf, 4: 0, 5: 5, 6: 2},
              5: {0: inf, 1: inf, 2: inf, 3: inf, 4: inf, 5: 0, 6: inf},
              6: {0: inf, 1: inf, 2: inf, 3: inf, 4: inf, 5: inf, 6: 0}
            }
        """
        vertices = self.v.keys()
        return {v1:
             {v2: 0 if v1 == v2 else self.v[v1].getNeighbours().get(v2, missing) for v2 in vertices
             }
             for v1 in vertices
            }

    def floyds(self):
        """
            All pair shortest Path
            Idea:
            for k in (0, n):
                for i in (0, n):
                    for j in (0, n):
                    g[i][j] = min(graph[i][j], graph[i][k]+graph[k][j])
            Find the shortest distance between every pair of vertices in the weighted Graph G
        """
        d =  self.adj()  # prepare the adjacency list representation for the algorithm

        vertices = self.v.keys()

        for v2 in vertices:
            d = {v1: {v3: min(d[v1][v3], d[v1][v2] + d[v2][v3])
                     for v3 in vertices}
                 for v1 in vertices}
        return d

    def reachability(self):
        """ Idea: graph reachability floyd-warshall
            for k in (0, n):
                for i in (0, n):
                    for j in (0, n):
                    g[i][j] = graph[i][j] || (graph[i][k]&&graph[k][j]))
        """
        vertices = self.v.keys()
        d =  self.adj(float('0'))
        for u in vertices:
            for v in vertices:
                if u ==v or d[u][v]: d[u][v] = True
                else: d[u][v] = False
        for v2 in vertices:
            d = {v1: {v3: d[v1][v3] or (d[v1][v2] and d[v2][v3]) # path for v1->v3 or v1->v2, v2-?v3
                     for v3 in vertices}
                 for v1 in vertices}
        return d



    def pathRecoveryFloydWarshall(self):
        d =  self.adj()  # missing edges will have -1.0 value
        vertices = self.v.keys()

        parentMap = copy.deepcopy(d)
        for v1 in vertices:
            for v2 in vertices:
                if (v1 == v2) or d[v1][v2] == float('inf'):
                    parentMap[v1][v2] = -1
                else:
                    parentMap[v1][v2] = v1

        for i in vertices:
            for j in vertices:
                for k in vertices:
                    temp = d[i][k] + d[k][j]
                    if temp < d[i][j]:
                        d[i][j] = temp
                        parentMap[i][j] = parentMap[k][j]

        return parentMap


    def getFloydPath(self, parentMap, u, v, path=[]):
        """
            recursive procedure to get the path from parentMap matrix
        """
        path.append(v)
        if u != v and v != -1:
            self.getFloydPath(parentMap, u, parentMap[u][v], path)


    # from active recipes - handy thoughts to think about heap for this algorithm
    def dijkstra(self, start, end=None):
        """
            Find shortest paths from the start vertex to all
            vertices nearer than or equal to the end.

            The input graph G is assumed to have the following
            representation: A vertex can be any object that can
            be used as an index into a dictionary.  G is a
            dictionary, indexed by vertices.  For any vertex v,
            G[v] is itself a dictionary, indexed by the neighbors
            of v.  For any edge v->w, G[v][w] is the length of
            the edge.  This is related to the representation in
            <http://www.python.org/doc/essays/graphs.html>

            Of course, G and G[v] need not be Python dict objects;
            they can be any other object that obeys dict protocol,
            for instance a wrapper in which vertices are URLs
            and a call to G[v] loads the web page and finds its links.

            The output is a pair (D,P) where D[v] is the distance
            from start to v and P[v] is the predecessor of v along
            the shortest path from s to v.

            Dijkstra's algorithm is only guaranteed to work correctly
            when all edge lengths are positive. This code does not
            verify this property for all edges (only the edges seen
             before the end vertex is reached), but will correctly
            compute shortest paths even for some graphs with negative
            edges, and will raise an exception if it discovers that
            a negative edge has caused it to make a mistake.

            Introduction to Algorithms, 1st edition), page 528:

            G = { 's':{'u':10, 'x':5},
                 ' u':{'v':1, 'x':2},
                 'v':{'y':4},
                 'x':{'u':3, 'v':9, 'y':2},
                 'y':{'s':7, 'v':6}
            }
        """
        G = self.adj()

        D = {}    # dictionary of final distances
        P = {}    # dictionary of predecessors
        Q = priorityDictionary()   # est.dist. of non-final vert.
        Q[start] = 0

        for v in Q:
            D[v] = Q[v]
            if v == end: break

            for w in G[v]:
                vwLength = D[v] + G[v][w]
                if w in D:
                    if vwLength < D[w]:
                        raise (ValueError, "Dijkstra: found better path to already-final vertex")
                elif w not in Q or vwLength < Q[w]:
                    Q[w] = vwLength
                    P[w] = v

        return D,P

    def shortestPathDijkstra(self, start, end):
        """
        Find a single shortest path from the given start vertex
        to the given end vertex.
        The input has the same conventions as Dijkstra().
        The output is a list of the vertices in order along
        the shortest path.
        """

        D, P = self.dijkstra(start, end)
        Path = []
        while 1:
            Path.append(end)
            if end == start: break
            end = P[end]
        Path.reverse()
        return Path

    """
        smart snippet on the dijkstra alg:
        def shortestPath(graph, start, end):
            queue = [(0, start, [])]
            seen = set()
            while True:
                (cost, v, path) = heapq.heappop(queue)
                if v not in seen:
                    path = path + [v]
                    seen.add(v)
                    if v == end:
                        return cost, path
                    for (next, c) in graph[v].iteritems():
                        heapq.heappush(queue, (cost + c, next, path))
    """

    def strongly_connected_components(self):
        """
        Tarjan's Algorithm (named for its discoverer, Robert Tarjan) is a graph theory algorithm
        for finding the strongly connected components of a graph.

        Based on: http://en.wikipedia.org/wiki/Tarjan's_strongly_connected_components_algorithm
        """

        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        result = []

        def strongconnect(node):
            # set the depth index for this node to the smallest unused index
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            stack.append(node)

            # Consider successors of `node`
            try:
                successors = self.v[node].getNeighbours().keys()
                print(node, successors)
            except:
                successors = []
            for successor in successors:
                if successor not in lowlinks:
                    # Successor has not yet been visited; recurse on it
                    strongconnect(successor)
                    lowlinks[node] = min(lowlinks[node],lowlinks[successor])
                elif successor in stack:
                    # the successor is in the stack and hence in the current strongly connected component (SCC)
                    lowlinks[node] = min(lowlinks[node],index[successor])

            # If `node` is a root node, pop the stack and generate an SCC
            if lowlinks[node] == index[node]:
                connected_component = []

                while True:
                    successor = stack.pop()
                    connected_component.append(successor)
                    if successor == node: break
                component = tuple(connected_component)
                # storing the result
                print(component)
                result.append(component)

        for node in self.v.keys():
            if node not in lowlinks:
                strongconnect(node)

        return result

    def computeFirstUsingSCC(self, initFirst):

        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        result = []
        first = {}

        def computeFirst(node):
            # set the depth index for this node to the smallest unused index
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            stack.append(node)

            # Consider successors of `node`
            try:
                successors = self.v[node].getNeighbours().keys()
            except:
                successors = []
            for successor in successors:

                if successor not in lowlinks:
                    # Successor has not yet been visited; recurse on it
                    computeFirst(successor)

                    lowlinks[node] = min(lowlinks[node],lowlinks[successor])
                elif successor in stack:
                    # the successor is in the stack and hence in the current strongly connected component (SCC)
                    lowlinks[node] = min(lowlinks[node],index[successor])
                first[node] |= set(first[successor] - set(['epsilon'])).union(set(initFirst[node]))  #(*union!*)


            # If `node` is a root node, pop the stack and generate an SCC
            if lowlinks[node] == index[node]:
                connected_component = []

                while True:
                    successor = stack.pop()
                    #FIRST[w] := FIRST[v]; (*distribute!*)
                    first[successor] = set(first[node] - set(['epsilon'])).union(set(initFirst[successor]) )#(*distribute!*)
                    connected_component.append(successor)
                    if successor == node: break
                component = tuple(connected_component)
                # storing the result
                result.append(component)

        for v in initFirst:
            first[v] = initFirst[v]  #(*init!*)
        #print "init First assignment: ", first

        for node in self.v.keys():
            if node not in lowlinks:
                computeFirst(node)

        return first

    def computeFollowUsingSCC(self, FIRST, initFollow):

        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        result = []
        follow = {}

        def computeFollow(node):
            # set the depth index for this node to the smallest unused index
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            stack.append(node)

            # Consider successors of `node`
            try:
                successors = self.v[node].getNeighbours().keys()
            except:
                successors = []
            for successor in successors:

                if successor not in lowlinks:
                    # Successor has not yet been visited; recurse on it
                    computeFollow(successor)

                    lowlinks[node] = min(lowlinks[node],lowlinks[successor])
                elif successor in stack:
                    # the successor is in the stack and hence in the current strongly connected component (SCC)
                    lowlinks[node] = min(lowlinks[node],index[successor])

                follow[node] |= follow[successor] #(*union!*)


            # If `node` is a root node, pop the stack and generate an SCC
            if lowlinks[node] == index[node]:
                connected_component = []

                while True:
                    successor = stack.pop()
                    follow[successor] = follow[node]
                    connected_component.append(successor)
                    if successor == node: break
                component = tuple(connected_component)
                # storing the result
                result.append(component)

        for v in initFollow:
            follow[v] = initFollow[v]  #(*init!*)

        for node in self.v.keys():
            if node not in lowlinks:
                computeFollow(node)

        return follow
