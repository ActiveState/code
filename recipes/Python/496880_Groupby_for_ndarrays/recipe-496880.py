from numpy import array, vectorize, unique1d, ones
from operator import itemgetter
from itertools import imap, groupby, izip

# functional composition
def compose(*args):
    def composed(arg):
        for f in reversed(args):
            arg = f(arg)
        return arg
    return composed

def agroupby(*args, **kwds):
    """A groupby function which accepts and returns arrays.
    All passed arrays are expected to be one dimensional
    and of the same shape. All of the arrays are grouped by
    `key(arg[0])` and then returned.  The returned arrays will
    be two dimensional with each row corresponding to a group.
    The size of the first dimension is equal to the number of
    groups, and the size of the second dimension is equal the
    the size of the largest groups.  All smaller groups are
    padded with the value of the keyword argument `fill_value`."""
    keyfunc = kwds.get('key', lambda a: a)
    fill_val = kwds.get('fill_value', 0.0)
    args = [a.copy() for a in args]
    argsort = sorted(enumerate(args[0]), key=compose(keyfunc,itemgetter(1)))
    indexsort = [index for index, item in argsort]
    args = [a.take(indexsort) for a in args]
    # calculate groups
    g_mask = keyfunc(args[0])
    g_set = unique1d(g_mask)
    g_max = max([g_mask[g_mask==g].shape[0] for g in g_set])
    g_args = [fill_val * ones((len(g_set), g_max), dtype=a.dtype) for a in args]
    for gix, gval in enumerate(g_set):
        for ga, a in izip(g_args, args):
            b = a[g_mask==gval]
            ga[gix,:len(b)] = b
    return tuple(g_args)


if __name__ == "__main__":
    from numpy import arange, set_printoptions, random
    set_printoptions(precision=2, suppress=True, linewidth=60);
    b = arange(100, 200)
    c = agroupby(b, key=lambda x: x%10)
    print c
    
    a = random.geometric(0.01, 20)
    b = a + 20
    c, d = agroupby(a, b, key=lambda x: x%10)
    print c
    print d
