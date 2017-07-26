## Hopcroft-Karp bipartite matching  
Originally published: 2002-04-27 16:53:22  
Last updated: 2002-04-27 16:53:22  
Author: David Eppstein  
  
Takes as input a bipartite graph in a variation of Guido van Rossum's dictionary-of-lists format, and outputs both a maximum matching (largest possible set of nonadjacent edges) and a maximum independent set (largest possible set of nonadjacent vertices).  The running time in the worst case is O(E sqrt(V)) but for many graphs it runs faster due to doing fewer than the worst case number of iterations.