## freeze(), make any object immutable  
Originally published: 2008-10-04 12:38:48  
Last updated: 2008-10-04 14:39:20  
Author: Andreas Nilsson  
  
Calling freeze() on an object makes the object immutable, like const in C++. Useful if you want to make sure that a function doesn't mess with the parameters you pass to it.

Basic usage:

    class Foo(object):
        def __init__(self):
            self.x = 1

    def bar(f):
        f.x += 1

    f = Foo()
    bar(freeze(f)) #Raises an exception