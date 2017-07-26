def recursiveupdate(dst, src):
    """Recursively update dst from src.

    Recursion depth is bounded by the heap rather than the python 
    interpretor recursion limit.

    >>> dst = dict(a=1,b=2,c=dict(ca=31, cc=33, cd=dict(cca=1)), d=4, f=6)
    >>> src = dict(b='u2',c=dict(cb='u32', cd=dict(cda=dict(cdaa='u3411', cdab='u3412'))), e='u5')
    >>> r = recursiveupdate(dst, src)
    >>> assert r is dst
    >>> assert r['a'] == 1 and r['d'] == 4 and r['f'] == 6
    >>> assert r['b'] == 'u2' and r['e'] == 'u5'
    >>> assert dst['c'] is r['c']
    >>> assert dst['c']['cd'] is r['c']['cd']
    >>> assert r['c']['cd']['cda']['cdaa'] == 'u3411'
    >>> assert r['c']['cd']['cda']['cdab'] == 'u3412'
    >>> from pprint import pprint; pprint(r)
    {'a': 1,
     'b': 'u2',
     'c': {'ca': 31,
           'cb': 'u32',
           'cc': 33,
           'cd': {'cca': 1, 'cda': {'cdab': 'u3412', 'cdaa': 'u3411'}}},
     'd': 4,
     'e': 'u5',
     'f': 6}
    """
    irecursiveupdate(dst, src.iteritems())
    return dst

def irecursiveupdate(a, biter):
    """Recursively update dict `a` from `biter`

    `biter` is assumed to be an iterable of the form::
        [(k0, v0), (k1, v1), ..., (kN, vN)]

        ie, the result of src.iteritems()
    `a` is assumed to be a dict or dict like instance.

    In the following `dst` is the intial value of `a` and `src` is
    the initial value of `biter`.

    For every key in src: 
        If that key is also in dst and
        both dst[k] and src[k] are dicts then:
            recursiveupdate(dst[k], (src[k]))
        otherwise:
            dst[k] = src[k]

    """
    try:
        stack = []
        while biter:
            for (bk,bv) in biter:
                if (bk in a 
                    and isinstance(bv, dict)
                    and isinstance(a[bk], dict)):
                    stack.append((biter, a)) # current -> parent
                    break
                else:
                    a[bk] = bv
            else:
                while not biter:
                    biter, a = stack.pop() # current <- parent 
                continue
            biter, a = bv.iteritems(), a[bk]
    except IndexError:
        pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
 
