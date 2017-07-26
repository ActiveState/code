def multi_cmp(keys, getter):                                                    
    """                                                                         
    keys - a list of keys which the getter will used compare with
    getter - a getter, usually itemgetter or attrgetter from operator
                
    This function builds a compound compare over multiple keys using the        
    supplied getter.           
    """             
    def _cmp_with_keys(x,y):
        for key in keys: 
            retVal = cmp(getter(key)(x), getter(key)(y))                        
            if retVal:                                                          
                return retVal
        return 0
    return _cmp_with_keys                                                       
    
