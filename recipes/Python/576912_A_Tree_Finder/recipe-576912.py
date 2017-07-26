"""
    Is It A Tree? A Tree Finder.
    
    This python script is for solving the ACM problem Q1308: Is It A Tree?
    http://acm.pku.edu.cn/JudgeOnline/problem?id=1308
    
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

class DirectedGraph(object):
  def __init__(self):
    self.vertices = set()
    self.adjs = {}
    
  def add_vertex(self, v):
    if v not in self.vertices:
      self.vertices.add(v)
      self.adjs[v] = {}
    else:
      print 'warning! try to add a existed vertex.'

  def add_edge(self, u, v, w=1):
    ''' @ add an edge from u -> v.
    '''
    if u not in self.vertices:
      self.add_vertex(u)
    if v not in self.vertices:
      self.add_vertex(v)
    
    self.adjs[u][v] = w

  def adjacents(self, u):
    return self.adjs[u].keys()


class TreeFinder(object):
  def __init__(self):
    self.has_duplicate_edges = False      
    self.inv_g = DirectedGraph()
    self.roots = set()
    
  def add_edges(self, edges):
    if len(edges) != len(set(edges)):
      self.has_duplicate_edges = True
      
    for u,v in edges:
      self.inv_g.add_edge(v,u) # here, the most tricky part!!

  def find_roots(self, v, visited):
    ''' @return: False, if failed to find the root,
                 starting with vertex 'v' and past path 'visited'
                 True, otherwise.
    '''
    adjs = self.inv_g.adjacents(v)
    if not adjs:
      self.roots.add(v)
      return True
    if len(adjs)>1:
      return False    # With bifurcation
    else:
      u = adjs[0]
      visited[v] = True
      if not visited.get(u, False):
        return self.find_roots(u, visited)
      else:
        return False  # With cycle
    return True

  def isTree(self):
    if not self.inv_g.vertices:
      return True
    if self.has_duplicate_edges:
      return False
    
    isATree = True
    for v in self.inv_g.vertices:
      if not self.find_roots(v, {}):
        isATree = False
    if not isATree:
      return False

    if len(self.roots) != 1:
      return False

    return True

class Reader(object):
  def __init__(self, fd):
    self.fd = fd

  def process_line(self, line):
    it = iter(map(int, line.strip().split()))
    return zip(it,it)
    
  def gen_edges(self):
    edges = []
    while True:
      try:
        line = self.fd.next()
        edges.extend( self.process_line(line) )
        if edges[-1] == (0,0):
          edges.pop()
          yield edges
          edges = []
        elif edges[-1] == (-1,-1):
          break
      except StopIteration:
        break

  def __del__(self):
    self.fd.close()


if __name__=='__main__':
  import StringIO
  import random
  import time
  def test(test_data):
    fd = StringIO.StringIO()
    fd.write(test_data)
    fd.seek(0)
    r = Reader(fd)
    for case_id, edges in enumerate(r.gen_edges()):
      tree_finder = TreeFinder()
      tree_finder.add_edges(edges)
      s = '' if tree_finder.isTree() else 'not '
      print 'Case %d is %sa tree' % (case_id+1, s)

  simple_test_data = '''8 1
7 3 6 2 8 9 7 5
7 4 7 8 7 6 0 0
6 8  5 3  5 2  6 4
5 6  0 0
3 8  6 8  6 4
5 3  5 6  5 2  0 0
0 0
1 2 0 0
1 2 1 3 4 5 0 0
1 1 0 0
1 2 2 1 0 0
1 2 1 2 0 0
1 2 2 3 3 1 4 5 0 0
-1 -1
'''
  test(simple_test_data)

  print '='*5,'my test data','='*5
  long_path = ' '.join(
      ['%d %d' % (i, i+1) for i in xrange(1,300)]+['\n']
      ) 
  long_path_2 = ' '.join(
      ['%d %d' % (i, i+1) for i in xrange(301,400)]+['\n']
      )
  
  is_a_tree_test_data = ''.join([long_path, long_path_2, '32 301 0 0'])
  start_time = time.time()
  test(is_a_tree_test_data)
  print 'time: %f' %(time.time()-start_time)
  
  is_not_a_tree_test_data = ''.join([long_path, long_path_2, '32 305 0 0'])
  start_time = time.time()
  test(is_not_a_tree_test_data)
  print 'time: %f' %(time.time()-start_time)
