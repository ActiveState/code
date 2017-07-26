def isallinstance(iterable, typeOrTuple):
    return all(isinstance(i, typeOrTuple) for i in iterable)




## Previous Version:
##
## def isallinstance(iterable, typeOrTuple):
##     vals = [isinstance(i, typeOrTuple) for i in iterable]
##     return len(vals) == sum(vals)
