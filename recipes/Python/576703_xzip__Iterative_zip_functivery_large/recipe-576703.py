def xzip( *args ):
    return ( tuple( [ a[i] for a in args ] ) \
             for i in xrange( min( [ len(a) for a in args ] ) ) )
