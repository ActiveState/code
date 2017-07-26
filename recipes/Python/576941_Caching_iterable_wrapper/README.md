## Caching iterable wrapper 
Originally published: 2009-11-01 12:29:33 
Last updated: 2009-11-06 11:38:43 
Author: Ulrik Sverdrup 
 
This is a very simple wrapper of an iterator or iterable, such that the iterator can be iterated streamingly without generating all elements or any at all, but the object can still be iterated from the beginning as many times as wanted. In effect, it is a streamingly loaded list.