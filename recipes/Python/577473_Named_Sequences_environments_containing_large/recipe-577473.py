#! /usr/bin/env python
######################################################################
#  Written by Kevin L. Sitze around 2008-05-03
#  This code may be used pursuant to the MIT License.
######################################################################

"""Generate classes with named data attributes that can be sequenced.
Useful for POD classes for which many instances will exist.
Compare this feature set to NamedTuples by Raymond Hettinger:
http://code.activestate.com/recipes/500261-named-tuples/

>>> Point = NamedSequences('Point', 'x', 'y')
>>> Point                               # module.class
<class '__main__.Point'>
>>> Point.__doc__                       # documentation
'Point(x, y) => instance'
>>> Point()                             # default fields are undefined
Point(x = None, y = None)
>>> Point = NamedSequences('Point', 'x', y=0) # specify new defaults
>>> Point()                             # default fields take our values
Point(x = None, y = 0)
>>> Point(1, 2)                         # positional parameters
Point(x = 1, y = 2)
>>> p = Point(y=3, x=4)                 # keyword parameters
>>> p
Point(x = 4, y = 3)
>>> p.x                                 # member access and...
4
>>> p[0]                                # ...indexing and...
4
>>> p[1]
3
>>> p[2]                                # ...bounds checking
Traceback (most recent call last):
  [snip]
    IndexError: tuple index out of range
>>> x, y = p                            # unpack on assignment
>>> x, y
(4, 3)
>>> d = p._asdict()                     # as dictionary
>>> d
{'y': 3, 'x': 4}
>>> Point(**d)                          # from dictionary
Point(x = 4, y = 3)
>>> p._replace(x=10)                    # replace fields by name
Point(x = 10, y = 3)
"""

import keyword
import copy
import sys

__all__ = ( 'NamedSequences', 'named_sequences' )

def unique( it ):
    """unique( it ) => iterator

    Generate each value from the input iterator "it" exactly once
    ordered according to the first occurance of the value.
    """
    seen = set()
    for v in it:
        if v in seen: continue
        seen.add( v )
        yield v

