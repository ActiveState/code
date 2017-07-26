###Combinations of a sequence without replacement using dynamic programming

Originally published: 2011-06-20 20:09:24
Last updated: 2011-06-20 20:09:24
Author: Filippo Squillace

This recipe shows a way to solve the K-combinations problem without replacement with a sequence of items using the dynamic programming technique.\n\nIf you want a divine but slower solution take into account a "divide et impera" paradigm like in this recipe: http://code.activestate.com/recipes/190465-generator-for-permutations-combinations-selections/\n\nThis implementation could be improved overcoming some drawbacks. In particular, the inefficiency is due to the data structure used to store every set of combinations.\n