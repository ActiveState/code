#!/usr/bin/env python3.2

def sort_direct_acyclic_graph(edge_list) :
	# edge_set is consummed, need a copy
	edge_set = set([tuple(i) for i in edge_list])
	
	# node_list will contain the ordered nodes
	node_list = list()
	
	# source_set is the set of nodes with no incomming edges
	node_from_list, node_to_list = zip(* edge_set)
	source_set = set(node_from_list) - set(node_to_list)
	
	while len(source_set) != 0 :
		# pop node_from off source_set and insert it in node_list
		node_from = source_set.pop()
		node_list.append(node_from)
		
		# find nodes which have a common edge with node_from
		from_selection = [e for e in edge_set if e[0] == node_from]
		for edge in from_selection :
			# remove the edge from the graph
			node_to = edge[1]
			edge_set.discard(edge)
			
			# if node_to don't have any remaining incomming edge :
			to_selection = [e for e in edge_set if e[1] == node_to]
			if len(to_selection) == 0 :
				# add node_to to source_set
				source_set.add(node_to)
				
	if len(edge_set) != 0 :
		raise IndexError # not a direct acyclic graph
	else :
		return node_list

u = [
	['a', 'b'], # a -> b, etc.
	['a', 'c'],
	['b', 'e'],
	['c', 'd'],
	['b', 'd'],
	['e', 'f'],
	['c', 'f'],
]

>>> sort_direct_acyclic_graph(u)
['a', 'c', 'b', 'e', 'd', 'f']
