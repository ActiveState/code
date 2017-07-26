## Flattening an arbitrarily nested list in Python  
Originally published: 2014-10-05 21:44:45  
Last updated: 2014-10-05 21:44:45  
Author: Vasudev Ram  
  
This is a recipe to flatten a Python list which may have nested lists as items within it. It works for lists that have a maximum depth of nesting roughly equal to the recursion depth limit of Python, which is set to 1000 by default, though it can be increased with sys.setrecursionlimit().
