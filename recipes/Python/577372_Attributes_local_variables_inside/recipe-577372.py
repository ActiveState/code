from sys import _getframe
from itertools import ifilter

class Attributes(object):
    """
    The 'with' statement temporarily exposes all attributes as global variables.
    Any new variables or changes to any exposed attribute are stored in the
    object instance on exit of the 'with' statement.

    Example:
    >>> obj = Attributes()
    >>> obj.x = 1
    >>> with obj:
    ...     y = x + 1
    ...     del x
    ...     
    >>> obj
    Attributes(y = 2)
    >>> 
    """
    def __init__(self, ** attr):
        self.__dict__.update(attr)
        self._entries = 0
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ", ".join([
            "%s = %r" % v for v in ifilter(lambda (name, _): name[0] != '_',
                                           self.__dict__.iteritems())]))
    def __enter__(self):
        """Show all attributes temporarily as global variables."""
        self._entries += 1
        if self._entries == 1:
            callers = []
            depth = 0
            try:
                while 1:
                    callers.append(_getframe(depth + 1).f_locals)
                    depth += 1
                    if _getframe(depth).f_code.co_name == '<module>': raise
            except:
                pass
            callers.append(_getframe(depth).f_globals)
            callers.reverse()
            self._callers = callers
            self._backups = [s.copy() for s in self._callers]
            self._callers[0].update(self.__dict__)
    def __exit__(self, exc_type, exc_value, traceback):
        """Hide all exposed attributes and any new variables"""
        if self._entries == 1:
            callers = {}
            for s in self._callers: callers.update(zip(s.keys(), [s] * len(s)))
            currentNames = set(callers.keys())
            savedNames = set()
            for s in self._backups: savedNames.update(s.keys())
            exposedNames = set(self.__dict__.keys())
            for n in exposedNames - currentNames:
                delattr(self, n)
            for n in currentNames - savedNames:
                s = callers[n]
                setattr(self, n, s[n])
                del s[n]
            for s, b in zip(self._callers, self._backups):
                s.update(b)
            del self._callers, self._backups
        self._entries -= 1

class Scope(Attributes):
    """
    Inheritable attributes.

    Examples:
    >>> s0 = Scope(x=1)                 # s0.x=1
    >>> s1, s2 = s0(y=10), s0(y=100)    # s1.x=s2.x=s0.x; s1.y=10; s2.y=100
    >>> with s1:
    ...     z = x + y + s2.y            # s1.z = s1.x + s1.y + s2.y = 111
    ...
    >>> s3 = s1(s2)                     # s3.x=s2.x; s3.y=s2.y; s3.z=s1.z
    >>> with s3:
    ...     print x, y, z
    ... 
    1 100 111
    """
    def __init__(self, * scopes, ** attributes):
        """Inherit scopes and add attributes"""
        Attributes.__init__(self)
        self._scopes = ()
        self.attach(* scopes, ** attributes)
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ", ".join(
            [repr(s) if not s is self else "<recursion>" for s in self._scopes]
            + ["%s = %r" % v for v in ifilter(lambda (name, _): name[0] != '_',
                                              self.__dict__.iteritems())]))
    def attach(self, * scopes, ** attributes):
        """Inherit more scopes and add more attributes"""
        self._scopes = scopes + self._scopes
        self.__dict__.update(attributes)
    def __call__(self, * scopes, ** attributes):
        """Create a child scope with more scopes and attributes"""
        return self.__class__(* (scopes + (self,)), ** attributes)
    def __enter__(self):
        for s in reversed(self._scopes): s.__enter__()
        Attributes.__enter__(self)
    def __exit__(self, exc_type, exc_value, traceback):
        Attributes.__exit__(self, exc_type, exc_value, traceback)
        for s in self._scopes:
            s.__exit__(exc_type, exc_value, traceback)

from itertools import ifilter
from spiro.spiroclient import SpiroClient
from spiro.spiroserver import SpiroServer
from urlparse import urlparse
from threading import Thread

class Workspaces(SpiroServer, Thread):
    """
    Publishes named workspaces with some shared attributes.

    Example (here publishing on another port than default 9091):
    
    >>> w = Workspaces('//:9092', readme = "Hello World!")
    Service spiro://:9092/<workspace> started.
    """
    host = ""   # Serves all interfaces
    port = 9091 # Default spiroserver port 9091
    # Verbosity
    Trace = 4
    Warnings = 3
    Errors = 2
    def __init__(self, host=host, verbosity = Warnings, ** shared):
        self._host = host
        u = urlparse(host, scheme='spiro')
        SpiroServer.__init__(self, host = u.hostname or "",
                             port = u.port or self.port,
                             logVerbosity = verbosity)
        Thread.__init__(self)
        self.modules = shared
        self.start()
        print "Service spiro://%s:%d/<workspace> started." % (
            self.host, self.port)
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ", ".join(
            [repr(self._host)] +
            ["%s = %r" % a for a in self.modules.iteritems()]))

class Workspace(Attributes):
    """
    Uses a named workspace on a server.
    
    >>> ### Workspaces should be available on a device that is always on. ###
    >>> w = Workspaces(readme = "Data is safe here!")
    Service spiro://:9091/<workspace> started.
    >>> a = Workspace('a', x = 1)
    >>> with a:
    ...     print readme
    ...     y = x + 1
    ...     del x
    ... 
    Data is safe here!
    >>> a
    Workspace('a', readme = 'Data is safe here!', y = 2)
    >>> del a
    >>> Workspace('a')
    Workspace('a', readme = 'Data is safe here!', y = 2)
    """
    host = "127.0.0.1" # Connect to localhost in same device.
    # Verbosity
    Trace = 4
    Warnings = 3
    Errors = 2
    _localattributes = ['_name', '_connection', '_callers', '_backups',
                        '_entries']
    def __init__(self, name, verbosity=Warnings, ** attributes):
        self._name = name
        u = urlparse(name, scheme='spiro')
        # TODO: "https://user:password@hostname:port/path" scheme.
        if u.scheme == 'spiro':
            c = SpiroClient(u.path, host = u.hostname or 'localhost',
                            port = u.port or Workspaces.port,
                            verbosity=verbosity)
        else: raise "Only a spiro connection scheme is supported."
        self._connection = c
        for attr, val in attributes.iteritems(): setattr(c, attr, val)
        attributes = dict([(attr, getattr(c, attr)) for attr in c.dir()])
        Attributes.__init__(self, ** attributes)
    def __repr__(self):
        # TODO: Remove this connection usage when server-push is implemented.
        c = self._connection
        return "%s(%s)" % (self.__class__.__name__, ", ".join(
            [repr(self._name)] +
            ["%s = %r" % v for v in [(a, getattr(self, a)) for a in ifilter(
                lambda a: a[0] != '_', c.dir())]]))
    def __getattr__(self, attr):
        val = self.__dict__[attr] = getattr(self._connection, attr)
        return val
    def __delattr__(self, attr):
        del self.__dict__[attr]
        if not attr in self._localattributes:
            self._connection.do("del %s" % attr)
    def __setattr__(self, attr, val):
        if attr in self._localattributes:
            self.__dict__[attr] = val
        else:
            setattr(self._connection, attr, val)
            self.__dict__[attr] = getattr(self._connection, attr)
    def __enter__(self):
        # TODO: Remove this method when server-push is implemented.
        c = self._connection
        self.__dict__.update(dict([(attr, getattr(c, attr)) for attr in c.dir()]))
        Attributes.__enter__(self)
