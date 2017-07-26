import sys
import string

"""
This module provides general purpose routines for generating
lists of strings from patterns. Thus:

    python Pattern.py 172.16.[72-74,77-82].[101-200]

produces the following sequence of 800 IPs:

    172.16.72.101
    172.16.72.102
    ...
    172.16.82.199
    172.16.82.200

Ranges can be decimal, hexidecimal and alphabetic, e.g.

    % python Pattern.py [0-10]
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    %

    % python Pattern.py foobar_[a-z]
    foobar_a
    foobar_b
    foobar_c
    ...
    foobar_x
    foobar_y
    foobar_z
    % 

    % python Pattern.py [a-z][A-Z]
    aA
    aB
    aC
    ...
    zX
    zY
    zZ
    % 

    % python Pattern.py [0x0-0xf]
    0
    1
    2
    ...
    d
    e
    f
    % 

For hexadecimal output the leading 0x is left out because it's trivial to add:

    % python Pattern.py 0x[0xa-0xf]
    0xa
    0xb
    0xc
    0xd
    0xe
    0xf
    % 

To help formatting, zero padding on the start of the range
is added to all members of the range, e.g.

    % python Pattern.py an-sm[1-8]-g[001-100]
    an-sm1-g001
    an-sm1-g002
    an-sm1-g003
    ...
    an-sm8-g098
    an-sm8-g099
    an-sm8-g100
    % 

In addition, Pattern extends IPPatterns notation by adding
the concept of a zip using juxtaposition. Thus the sequences
produced by successive arguments are computing in step and
are displayed together. Thus to produce a simple table of
the hex ascii codes for lowercase letters is simply:

    % python Pattern.py [A-Z] 0x[0x41-0x5a]
    A 0x41
    B 0x42
    C 0x43
    ...
    X 0x58
    Y 0x59
    Z 0x5a
    % 

Similarly to produce a deck of 52 cards is simply:

    % python Pattern.py [2-9,T,J,Q,K,A][C,D,H,S]
    2C
    2D
    2H
    2S
    3C
    3D
    3H
    3S
    ...
    KC
    KD
    KH
    KS
    AC
    AD
    AH
    AS
    %
"""

def aFill( str, n ):
    """leftpad str with 'a' so it is at least n chars long"""
    return ('a'*(n-len(str))) + str

def zFill( str, n ):
    """leftpad str with '0' so it is at least n chars long"""
    return str.zfill( n )

def computeIntRange( start, finish, toInt=int, fromInt=str, fill=zFill, padLen=len ):
    """Computes a range list from a start value, finish value and optional
       int-to-string, string-to-int, pad functions and pad length."""
    n = padLen( start )
    return [ fill( fromInt(i), n ) for i in range(toInt(start),toInt(finish)+1) ]

def fromHex( h ):
    """Convert a hex string into a int"""
    return int(h,16)

def   toHex( i ):
    """Convert an int into a hex string (without the leading 0x)"""
    return hex( i )[2:]

def isHexadecimalRange( start, finish ):
    """Tests for hexadecimal range"""
    return start.startswith( '0x' ) and finish.startswith( '0x' )

def isNumericRange( start, finish ):
    """Tests for decimal range"""
    return allNumeric( start ) and allNumeric( finish )

def allIn( as, members ):
    "Tests that all elements of as are in members"""
    for a in as:
        if a not in members:
            return False
    return True

def allLower( as ):
    """Tests that all strings in as are lowercase"""
    return allIn( as, string.lowercase )

def allUpper( as ):
    """Tests that all strings in as are uppercase"""
    return allIn( as, string.uppercase )

def allNumeric( as ):
    return allIn( as, string.digits )

def sameLength( as, bs ):
    """Tests that as and bs are the same length"""
    return len( as ) == len( bs )

def lettersToInt( str ):
    """turn a string of letters into a base 26 number"""
    return reduce( lambda x, y: 26*x + y, map( string.lowercase.index, str ))

def intToLetters( i, str='' ):
    """convert a number into a string of lowercase letters"""
    if i == 0:
        return str
    else:
        return intToLetters( i/26, string.lowercase[i%26] + str )

def isUpperLetterRange( start, finish ):
    """Tests start and finish are both uppercase letter ranges"""
    return allUpper( start ) and allUpper( finish )

def isLowerLetterRange( start, finish ):
    """Tests start and finish are both lowercase letter ranges"""
    return allLower( start ) and allLower( finish )

def computeRange( start, finish ):
    if isHexadecimalRange( start, finish ):
        return computeIntRange( start, finish, fromHex, toHex, zFill, lambda x: len( x )-2 )
    if isLowerLetterRange( start, finish ):
        return computeIntRange( start, finish, lettersToInt, intToLetters, aFill )
    if isUpperLetterRange( start, finish ):
        return [s.upper() for s in computeRange(start.lower(),finish.lower())]
    if isNumericRange( start, finish ):
        return computeIntRange( start, finish )
    else:
        raise SyntaxError, "invalid range syntax"

def splitAt( s, i, gap=0 ):
    """split s into two strings at index i with an optional gap"""
    return s[:i], s[i+gap:]

def find( s, target ):
    """version of find that returns len( s ) when target is not found"""
    result = s.find( target )
    if result == -1: result = len( s )
    return result

