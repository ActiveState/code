## Records  
Originally published: 2008-11-04 06:52:42  
Last updated: 2008-11-04 06:52:42  
Author: George Sakkis  
  
This is a recipe similar in functionality and exec-style optimized implementation to the very well received namedtuple (http://code.activestate.com/recipes/500261/) that was included in Python 2.6. The main difference is that **records**, unlike named tuples, are mutable. In addition, fields can have a default value. Instead of subclassing tuple or list, the implementation create a regular class with __slots__.