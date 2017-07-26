## Yielding out of nested routines by metaclass transformationOriginally published: 2006-11-16 20:04:07 
Last updated: 2006-11-17 04:16:35 
Author: Bernhard Mulder 
 
Python 2.5 improved the support for generators, making it easier to\nuse coroutines. If you want to use coroutines, however, you can not\ntransfer control out of nested functions. You can eliminate this\nrestriction by systematically converting regular functions into\ngenerator functions as demonstrated by this recipe http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/474127 The script below might\nserve as a starting point to do this transformation automatically,\nmaking the use of coroutines (tasklets, lightweight threads...) more\nnatural.