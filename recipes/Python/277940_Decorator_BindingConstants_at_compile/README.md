## Decorator for BindingConstants at compile time  
Originally published: 2004-04-13 04:42:35  
Last updated: 2010-11-16 08:36:38  
Author: Raymond Hettinger  
  
Decorator for automatic code optimization.  If a global is known at compile time, replace it with a constant.  Fold tuples of constants into a single constant.  Fold constant attribute lookups into a single constant.