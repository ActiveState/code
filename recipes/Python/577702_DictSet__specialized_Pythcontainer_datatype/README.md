## DictSet - A specialized Python container datatype for managing collections of sets.

Originally published: 2011-05-18 21:18:54
Last updated: 2011-05-18 21:18:54
Author: Roger Lew

The basic Python container types (dict, list, set, and tuple) are extremely versatile and powerful. The collections module first implemented in Python 2.4 has shown that sub-classing these containers can yield elegant solutions to the right problem. In a similar vein this project is a dict subclass for elegantly handling collections of sets. In many aspects a DictSet is similiar to a defaultdict of sets except it generalizes many of the set operations to the dict.\n\nPut simply, DictSet is a dict of sets that behaves like a set.\n\nDictSet requires 0 non-standard dependencies and should work with Python 2.5 and up.