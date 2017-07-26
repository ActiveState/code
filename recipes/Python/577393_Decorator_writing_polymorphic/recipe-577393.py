import functools

class Namespace(object):
    pass

def poly(**poly_kw):
    """a decorator for writing polymorphic functions

Python 3 makes a clean separation between unicode text strings (str) and byte
strings (bytes). However, for some tasks (notably networking), it makes sense
to apply the same process to str and bytes, usually relying on the byte string
beeing encoded with an ASCII compatible encoding.

In this context, a polymorphic function is one which will operate on unicode
strings (str) or bytes objects (bytes) depending on the type of the arguments.
The common difficulty is that string constants used in the function also have
to be of the right type. This decorator helps by allowing to use a different
set of constants depending on the type of the argument.

In order to unambiguously determine the right type to operate, there are
restrictions on the type of the arguments; not respecting them leads to
a runtime exception (TypeError) beeing raised:
1) at least one positional argument has to be str or bytes.
2) all positional arguments that are either str or bytes have to be of the
   same type.

The decorator only accepts keyword arguments. Each of them must be a sequence,
where the first item is the value to be used with str, the second with bytes.
The decorated function will be passed a namespace object as the first
positional argument. For each keyword argument of the decorator, the namespace
will have an attribute with the same name, and the appropriate item as a value.

>>> @poly(sep=("/",b"/"))
... def joinpath(p, first, second):
...     return p.sep.join((first, second))
...
>>> joinpath('a','b')
'a/b'
>>> joinpath(b'a',b'b')
b'a/b'
>>> joinpath(1,2)
Traceback (most recent call last):
    ...
TypeError: Polymorphic function called without a str or bytes argument
>>> joinpath('a', b'b')
Traceback (most recent call last):
    ...
TypeError: Polymorphic function called with mixed types

"""

    str_ns, bytes_ns = Namespace(), Namespace()

    for k in poly_kw:
        setattr(str_ns, k, poly_kw[k][0])
        setattr(bytes_ns, k, poly_kw[k][1])

    def outer(fun):

        def inner(*args, **kwargs):

            ns = None

            for a in args:

                if isinstance(a, str):
                    
                    if ns is None:
                        ns = str_ns

                    elif ns is bytes_ns:
                        raise TypeError("Polymorphic function called with mixed types")

                if isinstance(a, bytes):

                    if ns is None:
                        ns = bytes_ns

                    elif ns is str_ns:
                        raise TypeError("Polymorphic function called with mixed types")

            if ns is None:
                raise TypeError("Polymorphic function called without a str or bytes argument")

            else:
                return fun(ns, *args, **kwargs)

        functools.update_wrapper(inner, fun)

        return inner

    return outer
