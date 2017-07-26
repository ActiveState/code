## look ahead one item during iteration

Originally published: 2005-04-14 13:03:01
Last updated: 2005-04-14 20:12:32
Author: Wai Yip Tung

Iteration is a fundamental Python idiom. It is simple and effective.\n\nfor n in iterable:\n  # do something with n\n\nBut there are also cases when you might want to look ahead one item during iteration. For example, with a sorted list, one can eliminate duplicated items by dropping those equals to the next item. This generator based recipe that enumerate an item and its next in a list. For example,\n\n>>> for i,j in pairwise([1,2,3]): print i,j\n...\n1 2\n2 3\n3 None