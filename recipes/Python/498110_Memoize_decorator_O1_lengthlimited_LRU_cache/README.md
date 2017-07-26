## Memoize decorator with O(1) length-limited LRU cache, supports mutable types  
Originally published: 2006-09-17 15:03:25  
Last updated: 2006-09-17 15:03:25  
Author: Neil Toronto  
  
There are quite a few memoize decorators floating around, but none that met all my requirements. Here's my attempt. It draws from Bengt Richter's O(1) length-limited LRU cache (http://mail.python.org/pipermail/python-list/2002-October/125872.html) and a simplification of Daniel Brodie's Simple Decorators recipe (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/437086).