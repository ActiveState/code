"""
matcher() makes a string matcher function from any of:
    "RE pattern string"
    re.compile()
    a function, i.e. callable
    a dict / list / tuple / set / container

This uniformity is simple, useful, a Good Thing.

Usage:
    matchf = matcher( "re pattern" / re / func / dict / list / tuple / set )
    ...
    if matchf( str ):
        -- re.search( str ) / func( str ) / str in the container

A few example functions using matchers are here too:

  grep( matcher(), afile )
    -- print matching lines + header and trailer, in a file or iterable

  getfields( "kw kw2 ...".split(), afile )
    -- lines starting "kw:"  ->  [ ("kw", "kw: line") ... ]

  kwgrep, combined grep and getfields:
    kwgrep(
        "name: ^mp3  version: ^1.2.3"   -- match these
        "home-page: summary:"           -- and get these too
        )
    -> lines, nhit, nre
    e.g. [( "name", "name: mp3xx" )], 1, 2  -- 1 kw match only, not both

"""

# care: re.match( "end$" ) doesn't match "end " "end\n" "end\r"
# so rstrip lines early
# see also: pls egg-info list + search,  gmatch goopat

# 5may: matcher( ">= NJ" )  ->  lambda x: x >= "NJ"  -- str not num


import re, sys

__version__ = "2009-05-06-May"
__author_email__ = "denis-bz-py@t-online.de"
__credits__ = "BeautifulSoup"
Test = 0

_re_type = type( re.compile( "" ))
_relop_re = re.compile( r" ([<=>] =?) \s* (.*) ", re.X )

#-------------------------------------------------------------------------------
def matcher( x, negate=False ):
    """ matcher( "string" / compiled re / func / dict / list / tuple / set )
        -> a uniform match func, see above
    """
    if x in ( "", ".*", "*" ):  # always match
        f = lambda _: True
    elif isinstance( x, basestring ):
        if x[0] in "<=>":
            f = compare_func( x )  # ">= NJ"
        else:
            f = re.compile( x ) .search  # not BSoup lambda s: s == x
    elif isinstance( x, _re_type ):
        f = x.search
    elif callable( x ):  # e.g. re.compile().match
        f = x
    elif isinstance( x, (list, tuple) ):
        f = set( x ).__contains__
    elif hasattr( x, "__contains__" ):  # dict, set -- care if they change later ?!
        f = x.__contains__
    elif x in ( 0, 1, True, False, None ):
        f = lambda _: x
    # matcher( matcher) == matcher
    else:
        assert 0, "matcher: %s must be one of: str re callable dict list tuple" % x
    if negate:
        return lambda x: not f( x )  # match this - that, cf goopat
    return f

#...............................................................................
def grep( matchf, afile, header="", indent="", trailer="", out=sys.stdout ):
    """ print lines matching matchf ("re" / re / func / dict) + header and trailer
        -> nmatch
        out None: just return 1 on first match / 0
    """
    matchf = matcher( matchf )
    if isinstance( afile, basestring ):
        afile = open( afile )  # IOError: [Errno 2] No such file or directory
    nmatch = 0
    for line in afile:
        if matchf( line ):
            if out is None:
                return 1
            if header:
                print >>out, header
                header = None
            print "%s%s" % (indent, line)
            nmatch += 1
    if nmatch and out and trailer:
        print >>out, trailer.rstrip( " " )
    return nmatch


_kw_re = re.compile(      r" \s*  ([\w.-]+)  \s*  :  \s* ", re.X )
_kw_rest_re = re.compile( r" \s*  ([\w.-]+)  \s*  :  \s*  (.*)  ", re.X )
                                #  kw: rest of line

#...............................................................................
def getfields( fields, afile, lower=True ):
    """ grep lines starting with given keywords / field names ":"
        e.g. "name version".split()
       -> lines [ ("name", "name: ...") ... ]
    """
    if isinstance( fields, basestring ):
        fields = filter( None, re.split( r"[\s:,]+", fields ))
    matchf = matcher( fields )
    if isinstance( afile, basestring ):
        afile = open( afile )
    lines = []
    for line in afile:
        m = _kw_re.match( line )  # kw: ...
        if not m:
            continue
        kw = m.group( 1 )
        if lower:  kw = kw.lower()
        if matchf( kw ):  # kw in dict list tuple or set  or func( kw )
            lines.append( (kw, line.rstrip()) )
    return lines

