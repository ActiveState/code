## Predicate tests across sequences  
Originally published: 2001-04-19 16:12:44  
Last updated: 2002-06-05 09:45:38  
Author: Jon Dyte  
  
Often it is useful to know whether all elements of sequence meet\ncertain criteria, or if only some pass a test.\nThese two functions "every" and "any" do just that.\n\nExample usage:\n>>> every(lambda c: c > 5,(6,7,8,9))\n1\n>>> every(lambda c: c < 5,(6,7,8,9))\n0\n>>> any(lambda c: c > 5,(6,7,8,9))\n1\n>>> any(lambda c: c < 5,(6,7,8,9))\n0