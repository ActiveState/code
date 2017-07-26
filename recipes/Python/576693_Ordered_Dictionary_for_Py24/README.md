## Ordered Dictionary for Py2.4  
Originally published: 2009-03-18 03:37:17  
Last updated: 2011-04-24 03:20:45  
Author: Raymond Hettinger  
  
Drop-in substitute for Py2.7's new collections.OrderedDict.  The recipe has big-oh performance that matches regular dictionaries (amortized O(1) insertion/deletion/lookup and O(n) iteration/repr/copy/equality_testing).