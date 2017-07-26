## Thread-safe caching object with file and HTTP implementations  
Originally published: 2004-09-01 13:26:41  
Last updated: 2006-02-08 10:04:16  
Author: Nicolas Lehuen  
  
Implementation of an abstract, thread-safe cache with minimal locking. Four concrete implementations : a validating file cache, a validating HTTP cache, an experimental Python module cache and a function cache. Plus, an abstract cache with weak references to its values.