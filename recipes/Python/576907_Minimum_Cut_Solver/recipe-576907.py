"""
    A Minimum Cut Solver
    
    This python script is for solving the ACM problem Q2914: Minimum Cut.
    http://acm.pku.edu.cn/JudgeOnline/problem?id=2914

    Instead of using Ford-Fulkerson method, I use Stoer and Wagner's Min cut Algorithm.
    http://www.cs.dartmouth.edu/~ac/Teach/CS105-Winter05/Handouts/stoerwagner-mincut.pdf

    However I also include the max flow method (from wiki) for benchmark.
    The code can be found at: http://en.wikipedia.org/wiki/Ford-Fulkerson_algorithm
    
    Copyright 2009 Shao-Chuan Wang <shaochuan.wang@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

"""
__author__ = "Shao-Chuan Wang"
__email__ = "shaochuan.wang@gmail.com"
__version__ = "1.0"
__URL__ = "http://shao-chuan.appspot.com"

g_TryFlowNetwork = False
class FlowNetwork(object):
    ''' This class is copied from wiki for benchmark.
    '''
    def __init__(self):
        self.adj, self.flow, = {},{}
        self.src, self.sink = None, None
 
    def add_vertex(self, vertex):
        self.adj[vertex] = []

    def add_vertices(self, vertices):
        map(self.add_vertex, vertices)
 
    def get_edges(self, v):
        return self.adj[v]
 
    def add_edge(self, u,v,w=0):
        self.adj[u].append((v,w))
        self.adj[v].append((u,0))
        self.flow[(u,v)] = self.flow[(v,u)] = 0
 
    def find_path(self, source, sink, path):
        if source == sink:
            return path
        for vertex, capacity in self.get_edges(source):
            residual = capacity - self.flow[(source,vertex)]
            edge = (source,vertex,residual)
            if residual > 0 and not edge in path:
                result = self.find_path(vertex, sink, path + [edge]) 
                if result != None:
                    return result
 
    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            flow = min(r for u,v,r in path)
            for u,v,_ in path:
                self.flow[(u,v)] += flow
                self.flow[(v,u)] -= flow
            path = self.find_path(source, sink, [])
        return sum(self.flow[(source, vertex)] for vertex, capacity in self.get_edges(source))
      
class UndirectedGraph(object):
  def __init__(self):
    self.vertices = []
    self.edges = {}

  def add_vertex(self, v):
    self.vertices.append(v)
    self.edges[(v,v)] = 0

  def add_vertices(self, v_s):
    self.vertices.extend(v_s)
    for v in v_s:
      self.edges[(v,v)] = 0

  def add_edge(self, u, v, w=0):
    self.edges[(u,v)] = w
    self.edges[(v,u)] = w

  def adjacents(self, u):
    li = []
    for v in self.vertices:
      w = self.edges.get((u,v),0)
      if w:
        li.append((v,w))
    return li

  def merge(self, u, v):
    ''' merge u to v, where v is in the graph
    '''
    u_adjs = self.adjacents(u)
    for z,w in u_adjs:
      self.edges.pop((u,z))
      self.edges.pop((z,u))
    self.vertices.remove(u)
    v_adjs = dict(self.adjacents(v))
    for n, w in u_adjs:
      if n == v:
        continue
      v_adjs[n] = v_adjs.get(n,0) + w
    for n, w in v_adjs.iteritems():
      self.edges[(v,n)] = w
      self.edges[(n,v)] = w    

def w(g, A, y):
  assert y not in A
  return sum(w for v, w in g.adjacents(y) if v in A)

def min_cut_phase(g, a):
  A = set([a])
  V = set(g.vertices)
  order = [a]
  while A != V:
    w_candidates = [(w(g, A, v), v) for v in V-A]  #: candidates for most tightly connected
    _, x = max(w_candidates)
    A.add(x)
    order.append(x)
  t, s = order[-1], order[-2]

  min_cut = sum(w for v, w in g.adjacents(t))
  g.merge(t, s)
  return min_cut

