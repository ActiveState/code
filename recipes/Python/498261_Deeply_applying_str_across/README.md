## Deeply applying str() across a data structure 
Originally published: 2006-11-10 20:31:03 
Last updated: 2006-11-12 03:23:54 
Author: Danny Yoo 
 
The str() in the standard library behaves in a slightly weird way when applied against lists: on each element of the list, the repr() is appended.  In contrast, this module provides a deep_str() that deeply applies str() across lists.