## Fast Indexing functions (greater than, less than, equal to, and not equal to)  
Originally published: 2012-03-13 16:18:10  
Last updated: 2012-03-13 16:21:36  
Author: Garrett   
  
Oftentimes you want to find the index of a list-like object.  Numpy arrays, for example, do not have a index member function.  These get the job done quickly.

Note: these do not raise exceptions, instead they return -1 on error.  You should change that if you want different behavior.