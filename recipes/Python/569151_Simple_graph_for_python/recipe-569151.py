class Graph:
    def __init__(self,name=""):
        self.name = name
        self.list_neighbor = {}
        self.list_node = {}
    def add_node(self,node):
        self.list_node[node] = True

    def add_edge(self,node,nodebis):
        try :
            self.list_neighbor[node].append(nodebis)
        except :
            self.list_neighbor[node] = []
            self.list_neighbor[node].append(nodebis)
        try :
            self.list_neighbor[nodebis].append(node)
        except :
            self.list_neighbor[nodebis] = []
            self.list_neighbor[nodebis].append(node)
    def neighbors(self,node):
        try :
            return self.list_neighbor[node]
        except :
            return []
    def nodes(self):
        return self.list_node.keys()
    def delete_edge(self,node,nodebis):
        self.list_neighbor[node].remove(nodebis)
        self.list_neighbor[nodebis].remove(node)
    def delete_node(self,node):
        del self.list_node[node]
        try :
            for nodebis in self.list_neighbor[node] :
                self.list_neighbor[nodebis].remove(node)
            del self.list_neighbor[node]
        except :
            return "error"

if __name__ == "__main__":
    G = Graph("test")
    G.add_node(1)
    G.add_node(2)
    G.add_edge(1,2)
    print G.neighbors(1)
