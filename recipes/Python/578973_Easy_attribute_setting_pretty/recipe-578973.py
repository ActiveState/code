"""Mix-in classes for easy attribute setting and pretty representation

>>> class T(HasInitableAttributes, HasTypedAttributes, IsCallable):
...     spam = str
...     def __init__(self, eggs, ham = 'ham'): pass
...
>>> t = T('bacon'); t(ham = 'eggs'); t.spam += 'sausage'; t
__main__.T('bacon', ham = 'eggs', spam = 'sausage')
>>> 
"""

from inspect import getargspec
from itertools import chain


class HasInitableAttributes(object):
    """Initializes attributes automatically

    >>> class T(HasInitableAttributes):
    ...     z = 0
    ...     def __init__(self, x, y=0, **opts): pass
    ...
    >>> t = T(0, a = 1); t
    __main__.T(0, a = 1)
    >>> t.x, t.y, t.z = 1, 2, 3; t
    __main__.T(1, y = 2, a = 1, z = 3)
    >>> 
    """
    
    def __new__(cls, *pars, **opts):
        "Initialize all attributes in the signature and any other options supplied"
        try:
            self = super().__new__(cls, *pars, **opts)
        except:
            self = super().__new__(cls)
        self._argspec = names, parsname, optsname, defaults = getargspec(self.__init__)
        if not defaults: defaults = []
        n = len(names) - len(defaults) - 1
        if n - len(pars) > 0:
            _s, _to = ('s', '-%d' % (n-1)) if n - len(pars) > 1 else ('', '')
            missing =  "%s %s (pos %d%s)" % (_s, ", ".join(names[1:n+1]), len(pars), _to)
            raise TypeError("Required argument%s not found." % missing)
        for n, v in chain(zip(names[-len(defaults):], defaults), zip(names[1:], pars), opts.items()):
            setattr(self, n, v)
        return self
    
    def __repr__(self):
        "Show all attributes in the signature and any other public attributes that are changed"
        names, parsname, optsname, defaults = self._argspec
        if not defaults: defaults = []
        optnames = names[-len(defaults):] if defaults else []
        optvalues = (getattr(self, name) for name in optnames)
        othernames = sorted(set((n for n in self.__dict__ if n[0] != '_')) - set(names))
        othervalues = list((getattr(self, name, None) for name in othernames))
        otherdefaults = list((getattr(self.__class__, name, None) for name in othernames))
        return "%s.%s(%s)" % (self.__module__, self.__class__.__name__, ", ".join(chain(
            (repr(getattr(self, name)) for name in names[1:len(names)-len(defaults)]),
            ("%s = %r" % (name, value) for name, value, default in zip(optnames, optvalues, defaults) if value != default),
            ("%s = %r" % (name, value) for name, value, default in zip(othernames, othervalues, otherdefaults) if value != default))))


class HasTypedAttributes(object):
    """Objectifies class attributes automatically

    >>> class T(HasTypedAttributes):
    ...     spam = str
    ...     class C(HasTypedAttributes):
    ...         eggs = list
    ...
    >>> a, b = T(), T(); a.spam += 'ham'; a.C.eggs.append('bacon'); a.spam, b.spam, a.C.eggs, b.C.eggs
    ('ham', '', ['bacon'], [])
    >>> 
    """

    def __new__(cls, *pars, **opts):
        try:
            self = super().__new__(cls, *pars, **opts)
        except:
            self = super().__new__(cls)
        for name in dir(self):
            if name[0] != '_':
                value = getattr(self, name)
                if isinstance(value, type):
                    setattr(self, name, value(opts.pop(name)) if name in opts else value())
        if opts:
            raise TypeError("__init__() got%s unexpected keyword argument%s %r" % 
                (" an", "", opts.keys()[0]) if len(opts) == 1 else ("", "s", opts.keys()))
        return self


class IsCallable(object):
    """Update attributes by calling

    >>> class T(IsCallable):
    ...     x = 0
    ...
    >>> t = T(); t(x=1, y=2); t.x, t.y
    (1, 2)
    """

    def __call__(self, *pars, **opts):
        self.__dict__.update(*pars, **opts)


if __name__ == '__main__':
    from doctest import testmod
    testmod()
    class T(HasInitableAttributes, HasTypedAttributes, IsCallable):
        spam = str
    t = T()
    assert t.spam != str
