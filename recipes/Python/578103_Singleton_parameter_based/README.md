###Singleton (parameter based)

Originally published: 2012-04-12 07:38:27
Last updated: 2012-04-18 06:13:25
Author: Thomas Lehmann

**Why?**\n * There are many recipes but nearly all cover the global singleton only.\n * I need a singleton which can handle things in a specific context (environment).\n\n**The final singleton is a combination of following two recipes**:\n * http://www.python.org/dev/peps/pep-0318/#examples\n * http://stackoverflow.com/a/9489387\n\n**The basic advantages**:\n * Hiding the singleton code by a simple decorator\n * Flexible, because you can define fully global singletons or parameter based singletons.\n\n**Latest changes**:\n * Although a function/method does not have parameters you can call it with parameters **args** and **kwargs** as you now see in the **getInstance** function.\n * ...