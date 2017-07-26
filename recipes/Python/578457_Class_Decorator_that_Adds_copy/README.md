## A Class Decorator that Adds a copy() Method  
Originally published: 2013-02-14 20:43:19  
Last updated: 2013-02-14 20:43:20  
Author: Eric Snow  
  
Here's a class decorator that adds a rudimentary copy() method onto the decorated class.  Use it like this:

    @copiable
    class SomethingDifferent:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

or like this:

    @copiable("a b c")
    class SomethingDifferent:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

    s = SomethingDifferent(1,2,3)
    sc = s.copy()
    assert vars(s) == vars(sc)

(Python 3.3)