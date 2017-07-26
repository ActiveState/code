#! /usr/bin/env python
######################################################################
#  Written by Kevin L. Sitze on 2008-05-03
#  This code may be used pursuant to the MIT License.
######################################################################

"""
Property
========
The Property class provides basic functionality that allows class
level control over how a particular attribute is managed.  In its
simplest form a Property attribute works exactly like a regular
attribute on an instance while providing documentation details
about the attribute accessible via the declaring class.

This class modifies how properties are created on a class.  The Python
documentation contains the following example:

class C(object):
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x
    def setx(self, value):
        self._x = value
    def delx(self):
        del self._x
    x = property(getx, setx, delx, 'the "x" property.')

The equivalent using Property is as follows:

class C(object):
  x = Property('x', None)

>>> x = C()
>>> repr(x.x)
'None'
>>> C.x.__doc__
'the "x" property'

Need a read-only property?  Here is the Python example:

class Parrot(object):
    def __init__(self):
        self._voltage = 100000

    @property
    def voltage(self):
        'Get the current voltage.'
        return self._voltage

And here is the equivalent:

class Parrot(object):
    voltage = Property('voltage', 100000, Property.Mode.READ_ONLY, 'Get the current voltage')

If your class needs to write to a property that is intended to be
public read-only you can use the set_property() function.
"""

__all__ = ( 'Enum', 'Property' )

def Enum(*names):
    """See immutable symbolic enumeration types by Zoran Isailovski
    (see http://code.activestate.com/recipes/413486-first-class-enums-in-python/)

    - Enums are immutable; attributes cannot be added, deleted or changed.
    - Enums are iterable.
    - Enum value access is symbolic and qualified, ex. Days.Monday (like in C#).
    - Enum values are true constants.
    - Enum values are comparable.
    - Enum values are invertible (useful for 2-valued enums, like Enum('no', 'yes').
    - Enum values are usable as truth values (in a C tradition, but this is debatable).
    - Enum values are reasonably introspective (by publishing their enum type and numeric value)

    Changed slightly to add '__doc__' tags to the generated
    enumeration types.  So to the above author's comments we add:

    - Enums and Enum values are documented.
    - enumeration values are type-checked during comparisons.
    """
    assert names, "Empty enums are not supported" # <- Don't like empty enums? Uncomment!

    class EnumClass(object):
        __slots__ = names
        def __contains__(self, v): return v in constants
        def __getitem__(self, i):  return constants[i]
        def __iter__(self):        return iter(constants)
        def __len__(self):         return len(constants)
        def __repr__(self):        return 'Enum' + str(names)
        def __str__(self):         return 'enum ' + str(constants)

    class EnumValue(object):
        __slots__ = ('__value')
        def __init__(self, value): self.__value = value
        value = property(lambda self: self.__value)
        type = property(lambda self: EnumType)
        def __hash__(self):        return hash(self.__value)
        def __cmp__(self, other):
            try:
                if self.type is other.type:
                    return cmp(self.__value, other.__value)
                else:
                    raise TypeError, "requires a '%s' object but received a '%s'" % ( self.type.__class__.__name__, other.type.__class__.__name__ )
            except AttributeError:
                raise TypeError, "requires a '%s' object but received a '%s'" % ( self.type.__class__.__name__, other.__class__.__name__ )
        def __invert__(self):      return constants[maximum - self.__value]
        def __nonzero__(self):     return bool(self.__value)
        def __repr__(self):        return str(names[self.__value])
        
    maximum = len(names) - 1
    constants = [None] * len(names)
    for i, each in enumerate(names):
        val = type(EnumValue)(
            'EnumValue', (EnumValue,), { '__doc__': 'Enumeration value "%s"' % each }
        )(i)
        setattr(EnumClass, each, val)
        constants[i] = val
    constants = tuple(constants)
    EnumType = type(EnumClass)(
        'EnumClass', (EnumClass,), { '__doc__': 'Enumeration of %s' % repr(constants) }
    )()
    return EnumType

