## Property decorator for python 2.4Originally published: 2005-04-25 14:03:31 
Last updated: 2005-04-25 23:32:11 
Author: George Sakkis 
 
This recipe refines an older recipe on creating class properties (\nhttp://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/205183). The refinement consists of:\n- Using a decorator (introduced in python 2.4) to "declare" a function in class scope as property.\n- Using a trace function to capture the locals() of the decorated function, instead of requiring the latter to return locals(), as in the older recipe.