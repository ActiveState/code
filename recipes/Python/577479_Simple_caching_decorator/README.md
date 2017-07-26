## Simple caching decorator 
Originally published: 2010-12-01 00:43:00 
Last updated: 2010-12-01 00:43:01 
Author: Raymond Hettinger 
 
Memoizing decorator.  Has the same API as the functools.lru_cache() in Py3.2 but without the LRU feature, so it takes less memory, runs faster, and doesn't need locks to keep the dictionary in a consistent state.