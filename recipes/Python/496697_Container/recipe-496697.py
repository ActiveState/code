def recursion_lock(retval, lock_name = "____recursion_lock"):
    def decorator(func):
        def wrapper(self, *args, **kw):
            if getattr(self, lock_name, False):
                return retval
            setattr(self, lock_name, True)
            try:
                return func(self, *args, **kw)
            finally:
                setattr(self, lock_name, False)
        return wrapper
    return decorator

class Container(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)
    @recursion_lock("<...>")
    def __repr__(self):
        attrs = sorted("%s = %r" % (k, v) for k, v in self.__dict__.iteritems() if not k.startswith("_"))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(attrs))
    @recursion_lock("<...>")
    def __str__(self, nesting = 1):
        attrs = []
        indentation = "    " * nesting
        for k, v in self.__dict__.iteritems():
            if not k.startswith("_"):
                text = [indentation, k, " = "]
                if isinstance(v, Container):
                    text.append(v.__str__(nesting + 1))
                else:
                    text.append(repr(v))
                attrs.append("".join(text))
        attrs.sort()
        attrs.insert(0, self.__class__.__name__ + ":")
        return "\n".join(attrs)

---------
example:
---------

>>> c = Container(a=1, b="baaa")
>>> c # calls repr()
Container(a = 1, b = 'baaa')
>>> print c # calls str()
Container:
    a = 1
    b = 'baaa'
>>> c.c = 1.23
>>> print c
Container:
    a = 1
    b = 'baaa'
    c = 1.23
>>> c.d = Container(e = 6, f = "g")
>>> c
Container(a = 1, b = 'baaa', c = 1.23, d = Container(e = 6, f = 'g'))
>>> print c
Container:
    a = 1
    b = 'baaa'
    c = 1.23
    d = Container:
        e = 6
        f = 'g'
>>> c.h = c # recursive referencing
>>> c
Container(a = 1, b = 'baaa', c = 1.23, d = Container(e = 6, f = 'g'), h = <...>)
>>> print c
Container:
    a = 1
    b = 'baaa'
    c = 1.23
    d = Container:
        e = 6
        f = 'g'
    h = <...>
>>>
