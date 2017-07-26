from graph_tool.all import Vertex, Graph

class MyVertex:
    def __init__(self, g):
        self.g = g
        self.v = g.add_vertex()
        self.halted = False
        
    def vote_for_halt(self):
        self.halted = True

    def __getattr__(self, attr):
        return getattr(self.v, attr)

if __name__ == "__main__":        
    g = Graph()
    v1 = MyVertex(g)
    v2 = MyVertex(g)
    g.add_edge(v1, v2)
    v1.vote_for_halt()
    print v1.out_degree()  # will print 1
    print v1.halted  # will print True
    print v1.foo  # will raise error: AttributeError: 'Vertex' object has no attribute 'foo'