class Property(object):
    """Construct a data descriptor suitable for associating
    documentation with an attribute value.  Attribute values are
    instance specific and are stored within the instance dictionary
    (so property values go away when the instance is garbage
    collected).  Properties have a class-wide default value used if
    the property has not been specified on an instance.

    The class has the ability to indicate the access mode of the
    resulting attribute.  The possible access modes may be specified
    using exactly one of the following enumeration values:

    Mode.READ_ONLY
    ==================
    The attribute may only be read.  The instance property effectively
    becomes a class constant (as the attribute may not be written).  A
    READ_ONLY attribute must have the default value specified when the
    Property is constructed.

    Unlike an Enum class, the resulting Property is still accessable
    through the declaring class (to provide access to the attribute
    documentation).  This has the side effect that the constant value
    is only accessable through instances of the declaring class.

    Mode.READ_WRITE
    ===================
    The READ_WRITE mode is the default mode on Property instances and
    is used to provide attributes with all the normal behaviors of
    typical class attributes with supporting documentation and
    optional default values.

    Mode.WRITE_ONCE
    ===================
    The WRITE_ONCE mode builds a data descriptor that allows every
    instance of the declaring class to set the resulting attribute one
    time.  A default value may be specified that will be returned if
    the attribute is accessed prior to the write; but the default does
    not prevent the one-time write from occuring.

    Additionally you may supply a documentation string so your class
    properties may expose usage information.
    """

    ####
    #  Special value used to mark an undefined default value.
    ####

    __NONE = object()

    Mode = Enum('READ_ONLY', 'READ_WRITE', 'WRITE_ONCE')

    def __init__(self, name, default = __NONE, mode = Mode.READ_WRITE, doc = None):
        """Construct a new Property data descriptor.

        \var{name} the name of the attribute being created.
        \var{default} the (optional) default value to use when
        retrieving the attribute if it hasn't already been set.
        \var{mode} the mode of the constructed Property.
        \var{doc} the documentation string to use.  This string is
        accessed through the declaring class.
        """
        self.__name = name
        self.__key = '__property__' + name
        if mode.__class__ not in (i.__class__ for i in self.Mode):
            raise TypeError, "the mode parameter requires a member of the 'Property.Mode' enumeration but received a '%s'" % mode.__class__.__name__
        self.__mode = mode
        if default is not self.__NONE:
            self.__default = default
        elif mode is self.Mode.READ_ONLY:
            raise ValueError, 'read only attributes require a default value'
        if doc is None:
            self.__doc__ = 'the "%s" property' % name
        else:
            self.__doc__ = doc

    def __get__(self, obj, objType = None):
        """Get the attribute value.
        """
        try: return obj.__dict__[self.__key]
        except AttributeError: return self
        except KeyError: pass

        try: return objType.__dict__[self.__key]
        except KeyError: pass

        try: return self.__default
        except AttributeError:
            raise AttributeError, "'%s' object has no attribute '%s'" % ( obj.__class__.__name__, self.__name )

    def __set__(self, obj, value):
        """Set the attribute value.
        """
        if self.__mode is self.Mode.READ_ONLY:
            raise AttributeError, "can't set attribute \"%s\"" % self.__name
        elif self.__mode is self.Mode.WRITE_ONCE:
            if self.__key in obj.__dict__:
                raise AttributeError, "can't set attribute \"%s\"" % self.__name
        obj.__dict__[self.__key] = value

    def __delete__(self, obj):
        """Delete the attribute value.
        """
        if self.__mode is not self.Mode.READ_WRITE:
            raise AttributeError, "can't delete attribute \"%s\"" % self.__name
        del(obj.__dict__[self.__key])

def set_property(obj, name, value):
    """Set or reset the property 'name' to 'value' on 'obj'.

    This function may be used to modify the value of a WRITE_ONCE or
    READ_ONLY property.  Therefore use of this function should be
    limited to the implementation class.
    """
    obj.__dict__['__property__' + name] = value

