## deque collection class  
Originally published: 2004-01-12 00:13:36  
Last updated: 2007-07-14 11:53:06  
Author: Raymond Hettinger  
  
Pure python drop in replacement for collections.deque() from Py2.4.  See documentation at:  http://www.python.org/dev/doc/devel/lib/module-collections.html\n<br>\nUses a dictionary as the underlying data structure for the deque (pronounced "deck", short for "double-ended queue", a generalization of stacks and queues) which provides O(1) performance for appends and pops from either end.\n<br>\nRuns on PyPy, Jython, and older Pythons.