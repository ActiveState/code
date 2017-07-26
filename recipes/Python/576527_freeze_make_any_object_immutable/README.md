## freeze(), make any object immutableOriginally published: 2008-10-04 12:38:48 
Last updated: 2008-10-04 14:39:20 
Author: Andreas Nilsson 
 
Calling freeze() on an object makes the object immutable, like const in C++. Useful if you want to make sure that a function doesn't mess with the parameters you pass to it.\n\nBasic usage:\n\n    class Foo(object):\n        def __init__(self):\n            self.x = 1\n\n    def bar(f):\n        f.x += 1\n\n    f = Foo()\n    bar(freeze(f)) #Raises an exception