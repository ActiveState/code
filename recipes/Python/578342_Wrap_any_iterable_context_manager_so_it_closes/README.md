## Wrap any iterable context manager so it closes when consumed 
Originally published: 2012-11-19 20:06:05 
Last updated: 2012-11-19 20:10:35 
Author: Andrew Barnert 
 
There are a few types in Python—most notably, files—that are both iterators and context managers. For trivial cases, these features are easy to use together, but as soon as you need to use the iterator lazily or asynchronously, a with statement won't help. That's where this recipe comes in handy:\n\n    send_async(with_iter(open(path, 'r')))\n\nThis also allows you to "forward" closing for a wrapped iterator, so closing the outer iterator also closes the inner one:\n\n    sync_async(line.upper() for line in with_iter(open(path, 'r')))