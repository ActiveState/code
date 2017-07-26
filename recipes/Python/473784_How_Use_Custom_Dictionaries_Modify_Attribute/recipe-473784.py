################################################################################
#
#
#
#===============================================================================
class CustomDict( dict ):

    #---------------------------------------------------------------------------
    defaultValue = 'THIS ITEM NOT AVAILABLE'

    #---------------------------------------------------------------------------
    def __getitem__( self, name ):
        try:
            return super( CustomDict, self ).__getitem__( name )
        except KeyError:
            return self.defaultValue

    #---------------------------------------------------------------------------
    def __contains__( self, name ):
        return True

    #---------------------------------------------------------------------------
    def has_key( self, name ):
        return True

################################################################################
#
#
#
#===============================================================================
class X( object ):

    #---------------------------------------------------------------------------
    def __init__( self ):
        self._dict = CustomDict( foo = 'bar' )

    #---------------------------------------------------------------------------
    @property
    def __dict__( self ):
        #print 'X.__dict__ ( get() )'
        return self._dict

    #---------------------------------------------------------------------------
    def __getattr__( self, name ):
        return self.__dict__[ name ]

    #---------------------------------------------------------------------------
    def __setattr__( self, name, value ):
        if name == '_dict':
            return super( X, self ).__setattr__( name, value )
        self._dict[ name ] = value


################################################################################
#
#
#
#===============================================================================
if __name__ == '__main__':

    x = X()
    print x.__dict__[ 'foo' ]
    print x.__dict__[ 'bar' ]
    print x.foo
    print x.bar
    print x.__dict__
    x.oops = 42
    print x.__dict__

#   Output:
#	    bar
#	    THIS ITEM NOT AVAILABLE
#	    bar
#	    THIS ITEM NOT AVAILABLE
#	    {'foo': 'bar'}
#	    {'foo': 'bar', 'oops': 42}
