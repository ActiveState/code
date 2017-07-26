"""
Iterator algebra implementations of join algorithms: hash join, merge
join, and nested loops join, as well as a variant I dub "bisect join".

Requires Python 2.4.

Author: Jim Baker, jbaker@zyasoft.com

Define some relations to join:
>>> accounts = [
...    ('spender', 'Big', 'Spender', '123-456-7890'),
...    ('saver', 'Thrifty', 'Saver', '234-567-8901'),
...    ('nobody', 'A', 'Nobody', '999-999-9999')]
>>> transactions = [
...    ('spender', 'deposited', 100),
...    ('spender', 'withdraw', 40),
...    ('spender', 'withdraw', 15),
...    ('spender', 'withdraw', 25),
...    ('saver',  'deposited', 30)]

Given the above data, a useful join predicate is the first element of
each tuple. This will give us a usable equijoin:
>>> def first(x): return x[0]

Test that the implemented join methods are equivalent:
>>> nj = set(nested_loops_join(accounts, transactions, first))
>>> mj = set(merge_join(accounts, transactions, first))
>>> hj = set(hash_join(accounts, transactions, first))
>>> bj = set(bisect_join(accounts, transactions, first))
>>> nj == mj
True
>>> nj == hj
True
>>> mj == hj
True
>>> bj == hj
True

Perform a Cartesian join. In this case, we need a predicate that
returns the same value for every tuple, so in this case returning True
is arbitrary:
>>> def always(x): return True

With 5 tuples in transactions and 3 tuples in accounts, we should get
15 tuples:
>>> len(list(hash_join(accounts, transactions, always)))
15

With semijoins and outer joins, we now see the power of the
iterator approach. A left join will return a tuple even if there is
not a match on the predicate:
>>> lj = set(hash_join(accounts, transactions, first, 
...                    join=lambda X: left(X, when_empty=tuple([None]*3))))
>>> len(lj)
6

A full outer join is simply the union of a left join and a right
join. Let's make a right join by reversing the order of the join. We
will also to need to reverse how we combine the tuples:
>>> rj = set(nested_loops_join(transactions, accounts, first,
...                            combine=lambda r, s: s + r,
...                            join=lambda X: left(X, when_empty=tuple([None]*2))))
>>> len(rj)
5

Note that we have no activity in this example without an accompanying
account, so it's the same as an inner join. Now let's compute the full
outer join:
>>> foj = lj | rj
>>> len(foj)
6

A semijoin will return only the first matching tuple:
>>> len(list(hash_join(accounts, transactions, first, semi)))
2

>>> len(list(merge_join(accounts, transactions, first, semi)))
2

Semijoins are useful, especially in conjunction with hierarchical
queries. In SQL, if supported, they are the efficient alternative to
writing 'select distinct', although they make one's code difficult to
understand by the unversed.  Hopefully showing this with procedural
code can make this useful feature less mysterious.

"""

import operator

def identity(x):
    """x -> x

    As a predicate, this function is useless, but it provides a
    useful/correct default.

    >>> identity(('apple', 'banana', 'cherry'))
    ('apple', 'banana', 'cherry')
    """
    return x

def inner(X):
    """
    >>> X = [1, 2, 3, 4, 5]
    >>> list(inner(X))
    [1, 2, 3, 4, 5]
    """
    for x in X:
        yield x

def semi(X):
    """Returns X[0] if X is not empty

    >>> X = [1, 2, 3, 4, 5]
    >>> list(semi(X))
    [1]
    """
    
    for x in X:
        yield x
        break

def left(X, when_empty=()):
    empty = True
    for x in X:
        yield x
        empty = False
    if empty:
        yield when_empty
        

# Xp can mean X-prime or X-with-predicate; we use both meanings
# interchangeably here in the shorthand of this code.
# Xp -> (p(x0), x0), (p(x1), x1), ... 

# throughout, we assume S is the smaller relation of R and S.

def hash_join(R, S, predicate=identity, join=inner, combine=operator.concat):
    hashed = {}
    for s in S:
        hashed.setdefault(predicate(s),[]).append(s)
    for r in R:
        for s in join(hashed.get(predicate(r),())):
            yield combine(r, s)

def nested_loops_join(R, S, predicate=identity, join=inner,
                      combine=operator.concat, theta=operator.eq):
    Sp = [(predicate(s), s) for s in S]
    for r in R:
        rp = predicate(r) 
        for s in join(s for sp, s in Sp if theta(rp, sp)):
            yield combine(r, s)

def bisect_join(R, S, predicate=identity, join=inner, combine=operator.concat):
    """
    I have not found discussion of this variant on the sort-merge join anywhere.
    """

    from bisect import bisect_left

    def consume(Sp, si, rp):
        """This needs a better name..."""
        length = len(S)
        while si < length:
            sp, s = Sp[si]
            if rp == sp:
                yield s
            else:
                break
            si += 1

    Rp = sorted((predicate(r), r) for r in R)
    Sp = sorted((predicate(s), s) for s in S)

    for rp, r in Rp:
        si = bisect_left(Sp, (rp,))
        for s in join(consume(Sp, si, rp)):
            yield combine(r, s)


def merge_join(R, S, predicate=identity, join=inner, combine=operator.concat):
    """
    For obvious reasons, we depend on the predicate providing a
    sortable relation.

    Compare this presentation using iterator algebra with the much
    more difficult to follow presentation (IMHO) in
    http://en.wikipedia.org/wiki/Sort-Merge_Join
    """

    from itertools import groupby


    def advancer(Xp):
        """A simple wrapper of itertools.groupby, we simply need
        to follow our convention that Xp -> (xp0, x0), (xp1, x1), ...
        """

        for k, g in groupby(Xp, key=operator.itemgetter(0)):
            yield k, list(g)
    
    R_grouped = advancer(sorted((predicate(r), r) for r in R))
    S_grouped = advancer(sorted((predicate(s), s) for s in S))

    # in the join we need to distinguish rp from rk in the unpack, so
    # just use rk, sk
    rk, R_matched = R_grouped.next()
    sk, S_matched = S_grouped.next()

    while R_grouped and S_grouped:
        comparison = cmp(rk, sk)
        if comparison == 0:
            # standard Cartesian join here on the matched tuples, as
            # subsetted by the join method
            for rp, r in R_matched:
                for sp, s in join(S_matched):
                    yield combine(r, s)
            rk, R_matched = R_grouped.next()
            sk, S_matched = S_grouped.next()
        elif comparison > 0:
            sk, S_matched = S_grouped.next()
        else:
            rk, R_matched = R_grouped.next()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