#...............................................................................
def kwgrep( grepdict, afile, lower=True ):
    """ combined grep + getfields:
        "name: ^mp3  version: ^1.2.3"   -- match these
        "home-page: summary:"           -- and get these too
        or a dict, kw -> matcher() / "" for also-gets
    usage:
        lines, nmatch, nre = kwgrep()
        if nmatch == nre:
            ... all REs matched, here both name: and version:
            ... or 0 == 0, just getfields
    """
    if isinstance( grepdict, basestring ):
        grepdict = str_grepdict( grepdict )
    if isinstance( afile, basestring ):
        afile = open( afile )
    lines = []
    hits = {}  # nr diff keywords w RE matches
    for line in afile:
        m = _kw_rest_re.match( line )  # kw: ...
        if not m:
            continue
        kw = m.group( 1 )
        if lower:  kw = kw.lower()
        if kw not in grepdict:
            continue
        matchf = grepdict[kw]
        if not matchf:
            lines.append( (kw, line.rstrip()) )  # also-gets
            continue
        restofline = m.group( 2 ) .rstrip()
        if matchf( restofline ):
            lines.append( (kw, line.rstrip()) )
            hits[kw] = 1
    nre = sum( [bool(re) for re in grepdict.values()] )
    if Test:
        print >>sys.stderr, "test kwgrep:", lines, len(hits), nre
    return (lines, len(hits), nre)


def str_grepdict( s ):  # for kwget
    if ":" not in s:  # "a b c", "a: b: c:" -> get fields a b c, matchf True
        return dict.fromkeys( s.split(), "" )
    pairs = _kw_re.split( s.rstrip() )
        # "a: 1  b:  c:  d: 2" -> ['', 'a', ' 1', 'b', '', 'c', '', 'd', ' 2']
    grepdict = {}
    for kw, val in [pairs[j:j+2] for j in range( 1, len(pairs), 2 )]:
        grepdict[kw] = matcher( val ) if val  else ""
    if Test:
        print >>sys.stderr, "test str_grepdict:", grepdict
    return grepdict

#...............................................................................
def putlines( lines, header="", indent="", trailer="", out=sys.stdout ):
    """ kwlines = getfields( "name version".split(), afile )
        putlines( map( itemgetter(1), kwlines ), header=afile )
    """
    if not lines:
        return
    if header:
        print >>out, header
    for line in lines:
        print "%s%s" % (indent, line)
    if trailer:
        print >>out, trailer.rstrip( " " )

#...............................................................................
def compare_func( relopstr ):
    """ "< 3"  ->  the function  x -> (x < "3")  NB str "3" not num 3
    """
    # (could lambda x: (x < 3) if isnum(x)  else (x < "3")
    # but then version: > 0.1  is num compare,
    #          version: > 0.1.0  str

    relop, s = _relop_re.match( relopstr ) .groups()
    if relop == "=":  relop = "=="
    s = s.rstrip() .strip( "\"" )
    cmptext = "lambda x: x %s \"%s\"" % (relop, s)
                # e.g.   x < "3" 
    if Test:
        print >>sys.stderr, "compare_func: %s" % cmptext
    return eval( cmptext )  # try ?


#...............................................................................
if __name__ == "__main__":

#     for pat in ( "a", re.compile( "^a" ), matcher( "b" ), dict( a=1 ) ):
#         matchf = matcher( pat )
#         for s in "ab":
#             print "matcher( %s )( %r ) = %s" % (  pat, s, matchf( s ))
#         print ""
#     grep( "^def", __file__ )

    import readline

    # for afile in sys.argv[1:]:
    while 1:
        try:
            line = raw_input( "matcher: " )
        except EOFError:
            break
        if line[0] == "!":
            exec( line[1:] .strip() )
        else:
            print kwgrep( "name: ^mp3  version: ", line.split( ";" ))

# end matcher.py
