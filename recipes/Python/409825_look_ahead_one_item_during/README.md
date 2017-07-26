## look ahead one item during iteration  
Originally published: 2005-04-14 13:03:01  
Last updated: 2005-04-14 20:12:32  
Author: Wai Yip Tung  
  
Iteration is a fundamental Python idiom. It is simple and effective.

for n in iterable:
  # do something with n

But there are also cases when you might want to look ahead one item during iteration. For example, with a sorted list, one can eliminate duplicated items by dropping those equals to the next item. This generator based recipe that enumerate an item and its next in a list. For example,

>>> for i,j in pairwise([1,2,3]): print i,j
...
1 2
2 3
3 None