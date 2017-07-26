## Dijkstra's algorithm for shortest paths  
Originally published: 2010-08-02 13:03:44  
Last updated: 2010-08-02 13:03:45  
Author: poromenos   
  
Dijkstra(G,s) finds all shortest paths from s to each other vertex in the graph, and shortestPath(G,s,t) uses Dijkstra to find the shortest path from s to t.  Uses the priorityDictionary data structure (Recipe 117228) to keep track of estimated distances to each vertex.