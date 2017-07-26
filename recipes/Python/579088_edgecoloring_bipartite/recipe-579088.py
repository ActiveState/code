from bipartite_recipe import bipartite_match
def max_degree(graph):
	max_degree_u=max(len(v) for v in graph.values() )
	count={}
	for vlist in graph.values():
		for v in vlist:
			try:
				count[v]+=1
			except KeyError:
				count[v]=1
	max_degree_v=max(count.values())
	return max(max_degree_v,max_degree_u)
def best_match(graph):
	b_m=bipartiteMatch(graph)[0]
	return dict((value,key) for (key,value) in b_m.items())
def edge_coloring(graph):
	g=graph.copy()
	number_colors=max_degree(g)
	for color in range(number_colors):
		print 'NEXT COLOR'
		bm=best_match(g)
		print bm
		for k in g.copy():
			try:
				g[k].remove(bm[k])
			except KeyError:
				pass

graph={ 'p1':['c1','c3'], 'p2':['c1','c2'], 'p3':['c2','c3'], 'p4':['c2'] }
edge_coloring(graph)
