## topological sorting again  
Originally published: 2013-01-07 14:51:50  
Last updated: 2013-03-06 19:21:11  
Author: yota   
  
Topological sorting is the answer to the following question : in a direct acyclic graph, how can I pick up nodes "in order", such as upstream nodes are always before downstream ones ? Many solutions may exists, many algorithms too.

Alas, it seems I'm too stupid to understand already proposed recipes on topological sorting. Hopefully I do grasp the "write once, read many" concept.

Here, you will find a plain algorithm, optimized only for code clarity, of a topological sorting for direct acyclic graphs, implemented in python from the pseudo code found on [wikipedia](http://en.wikipedia.org/wiki/Topological_sorting):

    L ← Empty list that will contain the sorted elements
    S ← Set of all nodes with no incoming edges
    while S is non-empty do
        remove a node n from S
        insert n into L
        for each node m with an edge e from n to m do
            remove edge e from the graph
            if m has no other incoming edges then
                insert m into S
    if graph has edges then
        return error (graph has at least one cycle)
    else 
        return L (a topologically sorted order)

Only tested with python3.2, should work with other versions. Be careful, code indented with tabs, since space is evil è_é