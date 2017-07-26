Pure object filter example:

cmpcasts = {'__lt__': lambda x, y: x < y,
            '__le__': lambda x, y: x <= y,
            '__eq__': lambda x, y: x == y,
            '__ne__': lambda x, y: x != y,
            '__gt__': lambda x, y: x > y,
            '__ge__': lambda x, y: x >= y
            }

def short_or(key, aList, anObject):
    """A helper function for parse_branch,
       since reduce(or, [value]) won't short-circuit."""
    for eachValue in aList:
        if parse_branch(key, eachValue, anObject): return True
    return False

def opval(key, value, anObject):
    """A helper function for parse_branch."""
    operation, value = value
    # value = parse_branch(key, value, anObject)
    try:
        anOp = getattr(anObject.data[key], operation)
        return apply(anOp, [value])
    except AttributeError:
        return cmpcasts[operation](anObject.data[key], value)

def parse_branch(key, value, anObject):
    """Parse a BizFilter branch according to the following grammar:
    
    {name: value} implies an atomic operation on a value of name 'name'.
    Multiple {names} implies an 'and' relationship between them.
    
    [value, value, value, ...] implies an 'or' relationship.
    
    (operation, value) implies anObject.operation(value).
    
    Any other value is taken as a primitive type.
    
    Example: ((not isInvalid) and ((delivery is None) or delivery >= 3/13/29))
           = {'isInvalid': False,
              'delivery': [None,
                          ('__gt__', aDate('3/13/1929'))
                          ]
              }
    """
    
    if type(value) == type({}):
        if len(value) == 0: return True
        return reduce(lambda x,y: x and y,
                      [parse_branch(eachKey, eachValue, anObject)
                       for eachKey, eachValue in value.items()])
    elif type(value) == type([]):
        if len(value) == 0: return False
        return short_or(key, value, anObject)
    elif type(value) == type(()):
        return opval(key, value, anObject)
    else:
        try:
            return value == anObject.data[key]
        except KeyError: raise PropertyNotFoundError(key)



#######################

ADO Database example:

cmpcasts_ADO = {'__lt__': "<", '__le__': "<=",
            '__eq__': "=", '__ne__': "<>",
            '__gt__': ">", '__ge__': ">="
            }

def short_or_ADO(key, aList):
    """A helper function for parse_branch."""
    return "(%s)" % (" or ".join([("%s" % parse_branch_ADO(key, eachValue))
                        for eachValue in aList]))

def opval_ADO(key, value):
    """A helper function for parse_branch."""
    operation, value = value
    return "[%s] %s %s" % (key, cmpcasts_ADO[operation], quoted_field(value))

def parse_branch_ADO(key, value):
    """Parse a Filter branch according to the following grammar:
    (snip)
    """
    
    if type(value) == type({}):
        if len(value) == 0: return "True"
        return "(%s)" % reduce(lambda x,y: "%s and %s" % (x, y),
                      [parse_branch_ADO(eachKey, eachValue)
                       for eachKey, eachValue in value.items()])
    elif type(value) == type([]):
        if len(value) == 0: return "False"
        return short_or_ADO(key, value)
    elif type(value) == type(()):
        return opval_ADO(key, value)
    else:
        if value is None:
            return "IsNull([%s])" % (key)
        else:
            return "[%s] = %s" % (key, quoted_field(value))
