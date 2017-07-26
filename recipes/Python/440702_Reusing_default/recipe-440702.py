import inspect
import itertools as it
from collections import deque

__all__ = ['defaultsfrom']

#======= demos ===============================================================

def demo_func():
    '''Reuse function default values.'''

    def genericsort(iterable, cmp=None, key=None, reverse=False):
        raise NotImplementedError()

    @defaultsfrom(genericsort)
    def timsort(iterable, cmp, key, reverse):
        return sorted(iterable, cmp, key, reverse)

    s = ['hello', 'WORLD']
    timsort(s)
    timsort(s, key=str.lower)


def demo_class():
    '''Reuse method default values.'''

    import logging
    class GenericLogger(object):
        def __init__(self, name, level=logging.WARNING, handlers=(), 
                     filters=()):
            self._logger = logging.getLogger(name)
            self._logger.setLevel(level)
            for h in handlers: self._logger.addHandler(h)
            for f in filters: self._logger.addFilter(f)


    class FancyLogger(GenericLogger):

        @defaultsfrom(GenericLogger)
        def __init__(self, name, level, handlers, filters, bells=None,
                     whistles=None, debug=False):
            super(FancyLogger,self).__init__(name, level, handlers, filters)
            for attr in 'bells', 'whistles', 'debug':
                setattr(self, '_'+attr, eval(attr))

    mylog = FancyLogger('demo', filters=[logging.Filter()], debug=True)


#======= defaultsfrom ========================================================

def defaultsfrom(funcOrClass):
    '''Return a decorator d so that d(func) updates func's default arguments.

    If funcOrClass is a function (or method) 'foo', its default arguments are
    'inherited' by any function 'bar' decorated by the returned decorator:

    >>> def foo(a, x=0, y=''): pass
    >>> @defaultsfrom(foo)
    ... def bar(a, b, y, x, z=None): return a,b,y,x,z
    >>> bar(1,2,3,4,5)
    (1, 2, 3, 4, 5)
    >>> bar(1,2,3,4)
    (1, 2, 3, 4, None)
    >>> bar(1,2,3)
    (1, 2, 3, 0, None)
    >>> bar(1,2)
    (1, 2, '', 0, None)

    Any default arguments redefined by 'bar' are not inherited by 'foo':
    >>> @defaultsfrom(foo)
    ... def zong(a, x, y=-1): # y redefined
    ...     return a,x,y
    >>> zong(2)
    (2, 0, -1)

    Default arguments (inherited or not) cannot precede non-default ones:
    >>> @defaultsfrom(foo)
    ... def zap(a, x, b, y): # b is not a default arg; x cannot be inherited
    ...     return a,x,b,y
    Traceback (most recent call last):
        ...
    TypeError: ...

    If funcOrClass is a class, its method with the same name with the
    decorated function is handled as above:
    >>> class Base(object):
    ...    def __init__(self, a, b=0, c=None): pass
    >>> class Derived(Base):
    ...    @defaultsfrom(Base)  # equivalent to Base.__init__
    ...    def __init__(self, a, b, c): print (a,b,c)
    >>> d = Derived(1)
    (1, 0, None)
    '''

    def decorator(newfunc):
        if inspect.isclass(funcOrClass):
            func = getattr(funcOrClass, newfunc.__name__)
        else:
            func = funcOrClass
        args,_,_,defaults = inspect.getargspec(func)
        # map each default argument of func to its value
        arg2default = dict(zip(args[-len(defaults):],defaults))
        newargs,_,_,newdefaults = inspect.getargspec(newfunc)
        if newdefaults is None: newdefaults = ()
        nondefaults = newargs[:len(newargs)-len(newdefaults)]
        # starting from the last non-default argument towards the first, as
        # long as the non-defaults of newfunc are default in func, make them
        # default in newfunc too
        iter_nondefaults = reversed(nondefaults)
        newdefaults = deque(newdefaults)
        for arg in it.takewhile(arg2default.__contains__, iter_nondefaults):
            newdefaults.appendleft(arg2default[arg])
        # all inherited defaults should be placed together; no gaps allowed
        for arg in it.ifilter(arg2default.__contains__, iter_nondefaults):
            raise TypeError('%s cannot inherit the default arguments of '
                            '%s' % (newfunc, func))
        newfunc.func_defaults = tuple(newdefaults)
        return newfunc
    return decorator


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
    demo_func()
    demo_class()
