#!/usr/bin/env python
#
# $Source$
# $Id$
#

"""
Proxy objects for any library, that allow you to add hooks before or after
methods on a specific object.

"""

__version__ = "$Revision$"
__author__ = "Martin Blais <blais@furius.ca>"

#===============================================================================
# EXTERNAL DECLARATIONS
#===============================================================================

import types
from pprint import pformat

#===============================================================================
# PUBLIC DECLARATIONS
#===============================================================================

__all__ = ['HookProxy']

#-------------------------------------------------------------------------------
#
class ProxyMethodWrapper:
    """
    Wrapper object for a method to be called.
    """

    def __init__( self, obj, func, name ):
        self.obj, self.func, self.name = obj, func, name
        assert obj is not None
        assert func is not None
        assert name is not None

    def __call__( self, *args, **kwds ):
        return self.obj._method_call(self.name, self.func, *args, **kwds)

#-------------------------------------------------------------------------------
#
class HookProxy(object):
    """
    Proxy object that delegates methods and attributes that don't start with _.
    You can derive from this and add appropriate hooks where needed.
    Override _pre/_post to do something before/afer all method calls.
    Override _pre_<name>/_post_<name> to hook before/after a specific call.
    """

    def __init__( self, objname, obj ):
        self._objname, self._obj = objname, obj

    def __getattribute__( self, name ):
        """
        Return a proxy wrapper object if this is a method call.
        """
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        else:
            att = getattr(self._obj, name)
            if type(att) is types.MethodType:
                return ProxyMethodWrapper(self, att, name)
            else:
                return att

    def __setitem__( self, key, value ):
        """
        Delegate [] syntax.
        """
        name = '__setitem__'
        att = getattr(self._obj, name)
        pmeth = ProxyMethodWrapper(self, att, name)
        pmeth(key, value)

    def _call_str( self, name, *args, **kwds ):
        """
        Returns a printable version of the call.
        This can be used for tracing.
        """
        pargs = [pformat(x) for x in args]
        for k, v in kwds.iteritems():
            pargs.append('%s=%s' % (k, pformat(v)))
        return '%s.%s(%s)' % (self._objname, name, ', '.join(pargs))

    def _method_call( self, name, func, *args, **kwds ):
        """
        This method gets called before a method is called.
        """
        # pre-call hook for all calls.
        try:
            prefunc = getattr(self, '_pre')
        except AttributeError:
            pass
        else:
            prefunc(name, *args, **kwds)

        # pre-call hook for specific method.
        try:
            prefunc = getattr(self, '_pre_%s' % name)
        except AttributeError:
            pass
        else:
            prefunc(*args, **kwds)

        # get real method to call and call it
        rval = func(*args, **kwds)

        # post-call hook for specific method.
        try:
            postfunc = getattr(self, '_post_%s' % name)
        except AttributeError:
            pass
        else:
            postfunc(*args, **kwds)

        # post-call hook for all calls.
        try:
            postfunc = getattr(self, '_post')
        except AttributeError:
            pass
        else:
            postfunc(name, *args, **kwds)

        return rval


#===============================================================================
# TEST
#===============================================================================

def test():
    import sys

    class Foo:
        def foo( self, bli ):
            print '       (running foo -> %s)' % bli
            return 42

    class BabblingFoo(HookProxy):
        "Proxy for Foo."
        def _pre( self, name, *args, **kwds ):
            print >> sys.stderr, \
                  "LOG :: %s" % self._call_str(name, *args, **kwds)

        def _post( self, name, *args, **kwds ):
            print 'after all'

        def _pre_foo( self, *args, **kwds ):
            print 'before foo...'

        def _post_foo( self, *args, **kwds ):
            print 'after foo...'

    f = BabblingFoo('f', Foo())
    print 'rval = %s' % f.foo(17)

    # try calling non-existing method
    try:
        f.nonexisting()
        raise RuntimeError
    except AttributeError:
        pass

if __name__ == '__main__':
    test()
