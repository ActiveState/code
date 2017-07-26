## A Class Decorator that Adds a copy() MethodOriginally published: 2013-02-14 20:43:19 
Last updated: 2013-02-14 20:43:20 
Author: Eric Snow 
 
Here's a class decorator that adds a rudimentary copy() method onto the decorated class.  Use it like this:\n\n    @copiable\n    class SomethingDifferent:\n        def __init__(self, a, b, c):\n            self.a = a\n            self.b = b\n            self.c = c\n\nor like this:\n\n    @copiable("a b c")\n    class SomethingDifferent:\n        def __init__(self, a, b, c):\n            self.a = a\n            self.b = b\n            self.c = c\n\n    s = SomethingDifferent(1,2,3)\n    sc = s.copy()\n    assert vars(s) == vars(sc)\n\n(Python 3.3)