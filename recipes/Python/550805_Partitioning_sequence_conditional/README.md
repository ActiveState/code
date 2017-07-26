## Partitioning a sequence by a conditional function

Originally published: 2008-03-01 13:58:25
Last updated: 2008-03-01 13:58:25
Author: Aaron Gallagher

This function takes a sequence and a function and returns two generators. The first generator yields all items in the sequence for which function(item) returns True, and the second generator yields all items for which function(item) returns False.