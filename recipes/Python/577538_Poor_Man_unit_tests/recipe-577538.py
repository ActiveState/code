#! /usr/bin/env python
######################################################################
#  Written by Kevin L. Sitze on 2010-12-03
#  This code may be used pursuant to the MIT License.
######################################################################

import sys
import traceback
from types import FloatType, ComplexType

__all__ = ( 
    'assertEquals',
    'assertNotEquals',
    'assertException',
    'assertFalse',
    'assertNone',
    'assertNotNone',
    'assertSame',
    'assertNotSame',
    'assertTrue'
)

def colon( msg ):
    if msg:
        return ": " + str( msg )
    else:
        return ""

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

def assertNotEquals( exp, got, msg = None ):
    """assertNotEquals( exp, got[, message] )

    Two objects test as "equal" if:
    
    * they are the same object as tested by the 'is' operator.
    * either object is a float or complex number and the absolute
      value of the difference between the two is less than 1e-8.
    * applying the equals operator ('==') returns True.
    """
    if exp is got:
        r = False
    elif ( type( exp ) in ( FloatType, ComplexType ) or
           type( got ) in ( FloatType, ComplexType ) ):
        r = abs( exp - got ) >= 1e-8
    else:
        r = ( exp != got )
    if not r:
        print >>sys.stderr, "Error: expected different values but both are equal to <%s>%s" % ( repr( exp ), colon( msg ) )
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

def assertFalse( b, msg = None ):
    """assertFalse( b[, message] )
    """
    if b:
        print >>sys.stderr, "Error: expected value to be False%s" % colon( msg )
        traceback.print_stack()

def assertNone( x, msg = None ):
    assertSame( None, x, msg )

def assertNotNone( x, msg = None ):
    assertNotSame( None, x, msg )

def assertSame( exp, got, msg = None ):
    if got is not exp:
        print >>sys.stderr, "Error: expected <%s> to be the same object as <%s>%s" % ( repr( exp ), repr( got ), colon( msg ) )
        traceback.print_stack()

def assertNotSame( exp, got, msg = None ):
    if got is exp:
        print >>sys.stderr, "Error: expected two distinct objects but both are the same object <%s>%s" % ( repr( exp ), colon( msg ) )
        traceback.print_stack()

def assertTrue( b, msg = None ):
    if not b:
        print >>sys.stderr, "Error: expected value to be True%s" % colon( msg )
        traceback.print_stack()

if __name__ == "__main__":
    assertNone( None )
    assertEquals( 5, 5 )
    assertException( KeyError, lambda: {}['test'] )

    assertNone( 5, 'this assertion is expected' )
    assertEquals( 5, 6, 'this assertion is expected' )
    assertException( KeyError, lambda: {}, 'this assertion is expected' )
