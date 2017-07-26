#!/usr/bin/python3

""" Test script for lru_timestamp function.

usage: lru.py [-h] [-r REFRESH] [-s SLEEP]

optional arguments:
  -h, --help            show this help message and exit
  -r REFRESH, --refresh REFRESH
                        refresh interval (default 60 min)
  -s SLEEP, --sleep SLEEP
                        sleep interval (default 10 min)

"""

import argparse
import datetime
import functools
import random
import time


def lru_timestamp(refresh_interval=60):
    """ Return a timestamp string for @lru_cache decorated functions.

    The returned timestamp is used as the value of an extra parameter
    to @lru_cache decorated functions, allowing for more control over
    how often cache entries are refreshed. The lru_timestamp function
    should be called with the same refresh_interval value for a given
    @lru_cache decorated function.  The returned timestamp is for the
    benefit of the @lru_cache decorator and is normally not used by
    the decorated function.

    Positional arguments:
    refresh_interval -- in minutes (default 60), values less than 1
                        are coerced to 1, values more than 1440 are
                        coerced to 1440

    """

    if not isinstance(refresh_interval, int):
        raise TypeError('refresh_interval must be an int from 1-1440')

    dt = datetime.datetime.now()

    if refresh_interval > 60:
        refresh_interval = min(refresh_interval, 60*24)
        fmt = '%Y%m%d'
        minutes = dt.hour * 60
    else:
        refresh_interval = max(1, refresh_interval)
        fmt = '%Y%m%d%H'
        minutes = dt.minute

    ts = dt.strftime(fmt)
    age = minutes // refresh_interval
    return '{0}:{1:d}'.format(ts, age)


@functools.lru_cache()
def calulate(x, y, timestamp):
    """ Return random int for testing lru_timestamp function."""

    print('performing calculation (not from cache), timestamp:', timestamp)
    return random.randint(x, y)


def init():
    """ Return parsed command line args."""

    random.seed()
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    parser.add_argument('-r', '--refresh', type=int, dest='refresh',
                        default=60, help='refresh interval (default 60 min)')

    parser.add_argument('-s', '--sleep', type=int, dest='sleep', default=10,
                        help='sleep interval (default 10 min)')

    return parser.parse_args()


def main():
    """ Script main."""

    args = init()
    print('refresh interval (min):', args.refresh)
    print('sleep interval (min):', args.sleep)
    print()
    refresh = args.refresh
    doze = args.sleep * 60

    #num = calulate(1, 1000, lru_timestamp('junk'))
    #num = calulate(1, 1000, lru_timestamp(1.22))
    #num = calulate(1, 1000, lru_timestamp(-1))
    #num = calulate(1, 1000, lru_timestamp(2000))

    while True:
        num = calulate(1, 1000, lru_timestamp(refresh))
        print('calculation returned', num)
        time.sleep(doze)

if __name__ == '__main__':
    main()
