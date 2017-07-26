#! /usr/bin/env python
######################################################################
#  Written by Kevin L. Sitze on 2010-11-25
#  This code may be used pursuant to the MIT License.
######################################################################

"""This module contains four flatten() functions for generating either
a sequence or an iterator.  The goal is to "flatten" a tree (typically
comprised of lists and tuples) by slicing the elements in each
contained subtree over the subtree element itself.  For example:

    ([a, b], [c, (d, e)]) => (a, b, c, d, e)

The functions available via this module are

    flatten    ( sequence[, max_depth[, ltypes]] ) => sequence
    xflatten   ( sequence[, max_depth[, ltypes]] ) => iterator
    flatten_it ( iterable[, max_depth[, ltypes]] ) => sequence
    xflatten_it( iterable[, max_depth[, ltypes]] ) => iterator

Each function takes as its only required argument the tree to flatten.
The first two functions (flatten() and xflatten()) require their first
argument to be a valid Python sequence object.  The '_it' functions
(flatten_it() and xflatten_it()) accept any iterable object.

The return type for the flatten() and xflatten_it functions is the
same type as the input sequence, when possible, otherwise the type
will be 'list'.

Wall clock speed of these functions increase from the top of the list
down (i.e., where possible prefer the flatten() function to any other
if speed is a concern).

The "max_depth" argument is either a non-negative integer indicating
the maximum tree depth to flatten; or "None" to flatten the entire
tree.  The required "sequence" argument has a 'depth' of zero; a list
element of the sequence would be flattened if "max_depth" is greater
than or equal to one (1).  A negative depth is treated the same as a
depth of zero.

The "ltypes" argument indicates which elements are subtrees.  It may
be either a collection of sequence types or a predicate function.  If
"ltypes" is a collection a subtree is expanded if its type is in the
collection.  If "ltypes" is a predicate function a subtree is expanded
if the predicate function returns "True" for that subtree.

The implementation of flatten here runs in O(N) time where N is the
number of elements in the traversed tree.  It uses O(N+D) space
where D is the maximum depth of the traversed tree.
"""

def flatten( l, max_depth = None, ltypes = ( list, tuple ) ):
    """flatten( sequence[, max_depth[, ltypes]] ) => sequence

    Flatten every sequence in "l" whose type is contained in "ltypes"
    to "max_depth" levels down the tree.  See the module documentation
    for a complete description of this function.

    The sequence returned has the same type as the input sequence.
    """
    if max_depth is None: make_flat = lambda x: True
    else: make_flat = lambda x: max_depth > len( x )
    if callable( ltypes ): is_sequence = ltypes
    else: is_sequence = lambda x: isinstance( x, ltypes )

    r = list()
    s = list()
    s.append(( 0, l ))
    while s:
        i, l = s.pop()
        while i < len( l ):
            while is_sequence( l[i] ):
                if not l[i]: break
                elif make_flat( s ):
                    s.append(( i + 1, l ))
                    l = l[i]
                    i = 0
                else:
                    r.append( l[i] )
                    break
            else: r.append( l[i] )
            i += 1
    try: return type(l)(r)
    except TypeError: return r

def xflatten( l, max_depth = None, ltypes = ( list, tuple ) ):
    """xflatten( sequence[, max_depth[, ltypes]] ) => iterable

    Flatten every sequence in "l" whose type is contained in "ltypes"
    to "max_depth" levels down the tree.  See the module documentation
    for a complete description of this function.

    This is the iterator version of the flatten function.
    """
    if max_depth is None: make_flat = lambda x: True
    else: make_flat = lambda x: max_depth > len( x )
    if callable( ltypes ): is_sequence = ltypes
    else: is_sequence = lambda x: isinstance( x, ltypes )

    r = list()
    s = list()
    s.append(( 0, l ))
    while s:
        i, l = s.pop()
        while i < len( l ):
            while is_sequence( l[i] ):
                if not l[i]: break
                elif make_flat( s ):
                    s.append(( i + 1, l ))
                    l = l[i]
                    i = 0
                else:
                    yield l[i]
                    break
            else: yield l[i]
            i += 1

