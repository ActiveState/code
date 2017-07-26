import sys


class Super(object):
    """
    >>> class A(object):
    ...     def a(self):
    ...         print "A.a()"

    >>> class B(A):
    ...     def a(self):
    ...         print "B.a()"
    ...         super.a()

    >>> b = B()
    >>> b.a()
    B.a()
    A.a()

    >>> class C(B):
    ...     def a(self):
    ...         print "C.a()"
    ...         super.a()

    >>> c = C()
    >>> c.a()
    C.a()
    B.a()
    A.a()
    """

    def __getattribute__(self, name):
        frame = sys._getframe(1)
        code = frame.f_code
        if code.co_argcount < 1:
            raise TypeError("super used in wrong context")
        caller_obj = frame.f_locals[code.co_varnames[0]]

        caller_class = None
        for c in type(caller_obj).__mro__:
            try:
                func_code = getattr(c, name).func_code
            except AttributeError:
                func_code = None

            if func_code is code:
                caller_class = c
            elif caller_class is not None:
                break
        else:
            raise TypeError("super used in wrong context")

        super_obj = __builtins__.super(caller_class, caller_obj)
        return getattr(super_obj, name)

super = Super()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
