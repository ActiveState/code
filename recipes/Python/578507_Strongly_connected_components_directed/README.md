## Strongly connected components of a directed graph.Originally published: 2013-04-02 19:33:16 
Last updated: 2013-04-03 19:30:32 
Author: Mark Dickinson 
 
Two linear-time algorithms for finding the strongly connected components of a directed graph.  `strongly_connected_components_tree` implements (a variant of) Tarjan's well-known algorithm for finding strongly connected components, while `strongly_connected_components_path` implements a path-based algorithm due (in this form) to Gabow.\n\nEdit:  I added an iterative function `strongly_connected_components_iterative`;  this is a direct conversion of `strongly_connected_components_path` into iterative form.  It's therefore safe to use on high-depth graphs, without risk of running into Python's recursion limit.