def minimum_cut(g, a):
  min_cut = sum(w for v, w in g.adjacents(a))
  while len(g.vertices) > 1:
    min_cut_candidate = min_cut_phase(g, a)
    if min_cut_candidate < min_cut:
      min_cut = min_cut_candidate
  return min_cut


class Reader(object):
  ''' A file reader: read the formated input data provided by Q2914: Minimum Cut
  '''
  def __init__(self, fd):
    ''' @param fd: an opened file-like object, and its contents are the input data.
    '''
    self.fd = fd

  def gen_graph(self):
    ''' a generator that yield graphs in order
    '''
    while True:
      try:
        line = self.fd.next()
        nVertices, nEdges = map(int, line.split())
        if g_TryFlowNetwork:
          g = FlowNetwork()
          g.add_vertices(xrange(nVertices))
          for i in xrange(nEdges):
            u,v,w = map(int, self.fd.next().split())
            if u < v:
              g.add_edge(u, v, w)
            else:
              g.add_edge(v, u, w)
          g.src, g.sink = 0, nVertices-1
        else:
          g = UndirectedGraph()
          g.add_vertices(xrange(nVertices))
          for i in xrange(nEdges):
            u,v,w = map(int, self.fd.next().split())
            g.add_edge(u, v, w)          
        yield g
      except StopIteration:
        break
    
  def __del__(self):
    self.fd.close()

