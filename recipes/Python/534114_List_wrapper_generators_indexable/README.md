## List wrapper for generators (indexable, subscriptable)  
Originally published: 2007-10-15 13:25:13  
Last updated: 2007-10-19 08:53:32  
Author: Florian Leitner  
  
Similar to <a href="http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/523026">Andrew Moffat's recipe</a>, this class takes a generator function as an argument and returns a list object where the generator's items can be accessed by indices (as indices or slices). Only once a certain index value was requested, it actually iterates the generator to that point. See docstrings for more. The values are stored in a Berkeley DB which is created in a temporary file on the fly (it would not need much to modify the code to store in memory if you would prefer that) in such a manner that for any object where id(obj1) == id(obj2) is True, only one entry is stored.