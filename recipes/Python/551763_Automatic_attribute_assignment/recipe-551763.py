from functools import wraps
from inspect import getargspec, isfunction
from itertools import izip, ifilter, starmap

def autoassign(*names, **kwargs):
    """
    autoassign(function) -> method
    autoassign(*argnames) -> decorator
    autoassign(exclude=argnames) -> decorator
    
    allow a method to assign (some of) its arguments as attributes of
    'self' automatically.  E.g.
    
    >>> class Foo(object):
    ...     @autoassign
    ...     def __init__(self, foo, bar): pass
    ... 
    >>> breakfast = Foo('spam', 'eggs')
    >>> breakfast.foo, breakfast.bar
    ('spam', 'eggs')
    
    To restrict autoassignment to 'bar' and 'baz', write:
    
        @autoassign('bar', 'baz')
        def method(self, foo, bar, baz): ...

    To prevent 'foo' and 'baz' from being autoassigned, use:

        @autoassign(exclude=('foo', 'baz'))
        def method(self, foo, bar, baz): ...
    """
    if kwargs:
        exclude, f = set(kwargs['exclude']), None
        sieve = lambda l:ifilter(lambda nv: nv[0] not in exclude, l)
    elif len(names) == 1 and isfunction(names[0]):
        f = names[0]
        sieve = lambda l:l
    else:
        names, f = set(names), None
        sieve = lambda l: ifilter(lambda nv: nv[0] in names, l)
    def decorator(f):
        fargnames, _, _, fdefaults = getargspec(f)
        # Remove self from fargnames and make sure fdefault is a tuple
        fargnames, fdefaults = fargnames[1:], fdefaults or ()
        defaults = list(sieve(izip(reversed(fargnames), reversed(fdefaults))))
        @wraps(f)
        def decorated(self, *args, **kwargs):
            assigned = dict(sieve(izip(fargnames, args)))
            assigned.update(sieve(kwargs.iteritems()))
            for _ in starmap(assigned.setdefault, defaults): pass
            self.__dict__.update(assigned)
            return f(self, *args, **kwargs)
        return decorated
    return f and decorator(f) or decorator

#---------- Examples of use ------------------

>>> class Test(object): 
...      @autoassign('foo', 'bar')
...      def __init__(self, foo, bar=3, baz=6):
...          "some clever stuff going on here"
...          print 'baz =', baz 
... 
>>> class Test2(object):
...     @autoassign
...     def __init__(self, foo, bar): pass
... 
>>> class Test3(object):
...     @autoassign(exclude=('foo', 'bar'))
...     def __init__(self, foo, bar, baz=5, **kwargs): pass
... 
>>> t = Test(1, 2, 5) 
baz = 5
>>> u = Test(foo=8)
baz = 6
>>> v = Test2(10, 11)
>>> w = Test3(100, 101, foobar=102)
>>> 
>>> print Test.__init__.__doc__
some clever stuff going on here
>>> 
>>> print t.foo
1
>>> print t.bar
2
>>> 
>>> print u.foo
8
>>> print u.bar
3
>>> 
>>> print v.foo, v.bar # 10 11
10 11
>>> print w.baz, w.foobar # 5 102
5 102
>>> for obj, attr in ('w', 'foo'), ('w', 'bar'), ('t', 'baz'):
...     try:
...         getattr(globals()[obj], attr)
...     except AttributeError:
...         print '%s.%s raises AttributeError' % (obj, attr)
... 
w.foo raises AttributeError
w.bar raises AttributeError
t.baz raises AttributeError
>>>