if __name__=='__main__':
  import time
  from StringIO import StringIO
  
  test_input = '''3 3
0 1 1
1 2 1
2 0 1
4 3
0 1 1
1 2 1
2 3 1
8 14
0 1 1
0 2 1
0 3 1
1 2 1
1 3 1
2 3 1
4 5 1
4 6 1
4 7 1
5 6 1
5 7 1
6 7 1
4 0 1
7 3 1
8 12
0 1 2
0 4 3
1 4 2
4 5 3
1 2 3
1 5 2
5 6 1
2 6 2
2 3 4
3 6 2
3 7 2
6 7 3
5 10
0 1 1
0 2 1
0 3 1
0 4 1
1 2 1
1 3 1
1 4 1
2 3 1
2 4 1
3 4 1
20 190
0 1 1
0 2 1
0 3 1
0 4 1
0 5 1
0 6 1
0 7 1
0 8 1
0 9 1
0 10 1
0 11 1
0 12 1
0 13 1
0 14 1
0 15 1
0 16 1
0 17 1
0 18 1
0 19 1
1 2 1
1 3 1
1 4 1
1 5 1
1 6 1
1 7 1
1 8 1
1 9 1
1 10 1
1 11 1
1 12 1
1 13 1
1 14 1
1 15 1
1 16 1
1 17 1
1 18 1
1 19 1
2 3 1
2 4 1
2 5 1
2 6 1
2 7 1
2 8 1
2 9 1
2 10 1
2 11 1
2 12 1
2 13 1
2 14 1
2 15 1
2 16 1
2 17 1
2 18 1
2 19 1
3 4 1
3 5 1
3 6 1
3 7 1
3 8 1
3 9 1
3 10 1
3 11 1
3 12 1
3 13 1
3 14 1
3 15 1
3 16 1
3 17 1
3 18 1
3 19 1
4 5 1
4 6 1
4 7 1
4 8 1
4 9 1
4 10 1
4 11 1
4 12 1
4 13 1
4 14 1
4 15 1
4 16 1
4 17 1
4 18 1
4 19 1
5 6 1
5 7 1
5 8 1
5 9 1
5 10 1
5 11 1
5 12 1
5 13 1
5 14 1
5 15 1
5 16 1
5 17 1
5 18 1
5 19 1
6 7 1
6 8 1
6 9 1
6 10 1
6 11 1
6 12 1
6 13 1
6 14 1
6 15 1
6 16 1
6 17 1
6 18 1
6 19 1
7 8 1
7 9 1
7 10 1
7 11 1
7 12 1
7 13 1
7 14 1
7 15 1
7 16 1
7 17 1
7 18 1
7 19 1
8 9 1
8 10 1
8 11 1
8 12 1
8 13 1
8 14 1
8 15 1
8 16 1
8 17 1
8 18 1
8 19 1
9 10 1
9 11 1
9 12 1
9 13 1
9 14 1
9 15 1
9 16 1
9 17 1
9 18 1
9 19 1
10 11 1
10 12 1
10 13 1
10 14 1
10 15 1
10 16 1
10 17 1
10 18 1
10 19 1
11 12 1
11 13 1
11 14 1
11 15 1
11 16 1
11 17 1
11 18 1
11 19 1
12 13 1
12 14 1
12 15 1
12 16 1
12 17 1
12 18 1
12 19 1
13 14 1
13 15 1
13 16 1
13 17 1
13 18 1
13 19 1
14 15 1
14 16 1
14 17 1
14 18 1
14 19 1
15 16 1
15 17 1
15 18 1
15 19 1
16 17 1
16 18 1
16 19 1
17 18 1
17 19 1
18 19 1
50 1225
0 1 1
0 2 1
0 3 1
0 4 1
0 5 1
0 6 1
0 7 1
0 8 1
0 9 1
0 10 1
0 11 1
0 12 1
0 13 1
0 14 1
0 15 1
0 16 1
0 17 1
0 18 1
0 19 1
0 20 1
0 21 1
0 22 1
0 23 1
0 24 1
0 25 1
0 26 1
0 27 1
0 28 1
0 29 1
0 30 1
0 31 1
0 32 1
0 33 1
0 34 1
0 35 1
0 36 1
0 37 1
0 38 1
0 39 1
0 40 1
0 41 1
0 42 1
0 43 1
0 44 1
0 45 1
0 46 1
0 47 1
0 48 1
0 49 1
1 2 1
1 3 1
1 4 1
1 5 1
1 6 1
1 7 1
1 8 1
1 9 1
1 10 1
1 11 1
1 12 1
1 13 1
1 14 1
1 15 1
1 16 1
1 17 1
1 18 1
1 19 1
1 20 1
1 21 1
1 22 1
1 23 1
1 24 1
1 25 1
1 26 1
1 27 1
1 28 1
1 29 1
1 30 1
1 31 1
1 32 1
1 33 1
1 34 1
1 35 1
1 36 1
1 37 1
1 38 1
1 39 1
1 40 1
1 41 1
1 42 1
1 43 1
1 44 1
1 45 1
1 46 1
1 47 1
1 48 1
1 49 1
2 3 1
2 4 1
2 5 1
2 6 1
2 7 1
2 8 1
2 9 1
2 10 1
2 11 1
2 12 1
2 13 1
2 14 1
2 15 1
2 16 1
2 17 1
2 18 1
2 19 1
2 20 1
2 21 1
2 22 1
2 23 1
2 24 1
2 25 1
2 26 1
2 27 1
2 28 1
2 29 1
2 30 1
2 31 1
2 32 1
2 33 1
2 34 1
2 35 1
2 36 1
2 37 1
2 38 1
2 39 1
2 40 1
2 41 1
2 42 1
2 43 1
2 44 1
2 45 1
2 46 1
2 47 1
2 48 1
2 49 1
3 4 1
3 5 1
3 6 1
3 7 1
3 8 1
3 9 1
3 10 1
3 11 1
3 12 1
3 13 1
3 14 1
3 15 1
3 16 1
3 17 1
3 18 1
3 19 1
3 20 1
3 21 1
3 22 1
3 23 1
3 24 1
3 25 1
3 26 1
3 27 1
3 28 1
3 29 1
3 30 1
3 31 1
3 32 1
3 33 1
3 34 1
3 35 1
3 36 1
3 37 1
3 38 1
3 39 1
3 40 1
3 41 1
3 42 1
3 43 1
3 44 1
3 45 1
3 46 1
3 47 1
3 48 1
3 49 1
4 5 1
4 6 1
4 7 1
4 8 1
4 9 1
4 10 1
4 11 1
4 12 1
4 13 1
4 14 1
4 15 1
4 16 1
4 17 1
4 18 1
4 19 1
4 20 1
4 21 1
4 22 1
4 23 1
4 24 1
4 25 1
4 26 1
4 27 1
4 28 1
4 29 1
4 30 1
4 31 1
4 32 1
4 33 1
4 34 1
4 35 1
4 36 1
4 37 1
4 38 1
4 39 1
4 40 1
4 41 1
4 42 1
4 43 1
4 44 1
4 45 1
4 46 1
4 47 1
4 48 1
4 49 1
5 6 1
5 7 1
5 8 1
5 9 1
5 10 1
5 11 1
5 12 1
5 13 1
5 14 1
5 15 1
5 16 1
5 17 1
5 18 1
5 19 1
5 20 1
5 21 1
5 22 1
5 23 1
5 24 1
5 25 1
5 26 1
5 27 1
5 28 1
5 29 1
5 30 1
5 31 1
5 32 1
5 33 1
5 34 1
5 35 1
5 36 1
5 37 1
5 38 1
5 39 1
5 40 1
5 41 1
5 42 1
5 43 1
5 44 1
5 45 1
5 46 1
5 47 1
5 48 1
5 49 1
6 7 1
6 8 1
6 9 1
6 10 1
6 11 1
6 12 1
6 13 1
6 14 1
6 15 1
6 16 1
6 17 1
6 18 1
6 19 1
6 20 1
6 21 1
6 22 1
6 23 1
6 24 1
6 25 1
6 26 1
6 27 1
6 28 1
6 29 1
6 30 1
6 31 1
6 32 1
6 33 1
6 34 1
6 35 1
6 36 1
6 37 1
6 38 1
6 39 1
6 40 1
6 41 1
6 42 1
6 43 1
6 44 1
6 45 1
6 46 1
6 47 1
6 48 1
6 49 1
7 8 1
7 9 1
7 10 1
7 11 1
7 12 1
7 13 1
7 14 1
7 15 1
7 16 1
7 17 1
7 18 1
7 19 1
7 20 1
7 21 1
7 22 1
7 23 1
7 24 1
7 25 1
7 26 1
7 27 1
7 28 1
7 29 1
7 30 1
7 31 1
7 32 1
7 33 1
7 34 1
7 35 1
7 36 1
7 37 1
7 38 1
7 39 1
7 40 1
7 41 1
7 42 1
7 43 1
7 44 1
7 45 1
7 46 1
7 47 1
7 48 1
7 49 1
8 9 1
8 10 1
8 11 1
8 12 1
8 13 1
8 14 1
8 15 1
8 16 1
8 17 1
8 18 1
8 19 1
8 20 1
8 21 1
8 22 1
8 23 1
8 24 1
8 25 1
8 26 1
8 27 1
8 28 1
8 29 1
8 30 1
8 31 1
8 32 1
8 33 1
8 34 1
8 35 1
8 36 1
8 37 1
8 38 1
8 39 1
8 40 1
8 41 1
8 42 1
8 43 1
8 44 1
8 45 1
8 46 1
8 47 1
8 48 1
8 49 1
9 10 1
9 11 1
9 12 1
9 13 1
9 14 1
9 15 1
9 16 1
9 17 1
9 18 1
9 19 1
9 20 1
9 21 1
9 22 1
9 23 1
9 24 1
9 25 1
9 26 1
9 27 1
9 28 1
9 29 1
9 30 1
9 31 1
9 32 1
9 33 1
9 34 1
9 35 1
9 36 1
9 37 1
9 38 1
9 39 1
9 40 1
9 41 1
9 42 1
9 43 1
9 44 1
9 45 1
9 46 1
9 47 1
9 48 1
9 49 1
10 11 1
10 12 1
10 13 1
10 14 1
10 15 1
10 16 1
10 17 1
10 18 1
10 19 1
10 20 1
10 21 1
10 22 1
10 23 1
10 24 1
10 25 1
10 26 1
10 27 1
10 28 1
10 29 1
10 30 1
10 31 1
10 32 1
10 33 1
10 34 1
10 35 1
10 36 1
10 37 1
10 38 1
10 39 1
10 40 1
10 41 1
10 42 1
10 43 1
10 44 1
10 45 1
10 46 1
10 47 1
10 48 1
10 49 1
11 12 1
11 13 1
11 14 1
11 15 1
11 16 1
11 17 1
11 18 1
11 19 1
11 20 1
11 21 1
11 22 1
11 23 1
11 24 1
11 25 1
11 26 1
11 27 1
11 28 1
11 29 1
11 30 1
11 31 1
11 32 1
11 33 1
11 34 1
11 35 1
11 36 1
11 37 1
11 38 1
11 39 1
11 40 1
11 41 1
11 42 1
11 43 1
11 44 1
11 45 1
11 46 1
11 47 1
11 48 1
11 49 1
12 13 1
12 14 1
12 15 1
12 16 1
12 17 1
12 18 1
12 19 1
12 20 1
12 21 1
12 22 1
12 23 1
12 24 1
12 25 1
12 26 1
12 27 1
12 28 1
12 29 1
12 30 1
12 31 1
12 32 1
12 33 1
12 34 1
12 35 1
12 36 1
12 37 1
12 38 1
12 39 1
12 40 1
12 41 1
12 42 1
12 43 1
12 44 1
12 45 1
12 46 1
12 47 1
12 48 1
12 49 1
13 14 1
13 15 1
13 16 1
13 17 1
13 18 1
13 19 1
13 20 1
13 21 1
13 22 1
13 23 1
13 24 1
13 25 1
13 26 1
13 27 1
13 28 1
13 29 1
13 30 1
13 31 1
13 32 1
13 33 1
13 34 1
13 35 1
13 36 1
13 37 1
13 38 1
13 39 1
13 40 1
13 41 1
13 42 1
13 43 1
13 44 1
13 45 1
13 46 1
13 47 1
13 48 1
13 49 1
14 15 1
14 16 1
14 17 1
14 18 1
14 19 1
14 20 1
14 21 1
14 22 1
14 23 1
14 24 1
14 25 1
14 26 1
14 27 1
14 28 1
14 29 1
14 30 1
14 31 1
14 32 1
14 33 1
14 34 1
14 35 1
14 36 1
14 37 1
14 38 1
14 39 1
14 40 1
14 41 1
14 42 1
14 43 1
14 44 1
14 45 1
14 46 1
14 47 1
14 48 1
14 49 1
15 16 1
15 17 1
15 18 1
15 19 1
15 20 1
15 21 1
15 22 1
15 23 1
15 24 1
15 25 1
15 26 1
15 27 1
15 28 1
15 29 1
15 30 1
15 31 1
15 32 1
15 33 1
15 34 1
15 35 1
15 36 1
15 37 1
15 38 1
15 39 1
15 40 1
15 41 1
15 42 1
15 43 1
15 44 1
15 45 1
15 46 1
15 47 1
15 48 1
15 49 1
16 17 1
16 18 1
16 19 1
16 20 1
16 21 1
16 22 1
16 23 1
16 24 1
16 25 1
16 26 1
16 27 1
16 28 1
16 29 1
16 30 1
16 31 1
16 32 1
16 33 1
16 34 1
16 35 1
16 36 1
16 37 1
16 38 1
16 39 1
16 40 1
16 41 1
16 42 1
16 43 1
16 44 1
16 45 1
16 46 1
16 47 1
16 48 1
16 49 1
17 18 1
17 19 1
17 20 1
17 21 1
17 22 1
17 23 1
17 24 1
17 25 1
17 26 1
17 27 1
17 28 1
17 29 1
17 30 1
17 31 1
17 32 1
17 33 1
17 34 1
17 35 1
17 36 1
17 37 1
17 38 1
17 39 1
17 40 1
17 41 1
17 42 1
17 43 1
17 44 1
17 45 1
17 46 1
17 47 1
17 48 1
17 49 1
18 19 1
18 20 1
18 21 1
18 22 1
18 23 1
18 24 1
18 25 1
18 26 1
18 27 1
18 28 1
18 29 1
18 30 1
18 31 1
18 32 1
18 33 1
18 34 1
18 35 1
18 36 1
18 37 1
18 38 1
18 39 1
18 40 1
18 41 1
18 42 1
18 43 1
18 44 1
18 45 1
18 46 1
18 47 1
18 48 1
18 49 1
19 20 1
19 21 1
19 22 1
19 23 1
19 24 1
19 25 1
19 26 1
19 27 1
19 28 1
19 29 1
19 30 1
19 31 1
19 32 1
19 33 1
19 34 1
19 35 1
19 36 1
19 37 1
19 38 1
19 39 1
19 40 1
19 41 1
19 42 1
19 43 1
19 44 1
19 45 1
19 46 1
19 47 1
19 48 1
19 49 1
20 21 1
20 22 1
20 23 1
20 24 1
20 25 1
20 26 1
20 27 1
20 28 1
20 29 1
20 30 1
20 31 1
20 32 1
20 33 1
20 34 1
20 35 1
20 36 1
20 37 1
20 38 1
20 39 1
20 40 1
20 41 1
20 42 1
20 43 1
20 44 1
20 45 1
20 46 1
20 47 1
20 48 1
20 49 1
21 22 1
21 23 1
21 24 1
21 25 1
21 26 1
21 27 1
21 28 1
21 29 1
21 30 1
21 31 1
21 32 1
21 33 1
21 34 1
21 35 1
21 36 1
21 37 1
21 38 1
21 39 1
21 40 1
21 41 1
21 42 1
21 43 1
21 44 1
21 45 1
21 46 1
21 47 1
21 48 1
21 49 1
22 23 1
22 24 1
22 25 1
22 26 1
22 27 1
22 28 1
22 29 1
22 30 1
22 31 1
22 32 1
22 33 1
22 34 1
22 35 1
22 36 1
22 37 1
22 38 1
22 39 1
22 40 1
22 41 1
22 42 1
22 43 1
22 44 1
22 45 1
22 46 1
22 47 1
22 48 1
22 49 1
23 24 1
23 25 1
23 26 1
23 27 1
23 28 1
23 29 1
23 30 1
23 31 1
23 32 1
23 33 1
23 34 1
23 35 1
23 36 1
23 37 1
23 38 1
23 39 1
23 40 1
23 41 1
23 42 1
23 43 1
23 44 1
23 45 1
23 46 1
23 47 1
23 48 1
23 49 1
24 25 1
24 26 1
24 27 1
24 28 1
24 29 1
24 30 1
24 31 1
24 32 1
24 33 1
24 34 1
24 35 1
24 36 1
24 37 1
24 38 1
24 39 1
24 40 1
24 41 1
24 42 1
24 43 1
24 44 1
24 45 1
24 46 1
24 47 1
24 48 1
24 49 1
25 26 1
25 27 1
25 28 1
25 29 1
25 30 1
25 31 1
25 32 1
25 33 1
25 34 1
25 35 1
25 36 1
25 37 1
25 38 1
25 39 1
25 40 1
25 41 1
25 42 1
25 43 1
25 44 1
25 45 1
25 46 1
25 47 1
25 48 1
25 49 1
26 27 1
26 28 1
26 29 1
26 30 1
26 31 1
26 32 1
26 33 1
26 34 1
26 35 1
26 36 1
26 37 1
26 38 1
26 39 1
26 40 1
26 41 1
26 42 1
26 43 1
26 44 1
26 45 1
26 46 1
26 47 1
26 48 1
26 49 1
27 28 1
27 29 1
27 30 1
27 31 1
27 32 1
27 33 1
27 34 1
27 35 1
27 36 1
27 37 1
27 38 1
27 39 1
27 40 1
27 41 1
27 42 1
27 43 1
27 44 1
27 45 1
27 46 1
27 47 1
27 48 1
27 49 1
28 29 1
28 30 1
28 31 1
28 32 1
28 33 1
28 34 1
28 35 1
28 36 1
28 37 1
28 38 1
28 39 1
28 40 1
28 41 1
28 42 1
28 43 1
28 44 1
28 45 1
28 46 1
28 47 1
28 48 1
28 49 1
29 30 1
29 31 1
29 32 1
29 33 1
29 34 1
29 35 1
29 36 1
29 37 1
29 38 1
29 39 1
29 40 1
29 41 1
29 42 1
29 43 1
29 44 1
29 45 1
29 46 1
29 47 1
29 48 1
29 49 1
30 31 1
30 32 1
30 33 1
30 34 1
30 35 1
30 36 1
30 37 1
30 38 1
30 39 1
30 40 1
30 41 1
30 42 1
30 43 1
30 44 1
30 45 1
30 46 1
30 47 1
30 48 1
30 49 1
31 32 1
31 33 1
31 34 1
31 35 1
31 36 1
31 37 1
31 38 1
31 39 1
31 40 1
31 41 1
31 42 1
31 43 1
31 44 1
31 45 1
31 46 1
31 47 1
31 48 1
31 49 1
32 33 1
32 34 1
32 35 1
32 36 1
32 37 1
32 38 1
32 39 1
32 40 1
32 41 1
32 42 1
32 43 1
32 44 1
32 45 1
32 46 1
32 47 1
32 48 1
32 49 1
33 34 1
33 35 1
33 36 1
33 37 1
33 38 1
33 39 1
33 40 1
33 41 1
33 42 1
33 43 1
33 44 1
33 45 1
33 46 1
33 47 1
33 48 1
33 49 1
34 35 1
34 36 1
34 37 1
34 38 1
34 39 1
34 40 1
34 41 1
34 42 1
34 43 1
34 44 1
34 45 1
34 46 1
34 47 1
34 48 1
34 49 1
35 36 1
35 37 1
35 38 1
35 39 1
35 40 1
35 41 1
35 42 1
35 43 1
35 44 1
35 45 1
35 46 1
35 47 1
35 48 1
35 49 1
36 37 1
36 38 1
36 39 1
36 40 1
36 41 1
36 42 1
36 43 1
36 44 1
36 45 1
36 46 1
36 47 1
36 48 1
36 49 1
37 38 1
37 39 1
37 40 1
37 41 1
37 42 1
37 43 1
37 44 1
37 45 1
37 46 1
37 47 1
37 48 1
37 49 1
38 39 1
38 40 1
38 41 1
38 42 1
38 43 1
38 44 1
38 45 1
38 46 1
38 47 1
38 48 1
38 49 1
39 40 1
39 41 1
39 42 1
39 43 1
39 44 1
39 45 1
39 46 1
39 47 1
39 48 1
39 49 1
40 41 1
40 42 1
40 43 1
40 44 1
40 45 1
40 46 1
40 47 1
40 48 1
40 49 1
41 42 1
41 43 1
41 44 1
41 45 1
41 46 1
41 47 1
41 48 1
41 49 1
42 43 1
42 44 1
42 45 1
42 46 1
42 47 1
42 48 1
42 49 1
43 44 1
43 45 1
43 46 1
43 47 1
43 48 1
43 49 1
44 45 1
44 46 1
44 47 1
44 48 1
44 49 1
45 46 1
45 47 1
45 48 1
45 49 1
46 47 1
46 48 1
46 49 1
47 48 1
47 49 1
48 49 1
'''
  global g_TryFlowNetwork
  g_TryFlowNetwork = False #: when this variable is True, use FlowNetwork to find the min cut.
  fd = StringIO()
  fd.write(test_input)
  fd.seek(0)
  r = Reader(fd)
  for g in r.gen_graph():
    start_time = time.time()
    if g_TryFlowNetwork:
      print g.max_flow(g.src, g.sink)
    else:
      print minimum_cut(g, 1)
    print time.time() - start_time