def NamedSequences( className, *_names, **_kwds ):
    """NamedSequences( className[, 'name_1'[,...[,
                       name_N = defaultValue_1[, ... ]]]] )

    Construct a new class that contains only the named elements.
    This is useful in cases where you know you're going to have a ton
    of instances for a class and wish to conserve memory by avoiding
    the overhead of a per instance dictionary.

    Instances of the returned class are Python sequences.

        NamedSequences(
            __name__, 'MyClass',
            'fieldName1', ..., # argument field names
            fieldNameN = defaultValue1, ...)

    Keyword arguments are unordered dict's so if you wish to control
    field ordering you MUST specify your field names twice, once in
    the positional argument list area (to define the ordering), and
    the second time in the keyword area to specify that field's
    default value.  Field names defined only as keyword arguments are
    placed in ascending order after all field names specified as
    positional arguments.  Duplicate field names are dropped with
    priority given to the first appearance of the name.

    Keyword arguments beginning and ending with a double underscore
    are Python reserved words.  These will be inserted directly into
    the class __dict__ rather than added as regular field names.

    For example you can redefine the module that the class belongs to
    using the following pattern:

        Point = NamedSequences('Point', 'x', 'y', __module__ = __name__ )

    though this is actually redundant as the default is the module
    from which this function was called.  You can even specify your
    own documentation for the class using "__doc__ = '<my_docs>'".
    """
    # versatile arguments: (klass, 'x y'), (klass, 'x', 'y') or (klass, 'x,y')
    if len( _names ) == 1 and isinstance( _names[0], basestring ):
        _names = _names[0].replace( ',', ' ' ).split()
    _names = tuple( map( str, _names ) )

    def is_identifier( s ):
        try:
            class Tmp( object ): __slots__ = (s,)
        except TypeError: return False
        else: return not keyword.iskeyword( s )

    if not is_identifier( className ):
        raise ValueError( 'class name "%s" is not a valid identifier' % className )
    for name in _names + tuple( _kwds.keys() ):
        if not is_identifier( name ):
            raise ValueError( 'field name "%s" is not a valid identifier' % className )

    # Extract Python reserved words
    extras = dict( ( k, v ) for k, v in _kwds.iteritems() if k.startswith( '__' ) and k.endswith( '__' ) )
    _kwds = copy.deepcopy( _kwds )                 # no messing with defaults
    for k, v in extras.iteritems(): _kwds.pop( k ) # remove reserved words
    try: extras.setdefault( '__module__', sys._getframe( 1 ).f_globals.get( '__name__', '__main__' ) )
    except ( AttributeError, ValueError ): pass # no getting at the module in this env...
    _slots = tuple( unique( _names + tuple( sorted( _kwds.keys() ) ) ) ) # there can be only one...

    class SequenceClass( object ):
        """This class is the superclass of the class generated by
        "NamedSequences".  Each call to "NamedSequences" creates a
        new "SequenceClass" superclass.
        """
        __slots__ = ()
        def __init__( self, *argv, **kwds ):
            for n, v in zip( _slots, argv ): setattr( self, n, v )   # apply positional args 1st
            for n, v in kwds.iteritems(): setattr( self, n, v )     # apply keyword args 2nd
        def __cmp__( self, other ):
            if self.__class__ is other.__class__:
                return cmp( tuple( self ), tuple( other ) )
            else:
                raise TypeError, "requires a '%s' object but received a '%s'" % ( self.__class__.__name__, other.__class__.__name__ )
        def __getattr__( self, n ):
            """Defer applying class defaults until they are actually needed"""
            try: result = _kwds[n]
            except KeyError:
                if n in _slots:
                    result = None
                else: raise
            object.__setattr__( self, n, result )
            return result
        def __getitem__( self, i ): return getattr( self, _slots[i] )
        def __getnewargs__( self ): return tuple( self )
        def __setitem__( self, i, v ): setattr( self, _slots[i], v )
        def __iter__( self ): return iter( getattr( self, n ) for n in _slots )
        def __len__( self ):  return len( _slots )
        def __repr__( self ): return self.__class__.__name__ + '(' + ', '.join( n + ' = ' + repr( getattr( self, n ) ) for n in _slots ) + ')'
        def __str__( self ):  return self.__class__.__name__ + '(' + ', '.join( repr( getattr( self, n ) ) for n in _slots ) + ')'
        def _asdict( self ):  return dict( ( n, getattr( self, n ) ) for n in _slots )
        def _replace( self, **kwds ): return type( self )( *self, **kwds )

    klass = SequenceClass
    extras.setdefault( '__doc__', '%s%s => instance' % ( className, repr( _slots ).replace( "'", "" ) ) )
    extras.update( {
        '__name__': className,
        '__slots__': _slots
    } )
    return type( klass )( className, ( klass, ), extras )

def named_sequences(func):
    """Decorate a function definition to create the tuple.

    @named_sequences
    def Point(x, y): pass
    """
    return NamedSequences( func.__name__, *func.__code__.co_varnames )

