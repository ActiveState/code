"""Hopefully this function will save you the trip to oocalc/excel. Py3k code.

"""

def nth(n):
    m = abs(n)
    if m % 10 < 4 and m // 10 != 1:
        return '{}{}'.format(n, ('th', 'st', 'nd', 'rd')[m % 10])
    return '{}{}'.format(n, 'th')

def rangeth(*args):
    """rangeth([start,] stop[, skip]) -> list of places (rankings)

returns a list of strings as places in a list (1st, 2nd, etc)

>>> rangeth(4)
['0th', '1st', '2nd', '3rd']

    """
    return list(map(nth, range(*args)))
