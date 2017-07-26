"""
A function for flexible datetime parsing.
"""

from datetime import datetime
from itertools import permutations


def str2date(string):
    "Parse a string into a datetime object."

    for fmt in dateformats():
        try:
            return datetime.strptime(string, fmt)
        except ValueError:
            pass

    raise ValueError("'%s' is not a recognized date/time" % string)


def dateformats():
    "Yield all combinations of valid date formats."

    years = ("%Y",)
    months = ("%b", "%B")
    days = ("%d",)
    times = ("%I%p", "%I:%M%p", "%H:%M", "")

    for year in years:
        for month in months:
            for day in days:
                for args in ((day, month), (month, day)):
                    date = " ".join(args)
                    for time in times:
                        for combo in permutations([year, date, time]):
                            yield " ".join(combo).strip()

if __name__ == "__main__":
    tests = """
    10 May 2003 4pm
    3 feb 2011 23:32
    17 aug 1962
    Aug 22 1943 19:22
    14:55 aug 15 1976
    21 march 2005 6am
    2002 apr 10 5:32am
    14 Octember 2023
    """

    for string in tests.strip().split("\n"):
        s = string.strip()
        print "%-20s" % s,

        try:
            print str2date(s)
        except ValueError:
            print "invalid date/time"
