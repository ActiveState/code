## iter_except -- a useful variant of __builtin__.iter() 
Originally published: 2010-03-27 02:04:21 
Last updated: 2010-03-27 02:04:22 
Author: Raymond Hettinger 
 
Variant of iter(func, sentinel) that looks for an exception rather than for a sentinel value.  Good for making iterators from of APIs that advance over a data and return an exception when they are done.