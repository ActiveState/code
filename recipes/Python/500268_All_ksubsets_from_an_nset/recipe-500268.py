def k_subsets_i(n, k):
    '''
    Yield each subset of size k from the set of intergers 0 .. n - 1
    n -- an integer > 0
    k -- an integer > 0
    '''
    # Validate args
    if n < 0:
        raise ValueError('n must be > 0, got n=%d' % n)
    if k < 0:
        raise ValueError('k must be > 0, got k=%d' % k)
    # check base cases
    if k == 0 or n < k:
        yield set()
    elif n == k:
        yield set(range(n))

    else:
        # Use recursive formula based on binomial coeffecients:
        # choose(n, k) = choose(n - 1, k - 1) + choose(n - 1, k)
        for s in k_subsets_i(n - 1, k - 1):
            s.add(n - 1)
            yield s
        for s in k_subsets_i(n - 1, k):
            yield s

def k_subsets(s, k):
    '''
    Yield all subsets of size k from set (or list) s
    s -- a set or list (any iterable will suffice)
    k -- an integer > 0
    '''
    s = list(s)
    n = len(s)
    for k_set in k_subsets_i(n, k):
        yield set([s[i] for i in k_set])

def __test__():
    two_sets = list(k_subsets_i(10, 2))
    assert len(two_sets) == 45
    two_set = two_sets[0]
    assert len(two_set) == 2

    class Tester:
        def __init__(self, i):
            self.i = i
        def __repr__(self):
            return 'Tester(%d)' % self.i
    super_set = [Tester(i) for i in range(100, 200, 10)]
    two_sets = list(k_subsets(super_set, 2))
    assert len(two_sets) == 45
    two_set = two_sets[0]
    assert len(two_set) == 2
    assert isinstance(two_set.pop(), Tester)
__test__()

for two in k_subsets(range(20, 26), 2):
    print two

# prints:
set([24, 25])
set([25, 23])
set([25, 22])
set([25, 21])
set([25, 20])
set([24, 23])
set([24, 22])
set([24, 21])
set([24, 20])
set([22, 23])
set([21, 23])
set([20, 23])
set([21, 22])
set([20, 22])
set([20, 21])
