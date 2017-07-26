## Dijkstra's algorithm for shortest paths 
Originally published: 2002-04-04 12:38:22 
Last updated: 2002-04-04 12:38:22 
Author: David Eppstein 
 
Dijkstra(G,s) finds all shortest paths from s to each other vertex in the graph, and shortestPath(G,s,t) uses Dijkstra to find the shortest path from s to t.  Uses the priorityDictionary data structure (Recipe 117228) to keep track of estimated distances to each vertex.