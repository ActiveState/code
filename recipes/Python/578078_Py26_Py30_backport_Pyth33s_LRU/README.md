## Py2.6+ and Py3.0+ backport of Python 3.3's LRU Cache 
Originally published: 2012-03-17 05:06:09 
Last updated: 2013-03-06 05:38:15 
Author: Raymond Hettinger 
 
Full-featured O(1) LRU cache backported from Python3.3.  The full Py3.3 API is supported (thread safety, maxsize, keyword args, type checking, __wrapped__, and cache_info).  Includes Py3.3 optimizations for better memory utilization, fewer dependencies, and fewer dict lookups.