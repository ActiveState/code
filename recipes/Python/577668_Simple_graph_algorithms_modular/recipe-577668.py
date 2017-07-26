from abc import ABCMeta, abstractmethod
from collections import Counter
from Queue import Queue, LifoQueue


class AbstractGraph(dict):
    __metaclass__ = ABCMeta

    def __init__(self):
        dict.__init__(self)
        self._size = 0
    
    def order(self):
        return len(self)

    def size(self):
        return self._size

    def neighbours(self, v):
        return self[v]

    @abstractmethod
    def degree(self, v):
        pass

    def add_vertex(self, v):
        self[v] = set()
    
    @abstractmethod
    def add_edge(self, u, v):
        self._size += 1

    @abstractmethod
    def remove_edge(self, u, v):
        self._size -= 1


class UndirectedGraph(AbstractGraph):

    def degree(self, v):
        return len(self.neighbours(v))
    
    def add_edge(self, u, v):
        AbstractGraph.add_edge(self, u, v)
        self.neighbours(u).add(v)
        self.neighbours(v).add(u)           

    def remove_edge(self, u, v):
        AbstractGraph.remove_edge(self, u, v)
        self.neighbours(u).remove(v)
        self.neighbours(v).remove(u)


class DirectedGraph(AbstractGraph):

    def __init__(self):
        AbstractGraph.__init__(self)
        self._indegree = Counter()
    
    def in_degree(self, v):
        return self._indegree[v]

    def out_degree(self, v):
        return len(self.neighbours(v))

    def degree(self, v):
        return self.in_degree(v) + self.out_degree(v)
    
    def add_edge(self, u, v):
        AbstractGraph.add_edge(self, u, v)
        self.neighbours(u).add(v)
        self._indegree[v] += 1

    def remove_edge(self, u, v):
        AbstractGraph.remove_edge(self, u, v)
        self.neighbours(u).remove(v)
        self._indegree[v] -= 1


def generic_search(G, s, t, Q):
    visited = set()
    Q.put(s)

    while not Q.empty():
       u = Q.get()
       if u not in visited:
           if u == t:
               return True
           for v in G.neighbours(u):
               Q.put(v)
           visited.add(u)

    return False

        
def breadth_first_search(G, s, t):
    return generic_search(G, s, t, Queue())


def depth_first_search(G, s, t):
    return generic_search(G, s, t, LifoQueue())
    


if __name__ == '__main__':
    
    G = UndirectedGraph()
    for i in range(1, 5):
        G.add_vertex(i)
    G.add_edge(1, 2)
    G.add_edge(2, 3)

    assert G.order() == 4
    assert G.size() == 2

    assert 2 in G.neighbours(1) and 1 in G.neighbours(2)
    assert G.degree(1) == 1 and G.degree(2) == 2
    
    assert breadth_first_search(G, 1, 3) and depth_first_search(G, 1, 3)
    assert breadth_first_search(G, 3, 1) and depth_first_search(G, 3, 1)
    assert not (breadth_first_search(G, 4, 2) or depth_first_search(G, 4, 2))

    
    G = DirectedGraph()
    for i in range(1, 4):
        G.add_vertex(i)
    G.add_edge(1, 2)
    G.add_edge(2, 3)

    assert G.order() == 3
    assert G.size() == 2

    assert 2 in G.neighbours(1) and 1 not in G.neighbours(2)
    assert G.degree(1) == 1 and G.degree(2) == 2
    assert G.in_degree(2) == G.out_degree(2) == 1
    
    assert breadth_first_search(G, 1, 3) and depth_first_search(G, 1, 3)
    assert not (breadth_first_search(G, 3, 1) or depth_first_search(G, 3, 1))

    print 'OK'
