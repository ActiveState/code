## Synchronizing all methods in an object 
Originally published: 2001-06-14 02:07:21 
Last updated: 2001-06-14 02:07:21 
Author: André Bjärby 
 
Makes sure that only one thread at a time is "inside" the object. This restriction can be lifted for methods whose locking you want to handcode.