if __name__ == '__main__':

    from types import FloatType, ComplexType

    def assertEquals( exp, got, msg = None ):
        """assertEquals( exp, got[, message] )

        Two objects test as "equal" if:
        
        * they are the same object as tested by the 'is' operator.
        * either object is a float or complex number and the absolute
          value of the difference between the two is less than 1e-8.
        * applying the equals operator ('==') returns True.
        """
        if exp is got:
            r = True
        elif ( type( exp ) in ( FloatType, ComplexType ) or
               type( got ) in ( FloatType, ComplexType ) ):
            r = abs( exp - got ) < 1e-8
        else:
            r = ( exp == got )
        if not r:
            print >>sys.stderr, "Error: expected <%s> but got <%s>%s" % ( repr( exp ), repr( got ), colon( msg ) )
            traceback.print_stack()

    def assertException( exceptionType, f, msg = None ):
        """Assert that an exception of type \var{exceptionType}
        is thrown when the function \var{f} is evaluated.
        """
        try:
            f()
        except exceptionType:
            assert True
        else:
            print >>sys.stderr, "Error: expected <%s> to be thrown by function%s" % ( exceptionType.__name__, colon( msg ) )
            traceback.print_stack()

    def assertNone( x, msg = None ):
        assertSame( None, x, msg )

    def assertSame( exp, got, msg = None ):
        if got is not exp:
            print >>sys.stderr, "Error: expected <%s> to be the same object as <%s>%s" % ( repr( exp ), repr( got ), colon( msg ) )
            traceback.print_stack()

    def assertTrue( b, msg = None ):
        if not b:
            print >>sys.stderr, "Error: expected value to be True%s" % colon( msg )
            traceback.print_stack()

    ####
    #  Test Property
    ####

    class Test( object ):
        ro_value = Property( 'ro_value', 'test', mode = Property.Mode.READ_ONLY )

        assertException( ValueError, lambda: Property( 'ro_undef', mode = Property.Mode.READ_ONLY ),
                         'read-only attributes should require default' )

        rw_undef = Property( 'rw_undef' )
        rw_default = Property( 'rw_default', None )
        rw_doc = Property( 'rw_default', doc = 'alternate documentation' )

        assertException( TypeError, lambda: Property( 'bad_mode', mode = None ),
                         'bad Property mode should raise an exception' )

        wo_undef = Property( 'wo_undef', mode = Property.Mode.WRITE_ONCE )
        wo_default = Property( 'wo_default', 'test', mode = Property.Mode.WRITE_ONCE )

    a = Test()
    b = Test()

    ####
    #  Mode.READ_ONLY

    assertEquals( 'test', a.ro_value )
    assertEquals( 'test', b.ro_value )
    assertException( AttributeError, lambda: setattr( a, 'ro_value', 5 ), 'unexpected write to a read-only attribute' )
    # assertException( AttributeError, lambda: del( b.ro_value ), 'unexpected del() on a read-only attribute' )

    set_property( a, 'ro_value', 'tset' )
    assertEquals( 'tset', a.ro_value )
    assertEquals( 'test', b.ro_value )

    ####
    #  Mode.READ_WRITE

    assertException( AttributeError, lambda: getattr( a, 'rw_undef' ), 'unexpected read of an undefined attribute' )
    assertNone( a.rw_default )

    a.rw_undef = 5
    assertEquals( 5, a.rw_undef )
    assertTrue( '__property__rw_undef' in a.__dict__ )
    assertEquals( 5, a.__dict__['__property__rw_undef'] )
    assertEquals( 'the "rw_undef" property', Test.rw_undef.__doc__ )
    assertSame( int, type( a.rw_undef ) )
    assertSame( Property, type( Test.rw_undef ) )

    assertEquals( 'alternate documentation', Test.rw_doc.__doc__ )

    ####
    #  Mode.READ_WRITE: changes to 'a' should not affect 'b'

    assertException( AttributeError, lambda: getattr( b, 'rw_undef' ), 'invalid state change via a different instance' )
    assertNone( b.rw_default )

    ####
    #  Mode.WRITE_ONCE

    assertException( AttributeError, lambda: getattr( a, 'wo_undef' ), 'unexpected read of an undefined attribute' )
    assertException( AttributeError, lambda: delattr( a, 'wo_undef' ), 'unexpected del() on a write-once attribute' )
    a.wo_undef = 'write_once'
    assertEquals( 'write_once', a.wo_undef )
    assertException( AttributeError, lambda: setattr( a, 'wo_undef', 'write_twice' ), 'unexpected secondary write on a write-once attribute' )
    assertEquals( 'write_once', a.wo_undef )
    assertException( AttributeError, lambda: delattr( a, 'wo_value' ), 'unexpected del() on a write-once attribute' )
    assertEquals( 'test', a.wo_default )
    a.wo_default = 'write_once'
    assertEquals( 'write_once', a.wo_default )
    assertEquals( 'test', b.wo_default )
