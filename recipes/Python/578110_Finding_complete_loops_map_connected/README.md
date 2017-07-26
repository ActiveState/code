## Finding complete loops in a map of connected nodes  
Originally published: 2012-04-24 18:47:20  
Last updated: 2012-04-24 18:47:21  
Author: Sachin Joglekar  
  
This module finds loops in a given map.Input is a dictionary like\n\nd={1:[2,4,5,6],2:[1,3],3:[2,4,5,6],4:[1,3,5],5:[1,3,4],6:[1,3]}\n\nthis means node 1 is connected to nodes 2,4,5 and 6 and so on..\n\nOutput is a list of complete loops.\nfor above examples,output is\n\n[[1, 4, 5, 1], [3, 4, 5, 3], [1, 2, 3, 4, 1], [1, 2, 3, 5, 1], [1, 2, 3, 6, 1], [1, 4, 3, 5, 1], [1, 4, 3, 6, 1], [1, 5, 3, 6, 1], [1, 2, 3, 4, 5, 1], [1, 4, 5, 3, 6, 1]]