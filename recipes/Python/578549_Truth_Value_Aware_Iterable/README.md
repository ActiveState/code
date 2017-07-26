## Truth Value Aware Iterable

Originally published: 2013-06-04 21:25:02
Last updated: 2013-06-11 08:00:25
Author: Alan Franzoni

This small recipe enables truth value testing on iterables.\n\nIt is quite common to do things like:\n\n    if somesequence:\n        ...\n    else:\n        ...\n\nSuch constructs, that enter the if block if the sequence's got one or more elements and the else block if it's empty, work fine on non-lazy builtin sequences (lists, strings, tuples) and dictionaries as well, but doesn't necessarily work on generic iterables -  most of them are always true regardless of their contents, since they're some kind of object. A classical example is generators, but such behaviour can be extended to any object implementing the Iterable interface.\n\nJust wrap your iterable with this decorator and you'll get a truth-aware iterable which supports proper truth testing by doing a small first element prefetching and can then be used just like the original iterable.