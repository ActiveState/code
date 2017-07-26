## Predicate tests across sequences  
Originally published: 2001-04-19 16:12:44  
Last updated: 2002-06-05 09:45:38  
Author: Jon Dyte  
  
Often it is useful to know whether all elements of sequence meet
certain criteria, or if only some pass a test.
These two functions "every" and "any" do just that.

Example usage:
>>> every(lambda c: c > 5,(6,7,8,9))
1
>>> every(lambda c: c < 5,(6,7,8,9))
0
>>> any(lambda c: c > 5,(6,7,8,9))
1
>>> any(lambda c: c < 5,(6,7,8,9))
0