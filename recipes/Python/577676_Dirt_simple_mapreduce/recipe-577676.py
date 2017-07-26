from collections import namedtuple
from math import fsum

def map_reduce(data, mapper, reducer=None):
    '''Simple map/reduce for data analysis.

    Each data element is passed to a *mapper* function.
    The mapper returns key/value pairs
    or None for data elements to be skipped.

    Returns a dict with the data grouped into lists.
    If a *reducer* is specified, it aggregates each list.

    >>> def even_odd(elem):                     # sample mapper
    ...     if 10 <= elem <= 20:                # skip elems outside the range
    ...         key = elem % 2                  # group into evens and odds
    ...         return key, elem

    >>> map_reduce(range(30), even_odd)         # show group members
    {0: [10, 12, 14, 16, 18, 20], 1: [11, 13, 15, 17, 19]}

    >>> map_reduce(range(30), even_odd, sum)    # sum each group
    {0: 90, 1: 75}

    '''
    d = {}
    for elem in data:
        r = mapper(elem)
        if r is not None:
            key, value = r
            if key in d:
                d[key].append(value)
            else:
                d[key] = [value]
    if reducer is not None:
        for key, group in d.items():
            d[key] = reducer(group)
    return d

Summary = namedtuple('Summary', ['n', 'lo', 'mean', 'hi', 'std_dev'])

def describe(data):
    'Simple reducer for descriptive statistics'
    n = len(data)
    lo = min(data)
    hi = max(data)
    mean = fsum(data) / n
    std_dev = (fsum((x - mean) ** 2 for x in data) / n) ** 0.5
    return Summary(n, lo, mean, hi, std_dev)


if __name__ == '__main__':

    from pprint import pprint
    import doctest

    Person = namedtuple('Person', ['name', 'gender', 'age', 'height'])

    persons = [
        Person('mary', 'fem', 21, 60.2),
        Person('suzy', 'fem', 32, 70.1),
        Person('jane', 'fem', 27, 58.1),
        Person('jill', 'fem', 24, 69.1),
        Person('bess', 'fem', 43, 66.6),
        Person('john', 'mal', 25, 70.8),
        Person('jack', 'mal', 40, 59.1),
        Person('mike', 'mal', 42, 60.3),
        Person('zack', 'mal', 45, 63.7),
        Person('alma', 'fem', 34, 67.0),
        Person('bill', 'mal', 20, 62.1),
    ]

    def height_by_gender_and_agegroup(p):
        key = p.gender, p.age //10
        val = p.height
        return key, val

    pprint(persons)                                                      # upgrouped dataset
    pprint(map_reduce(persons, lambda p: ((p.gender, p.age//10), p)))    # grouped people
    pprint(map_reduce(persons, height_by_gender_and_agegroup, None))     # grouped heights
    pprint(map_reduce(persons, height_by_gender_and_agegroup, len))      # size of each group
    pprint(map_reduce(persons, height_by_gender_and_agegroup, describe)) # describe each group
    print(doctest.testmod())
