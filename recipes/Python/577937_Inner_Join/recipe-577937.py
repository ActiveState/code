def inner_join(lot0, lot1, key0=None, key1=None, sort=True):
    ''' Joins two lists of tuples (or namedtuples) on a key field.
        If a keyfunc is not specified, it defaults to the first field in each tuple.
        Returns a sorted list in the form:  result [(key, lot1_tuple, lot2_tuple) ...]

        Keys in lot0 but not lot1 raise a KeyError.
        Keys in lot1 but not lot0 are silently ignored.
        Tuples with a non-unique key (duplicates) are silently ignored.

        Keys must be hashable and orderable or a TypeError is raised.
        Running time is O(n log n) due to the sorting step.

        from collections import namedtuple
        Employee = namedtuple('Employee', 'name dept paygrade')
        Person = namedtuple('Person', 'name age gender status')
        ee = [Employee('adam', 'acct', 8),
        ...   Employee('betty', 'sales', 9),
        ...   Employee('charlie', 'acct', 2),
        ... ]
        pp = [Person('adam', 30, 'm', 'single'),
        ...   Person('betty', 28, 'f', 'married'),
        ...   Person('charlie', 40, 'm', 'single'),
        ... ]
        for k, e, p in inner_join(ee, pp):
        ...    print k, e.dept, p.age
        adam acct 30
        betty sales 28
        charlie acct 40

    '''
    key0 = key0 or (lambda r: r[0])
    key1 = key1 or (lambda r: r[0])
    d0 = {key0(r): r for r in lot0}
    d1 = {key1(r): r for r in lot1}
    seq = sorted(d0) if sort else iter(d0)
    return [(k, d0[k], d1[k]) for k in seq]


if __name__ == '__main__':
    import doctest
    print doctest.testmod()
