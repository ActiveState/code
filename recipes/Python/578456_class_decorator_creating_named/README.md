## A class decorator for creating named tuples  
Originally published: 2013-02-14 18:47:08  
Last updated: 2013-02-14 19:58:13  
Author: Eric Snow  
  
This class decorator factory is useful for replacing the following:

    class MyTuple(namedtuple('MyTuple', "a b c")):
        """Something special."""
        @classmethod
        def from_defaults(cls, a, b=None, c=5):
            return cls(a, b, c)

or even:

    class MyTuple(namedtuple('MyTuple', "a b c")):
        """Something special."""
        def __new__(cls, a, b=None, c=5):
            return super().__new__(cls, a, b, c)

with this:

    @as_namedtuple("a b c", None, c=5)
    class MyTuple:
        """Something special."""

I found that I often subclass named tuples to add on some functionality or even just a nice docstring.  Plus with the class syntax there's no missing that a class is bound to the name (and it's a little easier to search for the definition).  When you subclass a named tuple the boilerplate involved really jumps out.

One of the main reasons Adding support for defaults to namedtuple would mitigate the need for that functionality here, but I'm not going to hold my breath on that.

One nice (though minor) thing is that you don't have to repeat the name when defining the namedtuple.