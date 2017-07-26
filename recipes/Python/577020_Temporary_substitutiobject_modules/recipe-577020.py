from __future__ import with_statement # only needed on python 2.5

import sys
from functools import partial

def _findattr(mod, rest):
    parent, dot, rest = rest.partition('.')
    if rest:
        return _findattr(getattr(mod, parent), rest)
    else:
        return mod, parent

def find_in_module(fullname):
    modname, dot, rest = fullname.partition('.')
    module, objname = _findattr(__import__(modname), rest)
    return getattr(module, objname), partial(setattr, module, objname)


class substitute(object):
    """
    A context manager that takes the name of a globally reachable
    object (in the form of 'module.object', e.g. `sys.stdout`) and
    substitutes it with another object while the context manager is in
    effect.

    Example::

        >>> from StringIO import StringIO
        >>> capture = StringIO()
        >>> with substitute('sys.stdout', capture):
        ...     print('foo')
        >>> capture.getvalue()
        'foo\\n'

    or::

        >>> import os
        >>> with substitute('os.path.exists', lambda p: 'Yes indeedy!'):
        ...     assert os.path.exists('/no/such/path') == 'Yes indeedy!'
        >>> assert os.path.exists('/no/such/path') == False

    Exceptions are propagated after the value is restored::

        >>> import os
        >>> with substitute('os.environ', {}):
        ...    os.environ['PATH']
        Traceback (most recent call last):
        KeyError
    """

    def __init__(self, name, substitution):
        self.name = name
        self.substitution = substitution

    def __enter__(self):
        self.oldvalue, self._set = find_in_module(self.name)
        self._set(self.substitution)
        return self

    def __exit__(self, exc, value, tb):
        self._set(self.oldvalue)
        if tb is not None:
            raise(exc, value, tb)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
