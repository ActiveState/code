## Python Binary Search Tree  
Originally published: 2011-08-08 00:15:09  
Last updated: 2011-08-08 00:15:09  
Author: sivarama sarma  
  
A data structure that holds a sorted collection of values, and supports efficient insertion, deletion, sorted iteration, and min/max finding.  Values may sorted either based on their natural ordering, or on a key function (specified as an argument to the search tree's constructor).  The search tree may contain duplicate values (or multiple values with equal keys) -- the ordering of such values is undefined.

This implementation was made with efficiency in mind.  In particular, it is more than twice as fast as the other native-Python implementations I tried (which all use objects to store search tree nodes).

See also: <http://en.wikipedia.org/wiki/Binary_search_tree>, <http://en.wikipedia.org/wiki/A*_search_algorithm>