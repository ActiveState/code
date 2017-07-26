def StringVersion( seq ):
    return '.'.join( ['%s'] * len( seq )) % tuple( seq )

def TupleVersion( str ):
    return map( int, str.split( '.' ))
