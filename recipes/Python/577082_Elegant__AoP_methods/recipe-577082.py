import functools
import sys
import types


def advise(*join_points):
    """Hook advice to a function or method.

    advise() is a decorator that takes a set of functions or methods and
    injects the decorated function in their place. The decorated function should
    have the signature:

        @advise(some_function, Class.some_method, Class.some_class_method,
                Class.some_static_method, ...)
        def interceptor(on, next, *args, **kwargs):
            ...

    Where "on" is the object that hosts the intercepted function (ie. a module,
    class or instance) and "next" is the next function in the interception
    chain.

    >>> def eat(lunch):
    ...   print 'eating', lunch

    >>> @advise(eat)
    ... def replace_sandwich(on, next, lunch):
    ...   if lunch == 'sandwich':
    ...     print 'delicious sandwich!'
    ...     return next('dirt')
    ...   else:
    ...     return next(lunch)

    >>> eat('soup')
    eating soup

    >>> eat('sandwich')
    delicious sandwich!
    eating dirt

    >>> class Eater(object):
    ...   def eat(self):
    ...     print 'tastes like identity!'
    ...   @classmethod
    ...   def eat_class(cls):
    ...     print 'let them eat cake!'
    ...   @staticmethod
    ...   def eat_static():
    ...     print 'mmm, static cling'
    ...   def eat_instance(self):
    ...     print 'a moment in time'

    >>> eater = Eater()

    Multiple functions can be intercepted in one call to @advise, including
    classmethods and staticmethods:

    >>> @advise(Eater.eat, Eater.eat_class, Eater.eat_static, eater.eat_instance)
    ... def delicious(on, next):
    ...   print 'delicious!'
    ...   return next()

    Normal method intercepted on the class:

    >>> Eater().eat()
    delicious!
    tastes like identity!

    Normal method intercepted on the instance:

    >>> eater.eat_instance()
    delicious!
    a moment in time

    Class method:

    >>> Eater.eat_class()
    delicious!
    let them eat cake!

    Static method:

    >>> Eater.eat_static()
    delicious!
    mmm, static cling

    Functions can be intercepted multiple times:

    >>> @advise(Eater.eat)
    ... def intercept(on, next):
    ...   print 'intercepted...AGAIN'
    ...   return next()

    >>> Eater().eat()
    intercepted...AGAIN
    delicious!
    tastes like identity!

    """
    hook = []
    def hook_advice(join_point):
        def intercept(*args, **kwargs):
            return hook[0](on, join_point, *args, **kwargs)
        intercept = functools.update_wrapper(intercept, join_point)

        # Either a normal method or a class method?
        if type(join_point) is types.MethodType:
            # Class method intercept or instance intercept
            if join_point.im_self:
                on = join_point.im_self
                # If we have hooked onto an instance method...
                if type(on) is type:
                    def intercept(cls, *args, **kwargs):
                        return hook[0](cls, join_point, *args, **kwargs)
                    intercept = functools.update_wrapper(intercept, join_point)
                    intercept = classmethod(intercept)
            else:
                # Normal method, we curry "self" to make "next" uniform
                def intercept(self, *args, **kwargs):
                    curry = functools.update_wrapper(
                        lambda *a, **kw: join_point(self, *a, **kw), join_point)
                    return hook[0](self, curry, *args, **kwargs)
                intercept = functools.update_wrapper(intercept, join_point)
                on = join_point.im_class
        else:
            # Static method or global function
            on = sys.modules[join_point.__module__]
            caller_globals = join_point.func_globals
            name = join_point.__name__
            # Global function
            if caller_globals.get(name) is join_point:
                caller_globals[name] = intercept
            else:
                # Probably a staticmethod, try to find the attached class
                for on in caller_globals.values():
                    if getattr(on, name, None) is join_point:
                        intercept = staticmethod(intercept)
                        break
                else:
                    raise ValueError('%s is not a global scope function and '
                                     'could not be found in top-level classes'
                                     % name)
        name = join_point.__name__
        setattr(on, name, intercept)

    for join_point in join_points:
        hook_advice(join_point)

    def add_hook(func):
        hook.append(func)
        return func
    return add_hook


if __name__ == '__main__':
    import doctest
    doctest.testmod()
