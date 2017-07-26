# collections.namedtuple, backported to Python 2.4, with a twist.
#
# This should be tested against Python 2.4 through 2.7, but is not expected
# to work in Python 3.


from operator import itemgetter as _itemgetter
from keyword import iskeyword as _iskeyword
import sys as _sys

try:
    all, any
except NameError:
    # Only needed in Python 2.4.
    def all(iterable):
        for element in iterable:
            if not element:
                return False
        return True

    def any(iterable):
        for element in iterable:
            if element:
                return True
        return False


def _check_name(name):
    """Check type or field name is valid.

    Returns an error message if name is not valid, otherwise the
    empty string.
    """
    if not name:
        err = "names must not be empty"
    elif name[0].isdigit():
        err = "name '%s' cannot start with a digit" % name
    elif name.startswith('_'):
        err = "name '%s' cannot start with an underscore" % name
    elif not all(c.isalnum() or c == '_' for c in name):
        err = ("name '%s' must only contain alphanumeric characters"
               " and underscores" % name)
    elif _iskeyword(name):
        err = "name '%s' is a reserved keyword" % name
    else:
        err = ""
    return err


def namedtuple(typename, field_names, verbose=False, rename=False):
    """Returns a new subclass of tuple with named fields.

    >>> Point = namedtuple('Point', 'x y')
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)

    """
    if not isinstance(typename, basestring):
        raise TypeError('typename must be a string, not %r' % type(typename))
    err = _check_name(typename)
    if err:
        raise ValueError(err)

    # Parse and validate the field names. Validation serves two purposes,
    # generating informative error messages and preventing template
    # injection attacks.
    if isinstance(field_names, basestring):
        # Field names separated by whitespace and/or commas.
        field_names = field_names.replace(',', ' ').split()
    field_names = list(map(str, field_names))
    seen = set()
    for i, name in enumerate(field_names):
        err = _check_name(name)
        if not err and name in seen:
            err = "duplicate name '%s'" % name
        if err:
            if rename:
                field_names[i] = "_%d" % i
            else:
                raise ValueError(err)
        else:
            seen.add(name)
    field_names = tuple(field_names)

    # === Dynamically construct the class ===

    # Unlike Raymond Hettinger's original recipe found at
    # http://code.activestate.com/recipes/500261-named-tuples/
    # we use a regular nested class. The only method which needs to be
    # generated dynamically is __new__.

    numfields = len(field_names)
    reprtxt = ', '.join('%s=%%r' % name for name in field_names)
    argtxt = ', '.join(field_names)

    class Inner(tuple):
        # Work around for annoyance: type __doc__ is read-only :-(
        __doc__ = ("%(typename)s(%(argtxt)s)"
                   % {'typename': typename, 'argtxt': argtxt})

        __slots__ = ()
        _fields = field_names

        # Don't decorate with classmethod here. See below.
        def _make(cls, iterable, new=tuple.__new__, len=len):
            """Make a new %s object from a sequence or iterable."""
            result = new(cls, iterable)
            if len(result) != numfields:
                raise TypeError('Expected %d arguments, got %d' % (numfields, len(result)))
            return result

        # Work around for annoyance: classmethod __doc__ is read-only :-(
        _make.__doc__ %= locals()
        _make = classmethod(_make)

        def __repr__(self):
            return '%s(%s)' % (typename, reprtxt%self)

        def _asdict(self):
            """Return a new dict which maps field names to their values."""
            return dict(zip(self._fields, self))

        def _replace(self, **kwds):
            """Return a new %(typename)s object replacing specified fields with new values."""
            result = self._make(map(kwds.pop, self._fields, self))
            #result = self._make(map(kwds.pop, ('x', 'y'), _self))
            if kwds:
                raise ValueError('Got unexpected field names: %r' % kwds.keys())
            return result

        def __getnewargs__(self):
            return tuple(self)

    # For pickling to work, the __module__ attribute needs to be set to the
    # frame where the named tuple is created.  Bypass this step in enviroments
    # where sys._getframe is not defined (Jython for example) or sys._getframe
    # is not defined for arguments greater than 0 (IronPython).
    try:
        Inner.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass

    # Dynamically create the __new__ method and inject it into the class.
    # We do this using exec because the method argument handling is otherwise
    # too hard. The "cls" parameter is named _cls instead to avoid clashing
    # with a field of that same name.
    ns = {'_new': tuple.__new__}
    template = """def __new__(_cls, %(argtxt)s):
        return _new(_cls, (%(argtxt)s))""" % locals()
    if verbose:
        print template
    exec template in ns, ns
    Inner.__new__ = staticmethod(ns['__new__'])  # NOT classmethod!

    # Inject properties to retrieve items by name.
    for i, name in enumerate(field_names):
        setattr(Inner, name, property(_itemgetter(i)))

    Inner.__dict__['_replace'].__doc__ %= locals()
    Inner.__name__ = typename
    return Inner


if __name__ == '__main__':
    # verify that instances can be pickled
    from cPickle import loads, dumps
    Point = namedtuple('Point', 'x, y', True)
    p = Point(x=10, y=20)
    assert p == loads(dumps(p, -1))

    # test and demonstrate ability to override methods
    class Point(namedtuple('Point', 'x y')):
        @property
        def hypot(self):
            return (self.x ** 2 + self.y ** 2) ** 0.5
        def __str__(self):
            return 'Point: x=%6.3f y=%6.3f hypot=%6.3f' % (self.x, self.y, self.hypot)

    for p in Point(3,4), Point(14,5), Point(9./7,6):
        print (p)

    class Point(namedtuple('Point', 'x y')):
        'Point class with optimized _make() and _replace() without error-checking'
        _make = classmethod(tuple.__new__)
        def _replace(self, _map=map, **kwds):
            return self._make(_map(kwds.get, ('x', 'y'), self))

    print Point(11, 22)._replace(x=100)

    import doctest
    TestResults = namedtuple('TestResults', 'failed attempted')
    print TestResults(*doctest.testmod())
