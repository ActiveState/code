## Singleton (parameter based)  
Originally published: 2012-04-12 07:38:27  
Last updated: 2012-04-18 06:13:25  
Author: Thomas Lehmann  
  
**Why?**
 * There are many recipes but nearly all cover the global singleton only.
 * I need a singleton which can handle things in a specific context (environment).

**The final singleton is a combination of following two recipes**:
 * http://www.python.org/dev/peps/pep-0318/#examples
 * http://stackoverflow.com/a/9489387

**The basic advantages**:
 * Hiding the singleton code by a simple decorator
 * Flexible, because you can define fully global singletons or parameter based singletons.

**Latest changes**:
 * Although a function/method does not have parameters you can call it with parameters **args** and **kwargs** as you now see in the **getInstance** function.
 * ...