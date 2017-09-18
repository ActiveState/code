import operator as op


def ncr(n, r):
    r       = min(r, n-r)
    if x == 0: return 1
    num     = reduce(op.mul, xrange(n, n-1, -1))
    denom   = reduce(op.mul, xrange(1, r+1))
    return num // denom

def ncr3(n, r):
    r       = min(r, n-r)
    if x == 0: return 1
    num     = reduce(op.mul, range(n, n-1, -1))
    denom   = reduce(op.mul, range(1, r+1))
    return num // denom
