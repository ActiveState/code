# Finding Eulerian path in undirected graph
# Przemek Drochomirecki, Krakow, 5 Nov 2006

def eulerPath(graph):
    # counting the number of vertices with odd degree
    odd = [ x for x in graph.keys() if len(graph[x])&1 ]
    odd.append( graph.keys()[0] )

    if len(odd)>3:
        return None
    
    stack = [ odd[0] ]
    path = []
    
    # main algorithm
    while stack:
        v = stack[-1]
        if graph[v]:
            u = graph[v][0]
            stack.append(u)
            # deleting edge u-v
            del graph[u][ graph[u].index(v) ]
            del graph[v][0]
        else:
            path.append( stack.pop() )
    
    return path
