#!/usr/bin/env python

from datetime import date, timedelta

def monday_of_week_one(yyyy):
    """ Method to calculate date for Monday of first week of year

    >>> monday_of_week_one(1970)
    datetime.date(1969, 12, 29)
    """

    REF_DAY = date(yyyy, 1, 4)
    DOW = REF_DAY.weekday()
    MONDAY = REF_DAY - timedelta(days = DOW)

    return MONDAY

if __name__ == '__main__':

    import doctest
    doctest.testmod()
