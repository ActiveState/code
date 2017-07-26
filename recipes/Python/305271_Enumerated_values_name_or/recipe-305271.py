class EnumType( object ):
    """
    Enumerated-values class.
    
    Allows reference to enumerated values by name
    or by index (i.e., bidirectional mapping).
    """
    def __init__( self, *names ):
        # Remember names list for reference by index
        self._names = list(names)
        # Attributes for direct reference
        for _i, _s in enumerate( self._names ):
            setattr( self, _s, _i )
    
    def __contains__( self, item ):
        try:
            trans = self[item]
            return True
        except:
            return False
    
    def __iter__( self ):
        return enumerate( self._names )
    
    def __getitem__( self, key ):
        if type(key) == type(0):
            return self._names[key]
        else:
            return self._nameToEnum( key )
    
    def __len__( self ):
        return len(self._names)
    
    def items( self ):
        return [ (idx, self._names[idx])
                for idx in range(0, len(self._names) ) ]
    
    
    def names( self ):
        return self._names[:]
    
    
    def _nameToEnum( self, name ):
        try:
            return getattr( self, name )
        except ValueError, exc:
            args = list(exc.args)
            args.append( "Unknown enum value name '%s'" % name )
            args = tuple(args)
            exc.args = args
            raise
