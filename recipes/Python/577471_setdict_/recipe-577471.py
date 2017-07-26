class setdict(dict):
    '''
    Add set operations to dicts.
    '''
    def __sub__(self, other):
        res = {}
        for k in set(self) - set(other):
            res[k] = self[k]
        return setdict(**res)
    
    def __and__(self, other):
        res = {}
        for k in set(self) & set(other):
            res[k] = self[k]
        return setdict(**res)
        
    def __xor__(self, other):
        res = {}
        for k in set(self) ^ set(other):
            try:
                res[k] = self[k]
            except KeyError:
                res[k] = other[k]
        return setdict(**res)
    
    def __or__(self, other):
        res = {}
        for k in set(self) | set(other):
            try:
                res[k] = self[k]
            except KeyError:
                res[k] = other[k]
        return setdict(**res)

def call_with_filtered_args(args, _callable):
    '''
    Filter any nonkeyword elements from args, then call
    the callable with them.
    '''
    try:
        argnames = _callable.func_code.co_varnames
    except AttributeError:
        argnames = _callable.__init__.func_code.co_varnames

    args = setdict(**args) & argnames
    
    return _callable(**args)
