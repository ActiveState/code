## Tuples with Named Elements via Spawning  
Originally published: 2004-09-07 19:45:52  
Last updated: 2004-09-08 02:54:50  
Author: Derrick Wallace  
  
In recipe 303439 (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/303439) Andrew Durdin presents a customized tuple class that permits individual item access via a named attribute.  I think this concept is quite novel and, as Andrew points out, can greatly improve readability of code.  In this recipe I implement his tuple concept in a slightly different manner.

Instead of requiring the named attributes list for each instantiation of the tuple, my implementation 'Spawns' a derived tuple class that is taylored to the named attributes specified.  And it is this Spawned class that is then used to instantiate tuples.  My approach effectively separates the definition of the attribute names from the data specification.  And in doing so, this approach diminishes instantiation hassles and further improves clarity.