def invmodp(a, p):
    '''
    The multiplicitive inverse of a in the integers modulo p.
    Return b s.t.
    a * b == 1 mod p
    '''
    
    for d in xrange(1, p):
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d
    
def __invmodp__test__():
    p = 101
    for i in range(1, p):
        iinv = invmodp(i, p)
        assert (iinv * i) % p == 1
    a = 3
    p = 4
    assert (a * invmodp(a, p)) % p == 1

__invmodp__test__()
