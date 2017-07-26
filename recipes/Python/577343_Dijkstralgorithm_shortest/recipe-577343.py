# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
from priodict import priorityDictionary

def Dijkstra(graph,start,end=None):
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
	where Guido van Rossum suggests representing graphs
	as dictionaries mapping vertices to lists of neighbors,
	however dictionaries of edges have many advantages
	over lists: they can store extra information (here,
	the lengths), they support fast existence tests,
	and they allow easy modification of the graph by edge
	insertion and removal.  Such modifications are not
	needed here but are important in other graph algorithms.
	Since dictionaries obey iterator protocol, a graph
	represented as described here could be handed without
	modification to an algorithm using Guido's representation.

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
	"""

	final_distances = {}	# dictionary of final distances
	predecessors = {}	# dictionary of predecessors
	estimated_distances = priorityDictionary()   # est.dist. of non-final vert.
	estimated_distances[start] = 0

	for vertex in estimated_distances:
		final_distances[vertex] = estimated_distances[vertex]
		if vertex == end: break

		for edge in graph[vertex]:
			path_distance = final_distances[vertex] + graph[vertex][edge]
			if edge in final_distances:
				if path_distance < final_distances[edge]:
					raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
			elif edge not in estimated_distances or path_distance < estimated_distances[edge]:
				estimated_distances[edge] = path_distance
				predecessors[edge] = vertex

	return (final_distances,predecessors)

def shortestPath(graph,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	final_distances,predecessors = Dijkstra(graph,start,end)
	path = []
	while 1:
		path.append(end)
		if end == start: break
		end = predecessors[end]
	path.reverse()
	return path
