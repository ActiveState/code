### reduceDicts.py ###

from operator import add

def reduceDicts(binOp, dicts):
    reduced = {}
    for dict in dicts:
        for k,v in dict.iteritems():
            try:
                reduced[k] = binOp(reduced[k], v)
            except KeyError:
                reduced[k] = v
    return reduced


def addDicts(*dicts):
    return reduceDicts(add, dicts)


######################################################

# test in the interpreter 

>>> from reduceDicts import reduceDicts,addDicts
>>> d1 = {"a":2, "b":3, "c":-2}
>>> d2 = {"a":-3, "c":12, "d":4, "f":1}
>>> addDicts(d1,d2)
{'a': -1, 'c': 10, 'b': 3, 'd': 4, 'f': 1}
>>> reduceDicts(max, [d1,d2])
{'a': 2, 'c': 12, 'b': 3, 'd': 4, 'f': 1}
