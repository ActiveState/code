#####################################
class MDarray( list ):  # version 12.5.11
    """Allow multi-dimensional tuples to be passed as indexes to a list.
    All other operations must use real indexes, which can be calculated
    using index_from_tuple().
    The constructor requires a tuple of positive integers to define the
    dimensions of the array (and hence the size of the underlying list).
    The size of the list should not be changed, to keep the multi-dimensional
    nature intact.
    """
    def __init__( self, dims, init=None ):
        if isinstance( dims, tuple ):
            self.dims = dims
        else:
            self.dims = (dims, dims)
        self.size = 1
        for ix in self.dims:
            if ix < 1:
                raise ValueError('each dimension must be a positive integer')
            self.size *= ix
        list.__init__( self, [ init ] * self.size )
    def index_from_tuple( self, dims ):
        rix = dims[ 0 ]
        for iy in range( len( self.dims ) - 1 ):
            rix = rix * self.dims[ iy ] + dims[ iy + 1 ]
        return rix
    def __getitem__( self, ix ):
        if isinstance( ix, tuple ):
            rix = self.index_from_tuple( ix )
        else:
            rix = ix
        return list.__getitem__( self, rix )
    def __setitem__( self, ix, val ):
        if isinstance( ix, tuple ):
            rix = self.index_from_tuple( ix )
        else:
            rix = ix
        list.__setitem__( self, rix, val )
    def __repr__( self ):
        return ( list.__repr__( self )
                 + ' dims: ' + self.dims.__repr__()
                 + ' size: ' + self.size.__repr__()
                 )
#####################################