if __name__ == '__main__':

    import traceback
    def assertEquals( exp, got ):
        """assertEquals(exp, got)

        Two objects test as "equal" if:
        
        * they are the same object as tested by the 'is' operator.
        * either object is a float or complex number and the absolute
          value of the difference between the two is less than 1e-8.
        * applying the equals operator ('==') returns True.
        """
        from types import FloatType, ComplexType
        if exp is got:
            r = True
        elif ( type( exp ) in ( FloatType, ComplexType ) or
               type( got ) in ( FloatType, ComplexType ) ):
            r = abs( exp - got ) < 1e-8
        else:
            r = ( exp == got )
        if not r:
            print >>sys.stderr, "Error: expected <%s> but got <%s>" % ( repr( exp ), repr( got ) )
            traceback.print_stack()

    def assertException( exceptionType, f ):
        """Assert that an exception of type \var{exceptionType}
        is thrown when the function \var{f} is evaluated.
        """
        try: f()
        except exceptionType: assert True
        else:
            print >>sys.stderr, "Error: expected <%s> to be thrown by function" % exceptionType.__name__
            traceback.print_stack()

    def assertFalse( b ):
        """assertFalse(b)
        """
        if b:
            print >>sys.stderr, "Error: expected value to be False"
            traceback.print_stack()

    def assertTrue( b ):
        if not b:
            print >>sys.stderr, "Error: expected value to be True"
            traceback.print_stack()

    ####
    #  Test NamedSequences
    ####

    Point = NamedSequences( 'Point', 'x', 'y' )
    assertEquals( "<class '__main__.Point'>", repr( Point ) )
    assertEquals( 'Point(x, y) => instance', Point.__doc__ )
    p = Point( 0, 1 )
    q = Point( y = 0, x = 1 )
    assertEquals( 0, p[0] )
    assertEquals( 0, p.x )
    assertEquals( 1, p[1] )
    assertEquals( 1, p.y )
    assertEquals( 1, q[0] )
    assertEquals( 1, q.x )
    assertEquals( 0, q[1] )
    assertEquals( 0, q.y )
    assertException( IndexError, lambda: p[2] )
    x, y = p
    assertEquals( p[0], x )
    assertEquals( p[1], y )
    x, y = q
    assertEquals( q[0], x )
    assertEquals( q[1], y )
    d = p._asdict()
    r = Point( **d )
    assertEquals( p, r )
    s = r._replace( x = 5 )
    assertEquals( 5, s.x )
    assertEquals( r.y, s.y )
    s = s._replace( y = 6 )
    assertEquals( 5, s.x )
    assertEquals( 6, s.y )

    assertEquals( 'Point', Point.__name__ )
    assertEquals( 'Point', p.__class__.__name__ )

    p = Point()
    q = Point()

    assertEquals( q, p )
    assertEquals( 0, cmp( p, q ) )

    p.x = 1
    q.x = 2
    assertTrue( p < q )
    assertTrue( q > p )
    assertTrue( cmp( p, q ) < 0 )
    assertTrue( cmp( q, p ) > 0 )
    p.x = 1
    q.x = 1
    assertEquals( 0, cmp( p, q ) )
    assertEquals( 0, cmp( q, p ) )
    p.y = 1
    q.y = 2
    assertTrue( cmp( p, q ) < 0 )
    assertTrue( cmp( q, p ) > 0 )

    assertEquals( 'Point(1, 1)', str( p ) )
    assertEquals( 'Point(x = 1, y = 1)', repr( p ) )
    assertEquals( p, Point( x = 1, y = 1 ) )

    p.x = '1'
    assertEquals( "Point('1', 1)", str( p ) )
    assertEquals( "Point(x = '1', y = 1)", repr( p ) )

    Point = NamedSequences( 'Point', x = 1, y = 2 )
    p = Point()
    assertEquals( 1, p.x )
    assertEquals( 2, p.y )

    Point = NamedSequences( 'Point', 'x y' )
    p = Point()
    p.x = 0
    p.y = 1

    Point = NamedSequences( 'Point', 'x,y' )
    p = Point()
    p.x = 0
    p.y = 1

    assertException( KeyError, lambda: p.z )
    assertException( AttributeError, lambda: setattr( p, 'z', 1 ) )

    Point = NamedSequences( 'Point', x = 0, y = 0, __module__ = '__name__' )
    assertEquals( "<class '__name__.Point'>", repr( Point ) )

    assertException( ValueError, lambda: NamedSequences( 'for' ) )
    assertException( ValueError, lambda: NamedSequences( 'in' ) )
    assertException( ValueError, lambda: NamedSequences( '123' ) )
    assertException( ValueError, lambda: NamedSequences( 'test', 'for' ) )
    assertException( ValueError, lambda: NamedSequences( 'test', 'in' ) )
    assertException( ValueError, lambda: NamedSequences( 'test', '123' ) )

    @named_sequences
    def Point(x, y, z): pass

    p = Point()
    p.x = 0
    p.y = 1
    p.z = 2
