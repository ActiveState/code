import itertools

def alldifferent(k,n):
    '''The probability that k random selections from n possibilities
    are all different.'''
    assert(k<=n)
    nums = xrange(n,n-k,-1)
    dens = itertools.repeat(n)
    fracs = itertools.imap(lambda x,y: float(x)/y, nums,dens)
    return reduce(float.__mul__, fracs)

def collide(k,n):
    '''The probability that, in k random selections from n possibilities,
    at least two selections collide.'''
    return 1 - alldifferent(k,n)
