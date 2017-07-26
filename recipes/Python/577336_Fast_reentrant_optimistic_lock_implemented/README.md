## Fast, re-entrant, optimistic lock implemented in CythonOriginally published: 2010-07-27 19:06:11 
Last updated: 2010-07-27 20:25:20 
Author: Stefan Behnel 
 
This is a C-level implementation of a fast, re-entrant, optimistic lock for CPython. It is written in Cython. Under normal conditions, it is about 10x faster than threading.RLock because it avoids all locking unless two or more threads try to acquire it at the same time. Under congestion, it is still about 10% faster than RLock due to being implemented in Cython.