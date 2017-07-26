## Range minima and least common ancestors  
Originally published: 2003-11-13 23:10:41  
Last updated: 2003-11-13 23:10:41  
Author: David Eppstein  
  
Data structures for solving the following two problems:\n\n- Range minimization: given an array X of data, quickly find min(X[i:j]) for different ranges i:j.\n\n- Least common ancestors: given a tree, quickly find the lowest tree node that is an ancestor of all of a given set of nodes.\n\nBoth problems are solved by data structures that take linear time and space to set up, after which queries can be answered in constant time.