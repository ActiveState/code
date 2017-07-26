## Implementation of sets using sorted lists 
Originally published: 2003-10-21 23:24:22 
Last updated: 2007-05-19 07:07:23 
Author: Raymond Hettinger 
 
Inspired by Py2.3's TimSort, this implementation of sets.py uses sorted lists instead of dictionaries.  For clumped data patterns, the set operations can be super-efficient (for example, two sets can be determined to be disjoint with only O(n) comparisons).  Also note, that the set elements are *not* required to be hashable; this provides a great deal more freedom than dictionary based implementations.