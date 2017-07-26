## Reference count checking  
Originally published: 2006-06-11 01:15:56  
Last updated: 2006-06-11 01:15:56  
Author: Robin Becker  
  
Whilst testing that a C extension was causing a problem with reference counts I created some code to check that the reference counts of a set of variables were not being changed by a call to a specific C method. That code itself was buggy as the output of a particular reference count eg 12 could actually modify one or more of the reference counts being checked. The solution was to store the refcount info as a string.