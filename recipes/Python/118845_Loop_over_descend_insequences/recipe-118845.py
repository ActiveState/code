def iterable( x, strict = 0 ):
    """Return true if +x+ allows application of the +in+ operator (which excludes, for example,
    numbers and +None+), *and* the +in+ loop is actually entered into (excluding sequences of
    length zero). If +strict+ is true, an affirmative answer is furthermore subject to the
    condition that the first element retrieved within an +in+ loop be not equal to the thing
    being iterated over, which excludes strings of length one. -- Used by +walk()+ and
    +flatten()+."""
    try:
        for element in x:
            if strict:
                return element != x
            return 1
    except TypeError:
        pass
    return 0

class RecursiveContent:
    """Wrapper class for content classed as displaying recursive behavior. The original content
    is available as ~+.data+. Given content +foo+ that prints a symbolic representation like,
    say, +^blah$+, the representation +`RecursiveContent(foo)+ is +^...$+, ie, the surround
    characters are kept, while the inner part is replaced by a typographical ellipsis. This is
    somewhat compatible with the way Python symbolizes a recursive list. -- Used by +walk()+
    and +flatten()+."""
    def __init__( self, data ): self.data = data
    def __call__( self ): return self.data
    def __repr__( self ): return '%s...%s' % ( `self.data`[0], `self.data`[-1] )
    def __iter__( self ): return iter( self.data )


def walk( seq, descend = ( list, tuple ), ancestry = None ):
    """This function provides a convenient and recursion-proof way to iterate over arbitrary
    data (which is a surprisingly involved task). +seq+ may be anything accepting the
    application of the +in+ operator; +descend+ should either be a sequence of types that will
    be descended into, or a function that decides, when called with a sequence element as
    argument, whether to descend into that element or not. +ancestry+ is an argument used by
    +walk()+ for internal bookkeeping (but you can manipulate it for special effects). -- Note
    that +descend+ is only checked when trying to decide whether to descend into *elements* of
    the sequence given, not when iterating over the sequence itself. Hence, if you pass a tuple
    but specify that only lists should be descended into, the outermost sequence will still be
    analyzed into elements. For example::

        seq = ( 0, 1, 2, [ 3, 4 ], 5, ( 6, 7 ), 8 )
        for e in walk( seq, ( list, ) ):
            print e,

    will print ::

        0 1 2 3 4 5 (6, 7) 8

    onto the screen. It is possible to pass +str+ as an element in +descend+, which will split
    strings into characters, so the results of ::

        walk( ( 0, 'abc', 1 ), ( str, ) )

    and

        walk( ( 0, 'a', 'b', 'c', 1 ) )

    become indistinguishable.

    Note that data whose type appears in +descend+ but which are inherently non-iterable will
    simply be absent from the result. This is logical since iterables whose types are listed in
    +descend+ but happen to be empty likewise do not leave any trace in the result (since they
    don't offer elements to be looped over).

    As convenient spin-offs, there are two more functions related to walk: +iterable()+ and
    +flatten()+, q.v.

    IMPLEMENTATION
    ==============

    The fundamental function is as simple as this::

        def walk( seq, descend ):
            for element in seq:
                if descend( element ):
                    for subelement in walk( element, descend ):
                        yield subelement
                else:
                    yield element

    However, this definition is not safe if an iterable contains itself as an element. In order
    to prevent the function from descending infinitely, we need to keep an account of what
    elements we have already come across in the same branch; argument +ancestry+ does exactly
    that (it is o.k. to put copies of he same container side by side into another container,
    since that does not lead to recursion; we only need check for cases where a container
    contains itself). If a recursive element is detected, an instance of +RecursiveContent+ is
    returned (that the caller might want to check for). +RecursiveContent+s print out much the
    same way Python's standard representation of recursive lists does.

    Another difficulty comes with strings: when a string is being iterated over, it yields
    characters. Now, a character is simply a string of length one, so once we allow descending
    into strings on the ground of their type, we also allow to descend into characters, which
    would result in recursion. To prevent this, +walk()+ additionally checks for 'strict
    iterability', as defined by function +iterable()+ when called with +strict=1+.

    THANKSTO
    ========

    This code was inspired by the posting "Walk a directory tree using a generator" by Tom Good,
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/105873.

    """

    #   If descend is not already a function, construct one that
    #   assumes that descend has been given as a list of types:
    _descend = descend
    if not callable( _descend ):
        _descend = lambda x: type( x ) in descend
    #   Initialize ancestry:
    if ancestry is None: ancestry = []
    #   Register sequence as ancestor:
    ancestry.append( seq )
    #   Unconditionally loop over all elements in sequence:
    for element in seq:
        #   If element is in ancestry:
        if element in ancestry:
            yield RecursiveContent( element )
        #   If element is not in ancestry:
        else:
            #   If element is eligible for descend, see whether to actually descend
            #   into it, yield it wholly, or don't yield anything:
            if _descend( element ):
                #   If element is eligible and strictly iterable (i.e., not inherently
                #   recursive and not an empty sequence), descend:
                if iterable( element, strict = 1 ):
                    for subelement in walk( element, descend, ancestry ):
                        yield subelement
                #   If element is eligible and not strictly, but at least loosely iterable,
                #   yield it (because then it is something like a single-character string
                #   which should not be lost):
                elif iterable( element ):
                    yield element
            #   If element is not eligible for descend, yield it:
            else:
                yield element
    ancestry.pop()


def flatten( seq, descend = ( list, tuple ) ):
    """Return a list of all the elements that result from an exhaustive +walk()+ over a given
    +seq+uence. See +walk()+ for the interpretation of +descend+."""
    return [ element for element in walk( seq, descend ) ]
