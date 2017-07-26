## (Yet another) Assignment in expression RecipeOriginally published: 2011-12-17 12:50:41 
Last updated: 2011-12-17 20:03:26 
Author: harish anand 
 
Python does not support assignment in if and while statements such as "if (x=func()):". This is an attempt to bring similar functionality to python by injecting bytecode to all functions and methods in a module.\nThis recipe is inspired from recipes [66061](http://code.activestate.com/recipes/66061), [202234](http://code.activestate.com/recipes/202234-assignment-in-expression) and [277940](http://code.activestate.com/recipes/277940-decorator-for-bindingconstants-at-compile-time).