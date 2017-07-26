## A memoize decorator for instance methods

Originally published: 2010-11-03 20:26:10
Last updated: 2010-11-04 20:23:35
Author: Daniel Miller

A simple result-caching decorator for instance methods. NOTE: does not work with plain old non-instance-method functions. The cache is stored on the instance to prevent memory leaks caused by long-term caching beyond the life of the instance (almost all other recipes I found suffer from this problem when used with instance methods).