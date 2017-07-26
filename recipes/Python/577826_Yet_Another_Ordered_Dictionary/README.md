## Yet Another Ordered DictionaryOriginally published: 2011-08-07 12:14:56 
Last updated: 2011-08-07 12:14:56 
Author: Lucio Santi 
 
An implementation of dictionaries preserving key insertion order. Despite using a doubly-linked list to keep track of the appropriate order, this list is actually embedded in the dictionary. As a consequence, there is little space penalty, and also every operation exhibits an efficient implementation (i.e., no need to perform lookups or deletions multiple times, as it happens with other versions of this data structure).