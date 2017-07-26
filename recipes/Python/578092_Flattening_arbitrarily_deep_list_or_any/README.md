## Flattening an arbitrarily deep list (or any iterator)

Originally published: 2012-04-03 16:21:31
Last updated: 2012-04-03 17:13:35
Author: Garrett 

What if you had a list like this: [1, -10, [1,2,[3,4]], xrange(200)], and you just wanted to go through each element in order (wanted it to return a simple list of [1,-10,1,2,3,4,1,2,3,4...199])\n\nI've seen a couple of attempts to flatten arbitrarily deep lists.  Many of them involve recursion, like this one: http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html\n\nRecursion is generally considered non-pythonic (at least to my knowledge), so I have used one which just involves simple iterators instead.  Also, recursion will fail if the list is too deep (so it wouldn't really be arbitrary, would it?).