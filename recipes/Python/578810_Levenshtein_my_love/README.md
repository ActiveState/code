## Levenshtein, my love  
Originally published: 2014-01-15 07:39:39  
Last updated: 2014-01-15 09:14:30  
Author: yota   
  
*be kind and comment, especially if you downvote*

**levenshtein_distance()** is an implementation of the iterative algorithm for the levenshtein distance (cf. http://en.wikipedia.org/wiki/Levenshtein_distance#Iterative_with_full_matrix)

**levenshtein_sequence()** is an attempt to retrieve one of the levenshtein paths (the one that give priority to substitution, deletion, insertion, in this order). The result is a list of tuples made of:
1. the operation ( `=`, `-`, `+`, `*` for respectively keep, delete, insert, substitute)
2. the coordinate in the first
3. and in the second string.


>>> levenshtein_sequence('saturday', 'sunday')	
[('=', 0, 0), ('-', 1, 0), ('-', 2, 0), ('=', 3, 1), ('*', 4, 2), ('=', 5, 3), ('=', 6, 4), ('=', 7, 5)]
>>> levenshtein_sequence('kitten', 'sitting')
[('*', 0, 0), ('=', 1, 1), ('=', 2, 2), ('=', 3, 3), ('*', 4, 4), ('=', 5, 5), ('+', 5, 6)]

This code is part of foreplays, in a plan I have to improve difflib with alternative SequenceMatchers \o/

*/!\ tab indented, as usual.*

