""" attribute.py
Provides functions for creating simple properties.

If, inside a class definition, you write:

    attribute(foo=1, bar=2)
    
simple properties named 'foo' and 'bar' are created for this class.
Also, private instance variables '__foo' and '__bar' will be added 
to instances of this class.

USEAGE:

# assumes attribute.py is on path 
from attribute import *

class MyClass(object):
    readable(foo=1, bar=2) # or, attribute('r', foo=1, bar=2)
    writable(fro=3, boz=4) # or, attribute('w', fro=3, boz=4)
    attribute(baz=5)

This is equivalent to the following:

class MyClass(object):
    def __init__(self): 
        self.__foo = 1
        self.__bar = 2
        self.__fro = 3
        self.__boz = 4
        self.__baz = 5

    def get_foo(self): 
        return self.__foo
    def get_bar(self): 
        return self.__bar
    def set_fro(self, value): 
        self.__fro = value
    def set_boz(self, value): 
        self.__boz = value
    def get_baz(self):
        return self.__baz
    def set_baz(self, value):
        self.__baz = value
    def del_baz(self):
        del self.__baz

    foo = property(fget=get_foo, doc="foo")
    bar = property(fget=get_bar, doc="bar")
    fro = property(fset=set_fro, doc="fro")
    boz = property(fset=set_boz, doc="boz")
    baz = property(fget=get_baz, fset=set_baz, fdel=del_baz, doc="baz")
"""

__all__ = ['attribute', 'readable', 'writable']
__version__ = '3.0'
__author__ = 'Sean Ross'
__credits__ = ['Guido van Rossum', 'Garth Kidd']
__created__ = '10/21/02'

import sys

def mangle(classname, attrname):
    """mangles name according to python name-mangling 
       conventions for private variables"""
    return "_%s__%s" % (classname, attrname)

def class_space(classlevel=3):
    "returns the calling class' name and dictionary"
    frame = sys._getframe(classlevel)
    classname = frame.f_code.co_name
    classdict = frame.f_locals
    return classname, classdict

# convenience function
def readable(**kwds):
    "returns one read-only property for each (key,value) pair in kwds"
    return _attribute(permission='r', **kwds)

# convenience function
def writable(**kwds):
    "returns one write-only property for each (key,value) pair in kwds"
    return _attribute(permission='w', **kwds) 

# needed because of the way class_space is resolved in _attribute
def attribute(permission='rwd', **kwds):
    """returns one property for each (key,value) pair in kwds;
       each property provides the specified level of access(permission):
           'r': readable, 'w':writable, 'd':deletable
    """
    return _attribute(permission, **kwds)

# based on code by Guido van Rossum, comp.lang.python 2001-07-31        
def _attribute(permission='rwd', **kwds):
    """returns one property for each (key,value) pair in kwds;
       each property provides the specified level of access(permission):
           'r': readable, 'w':writable, 'd':deletable
    """
    classname, classdict = class_space()
    def _property(attrname, default):
        propname, attrname = attrname, mangle(classname, attrname)
        fget, fset, fdel, doc = None, None, None, propname
        if 'r' in permission:
            def fget(self):
                value = default
                try: value = getattr(self, attrname)
                except AttributeError: setattr(self, attrname, default)
                return value
        if 'w' in permission:
            def fset(self, value):
                setattr(self, attrname, value)
        if 'd' in permission:
            def fdel(self): 
                try: delattr(self, attrname)
                except AttributeError: pass
                # calling fget can restore this attribute, so remove property 
                delattr(self.__class__, propname)
        return property(fget=fget, fset=fset, fdel=fdel, doc=doc)
        
    for attrname, default in kwds.items():
        classdict[attrname] = _property(attrname, default)
