## Find cyclical references

Originally published: 2007-06-29 08:54:52
Last updated: 2007-06-29 08:54:52
Author: Michael Droettboom

This recipe helps find cyclical references in Python code to a] optimize so the garbage collector doesn't have to work as hard, and b] deal with uncollectable objects, such as those with a __del__ method, or extension objects that don't participate in garbage collection.