class BadOpException( Exception ):
    pass

def doOp( op, a, b ):
    if op == '++':
        return setUnion( a, b )
    elif op == '--':
        return setDifference( a, b )
    elif op == '^^':
        return setIntersection( a, b )
    else:
        raise BadOpException

"""Implementation of Sets based on lists
   We don't use the python built-in sets because
   a) they were added in a later version (2.3?)
   b) we wanted an implemetation that presevered
   the ordering of the leftmost argument to any set
   operation even if it's slower.
"""

def setEmpty():
    """return the empty set"""
    return []

def setCopy( set ):
    """(shallow) copy a set"""
    return set[:]

def member( x, set ):
    """test for set membership"""
    try:
        set.index( x )
        return True
    except ValueError:
        return False

def setToList( set ):
    """takes a set and returns a list"""
    return set

def setAdd( set, m ):
    if not member( m, set ):
        set.append( m )
    return set

def setFromList( list ):
    """takes a list and returns a set by ignoring duplicates"""
    set = setEmpty()
    for a in list:
        setAdd( set, a )
    return set

def setSubtract( set, m ):
    """in place set removal"""
    if member( m, set ): set.remove( m )

def setUnion( as, bs ):
    """returns a new set that is the union of as and bs"""
    set = setCopy( as )
    for b in bs:
        setAdd( set, b )
    return set

def setDifference( as, bs ):
    """returns a new set that is the difference of as and bs"""
    set = setEmpty()
    for a in as:
        if not member( a, bs ):
            set.append( a )
    return set

def setIntersection( as, bs ):
    """returns a new set that is the intersection of as and bs"""
    set = setEmpty()
    for a in as:
        if member( a, bs ):
            set.append( a )
    return set

def find( s, target, i=0 ):
    """Version fo find which returns len( s ) if target is not found"""
    result = s.find( target, i )
    if result == -1: result = len( s )
    return result

def multifind( s, targets, i=0 ):
    """Find the earliest index in s which matches one of targets starting at i"""
    return min( [find( s, target, i ) for target in targets] )

def fileExpr( expr, fileStr='@' ):
    """If expression contains @file@ read in contents of file and return as a list"""
    if expr.startswith( fileStr ) and expr.endswith( fileStr ):
        return [ line.rstrip() for line in file( expr[1:-1] ).readlines() ]
    else:
        return [ expr ]

def computeList( expr, openStr='[', closeStr=']', rangeStr='-', sepStr=',', fileStr='@' ):
    """Parse and compute range in expr"""
    if expr[0] == openStr:
        result = []
        while expr[0] != closeStr:
            expr = expr[1:]
            i = multifind( expr, [closeStr,rangeStr,sepStr] )
            if expr[i] == sepStr:
                item, expr = splitAt( expr, i )
                result = result + fileExpr( item )
            elif expr[i] == rangeStr:
                start, expr  = splitAt( expr, i, 1 )
                finish, expr = splitAt( expr, multifind( expr, [closeStr,sepStr] ) )
                result = result + computeRange( start, finish )
            else:
                if i > 0: result = result + fileExpr( expr[:-1] )
                break
        return result
    elif expr[0] == fileStr:
        return fileExpr( expr[1:] )
    else:
        return [expr]

def splitOnBrackets( expr, openStr='[', closeStr=']' ):
    """Splits expr in a sequence of alternating non-bracketed and bracketed expressions"""
    n = len( expr )
    components = []
    while len( expr ) > 0:
        n = len( expr )
        target = openStr
        if expr[0] == target: target = closeStr
        i = multifind( expr, [target] )
        if target == closeStr: i += 1
        components.append( expr[:i] )
        expr = expr[i:]
    return components

def product( fields, i=0, result='' ):
    """Takes a list of list of fields and produces a generator
       that permutes through every possible combination of fields in order."""
    if i == len( fields ):
        yield result
    else:
        for field in fields[i]:
            for x in product( fields, i+1, result + field ):
                yield x

def pattern( p ):
    """Splits pattern p into it's constituents and produces
       a iterator than generates all possible permutation"""
    return product( map( computeList, splitOnBrackets( p ) ) )

def setExpression( expr ):
    """Handles IP expressions of the form:
          <exp> = <exp> [-- <exp> | ++ <exp> | ^^ <exp>]*"""
    subexp, expr = splitAt( expr, multifind( expr, ['--', '++', '^^'] ) )
    accum = setFromList( pattern( subexp ) )
    while expr != '':
        op, expr = splitAt( expr, 2 )
        subexp, expr = splitAt( expr, multifind( expr, ['--', '++', '^^'] ) )
        accum = doOp( op, accum, setFromList( pattern( subexp ) ) )
    return iter( setToList( accum ) )

def expression( ps, joinStr=' ' ):
    return zipGenerators( map( setExpression,  ps ), joinStr )

def zipGenerators( ps, joinStr ):
    """Takes a list of string iterators and produces an iterator of strings joined by joinStr"""
    while True:
        yield joinStr.join( [p.next() for p in ps] )

def Pattern( ps ):
    return expression( ps )

if __name__ == '__main__':
    for result in expression( sys.argv[1:] ):
        print "%s" % result
