#! /usr/bin/env python
######################################################################
#  Written by Kevin L. Sitze on 2006-12-03
#  This code may be used pursuant to the MIT License.
######################################################################

import re

__all__ = ( 'quote', )

_bash_reserved_words = {
    'case'     : True,
    'coproc'   : True,
    'do'       : True,
    'done'     : True,
    'elif'     : True,
    'else'     : True,
    'esac'     : True,
    'fi'       : True,
    'for'      : True,
    'function' : True,
    'if'       : True,
    'in'       : True,
    'select'   : True,
    'then'     : True,
    'until'    : True,
    'while'    : True,
    'time'     : True
}

####
#  _quote_re1 escapes double-quoted special characters.
#  _quote_re2 escapes unquoted special characters.

_quote_re1 = re.compile( r"([\!\"\$\\\`])" )
_quote_re2 = re.compile( r"([\t\ \!\"\#\$\&\'\(\)\*\:\;\<\>\?\@\[\\\]\^\`\{\|\}\~])" )

def quote( *args ):
    """Combine the arguments into a single string and escape any and
    all shell special characters or (reserved) words.  The shortest
    possible string (correctly quoted suited to pass to a bash shell)
    is returned.
    """
    s = "".join( args )
    if _bash_reserved_words.has_key( s ):
        return "\\" + s
    elif s.find( '\'' ) >= 0:
        s1 = '"' + _quote_re1.sub( r"\\\1", s ) + '"'
    else:
        s1 = "'" + s + "'"
    s2 = _quote_re2.sub( r"\\\1", s )
    if len( s1 ) <= len( s2 ):
        return s1
    else:
        return s2

if __name__ == '__main__':

    import sys
    import traceback
    from types import FloatType, ComplexType

    def assertEquals( exp, got ):
        """assertEquals( exp, got )

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
            print >>sys.stderr, "Error: expected <%s> but got <%s>" % ( repr( exp ), repr( got ) )
            traceback.print_stack()

    for word in _bash_reserved_words:
        assertEquals( "\\" + word, quote( word ) )

    for char in ( '\t',
                  ' ', '!', '"', '#',
                  '$', '&', "'", '(',
                  ')', '*', ':', ';',
                  '<', '>', '?', '@',
                  '[', ']', '^', '`',
                  '{', '|', '}', '~' ):
        assertEquals( "\\" + char, quote( char ) )

    assertEquals( "'this is a simple path with spaces'",
                  quote( 'this is a simple path with spaces' ) )
    assertEquals( "don\\'t", quote( "don't" ) )
    assertEquals( '"don\'t do it"', quote( "don't do it" ) )