def flatten_it( l, max_depth = None, ltypes = ( list, tuple ) ):
    """flatten_it( iterator[, max_depth[, ltypes]] ) => sequence

    Flatten every sequence in "l" whose type is contained in "ltypes"
    to "max_depth" levels down the tree.  See the module documentation
    for a complete description of this function.

    The sequence returned has the same type as the input sequence.
    """
    if max_depth is None: make_flat = lambda x: True
    else: make_flat = lambda x: max_depth > len( x )
    if callable( ltypes ): is_iterable = ltypes
    else: is_iterable = lambda x: isinstance( x, ltypes )

    r = list()
    s = list()
    s.append(( iter( l ) ))
    while s:
        i = s.pop()
        try:
            while True:
                e = i.next()
                if is_iterable( e ):
                    if make_flat( s ):
                        s.append(( i ))
                        i = iter( e )
                    else:
                        r.append( e )
                else:
                    r.append( e )
        except StopIteration: pass
    try: return type(l)(r)
    except TypeError: return r

def xflatten_it( l, max_depth = None, ltypes = ( list, tuple ) ):
    """xflatten_it( iterator[, max_depth[, ltypes]] ) => iterator

    Flatten every sequence in "l" whose type is contained in "ltypes"
    to "max_depth" levels down the tree.  See the module documentation
    for a complete description of this function.

    This is the iterator version of the flatten_it function.
    """
    if max_depth is None: make_flat = lambda x: True
    else: make_flat = lambda x: max_depth > len( x )
    if callable( ltypes ): is_iterable = ltypes
    else: is_iterable = lambda x: isinstance( x, ltypes )

    r = list()
    s = list()
    s.append(( iter( l ) ))
    while s:
        i = s.pop()
        try:
            while True:
                e = i.next()
                if is_iterable( e ):
                    if make_flat( s ):
                        s.append(( i ))
                        i = iter( e )
                    else:
                        yield e
                else:
                    yield e
        except StopIteration: pass

if __name__ == '__main__':

    import sys
    import traceback
    def assertEquals( exp, got ):
        if exp is got:
            r = True
        elif type( exp ) is not type( got ):
            r = False
        elif type( exp ) in ( float, complex ):
            r = abs( exp - got ) < 1e-8
        else:
            r = ( exp == got )
        if not r:
            print >>sys.stderr, "Error: expected <%s> but got <%s>" % ( repr( exp ), repr( got ) )
            traceback.print_stack()

    def test( exp, got, depth = None ):
        assertEquals( exp, flatten( got, depth ) )
        assertEquals( exp, tuple( xflatten( got, depth ) ) )
        assertEquals( exp, flatten_it( got, depth ) )
        assertEquals( exp, tuple( xflatten_it( got, depth ) ) )

    test( (),      () )
    test( (),      (()) )
    test( (),      ((),()) )
    test( (),      ((),((),()),()) )
    test( (1,),    ((1,),((),()),()) )
    test( (1,),    ((),1,((),()),()) )
    test( (1,),    ((),(1,(),()),()) )
    test( (1,),    ((),((1,),()),()) )
    test( (1,),    ((),((),1,()),()) )
    test( (1,),    ((),((),(1,)),()) )
    test( (1,),    ((),((),(),1),()) )
    test( (1,),    ((),((),()),1,()) )
    test( (1,),    ((),((),()),(1,)) )
    test( (1,),    ((),((),()),(),1) )
    test( (1,),    ((),1,()) )
    test( (1,2,3), (1,2,3) )
    test( (1,2,3), ((1,2),3) )
    test( (1,2,3), (1,(2,3)) )
    test( (1,2,3), ((1,),(2,),3) )
    test( ((((((((((0,),1),2),3),4),5),6),7),8),9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 0 )
    test( (((((((((0,),1),2),3),4),5),6),7),8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 1 )
    test( ((((((((0,),1),2),3),4),5),6),7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 2 )
    test( (((((((0,),1),2),3),4),5),6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 3 )
    test( ((((((0,),1),2),3),4),5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 4 )
    test( (((((0,),1),2),3),4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 5 )
    test( ((((0,),1),2),3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 6 )
    test( (((0,),1),2,3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 7 )
    test( ((0,),1,2,3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 8 )
    test( (0,1,2,3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 9 )
    test( (0,1,2,3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 10 )

    test( ({1:2},3,4,set([5,6])), ({1:2},(3,4),set([5,6])) )

    l = (1,)
    # Build a tree 1 million elements deep
    for i in xrange( 1000000 ): l = ( l, 2 )
    # expected value is a 1 followed by 1 million 2's
    exp = (1,) + (2,) * 1000000
    # # Under 5 seconds on my machine...
    # got = flatten( l )
    # assert( exp == got )
    # # Also under 5 seconds...
    # got = tuple( xflatten( l ) )
    # assert( exp == got )
    # # 6 seconds
    # got = flatten_it( l )
    # assert( exp == got )
    # # 7 seconds
    # got = tuple( xflatten_it( l ) )
    # assert( exp == got )
