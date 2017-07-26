#!/usr/bin/env python

"""Swatch Internet Time

This little recipe calculates Swatch Internet Time also known as Beats.
See: http://en.wikipedia.org/wiki/Swatch_Internet_Time
"""

from time import localtime, timezone


def itime():
    """Calculate and return Swatch Internet Time

    :returns: No. of beats (Swatch Internet Time)
    :rtype: float
    """

    h, m, s = localtime()[3:6]
    beats = ((h * 3600) + (m * 60) + s + timezone) / 86.4

    if beats > 1000:
        beats -= 1000
    elif beats < 0:
        beats += 1000

    return beats


def test():
    print("@{0:0.3f}".format(itime()))


if __name__ == "__main__":
    test()
