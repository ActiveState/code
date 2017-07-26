## Using ChainMap for embedded namespaces

Originally published: 2012-10-03 17:59:50
Last updated: 2012-10-03 18:12:50
Author: Steven D'Aprano

The Zen of Python tells us:\n\n*Namespaces are one honking great idea -- let's do more of those!*\n\nPython already has an excellent namespace type, the module, but the problem with modules is that they have to live in a separate file, and sometimes you want the convenience of a single file while still encapsulating your code into namespaces. That's where classes are the usual solution, but classes need to be instantiated and methods need to be defined with a `self` parameter.\n\nC++ has "namespaces" for encapsulating related objects and dividing the global scope into sub-scopes. Can we do the same in Python?\n\nWith a bit of metaclass trickery and the new ChainMap type from Python 3.3, we can!\n