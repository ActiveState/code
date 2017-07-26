###Using decorators to load data structures

Originally published: 2005-03-28 07:02:10
Last updated: 2005-03-28 07:02:10
Author: Scott David Daniels

Decorators can be used to load data structures with a function.  Using this technique can reduce the 'lots of declarations; large table definition; startup' structure of some larger programs.  The insight is remembering that a decorator can return the original function unchanged.